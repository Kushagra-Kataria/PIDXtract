# import cv2
# import matplotlib.pyplot as plt
# import networkx as nx
# from ultralytics import YOLO
# from scipy.spatial import distance
# from paddleocr import PaddleOCR
# import numpy as np
# from shapely.geometry import Polygon

# def main(image_path):
#     model = YOLO(r"best.pt")
#     image = cv2.imread(image_path)

#     results = model.predict(image_path)
#     boxes = results[0].boxes.xyxy.tolist()
#     classes = [model.names[int(c)] for c in results[0].boxes.cls.tolist()]

#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (7, 7), 3)
#     edges = cv2.Canny(blurred, 20, 80)
#     lines = detect_lines(edges)

#     texts_around_objects = run_ocr_around_objects(image, boxes)
#     G = build_graph_with_oriented_ocr(boxes, classes, lines, image.shape, texts_around_objects)
#     visualize_graph(G, image, show_original=False) # Modified visualize_graph call

#     print(f"\n✅ Labeling Summary: {sum(1 for n in G.nodes if G.nodes[n]['label'] != 'Unlabeled')} labeled / {len(G.nodes)} total symbols")
#     return G

# def detect_lines(edges):
#     lines = cv2.HoughLinesP(edges, 0.8, np.pi / 180, 15, minLineLength=20, maxLineGap=30)
#     return lines.reshape(-1, 4).tolist() if lines is not None else []

# def run_ocr_around_objects(image, boxes):
#     ocr = PaddleOCR(use_angle_cls=True, use_gpu=True)
#     object_texts = []
#     padding = 80  # Increased padding to capture nearby text

#     for i, box in enumerate(boxes):
#         x1, y1, x2, y2 = map(int, box)
#         crop_region = image[max(0, y1 - padding):min(image.shape[0], y2 + padding),
#                              max(0, x1 - padding):min(image.shape[1], x2 + padding)]
#         results = ocr.ocr(crop_region, cls=True)
#         texts_around = []
#         if results and results[0]:
#             for line in results[0]:
#                 box_coords = line[0]
#                 text, conf = line[1]
#                 angle = line[2] if len(line) > 2 else 0.0 # Check if angle is the third element

#                 # Adjust text box coordinates to be relative to the original image
#                 original_box_coords = [[int(coord[0] + max(0, x1 - padding)), int(coord[1] + max(0, y1 - padding))] for coord in box_coords]
#                 cx = (original_box_coords[0][0] + original_box_coords[2][0]) / 2
#                 cy = (original_box_coords[0][1] + original_box_coords[2][1]) / 2
#                 texts_around.append(((cx, cy), text.strip(), conf, original_box_coords, angle))
#         object_texts.append(texts_around)
#     return object_texts

# def build_graph_with_oriented_ocr(boxes, classes, lines, img_shape, texts_around_objects):
#     G = nx.Graph()
#     node_positions = []

#     for i, (box, cls, nearby_texts) in enumerate(zip(boxes, classes, texts_around_objects)):
#         center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
#         best_label = find_best_oriented_label(center, nearby_texts, box)
#         G.add_node(i, type=cls, pos=center, box=box, label=best_label)
#         node_positions.append(center)

#     connect_components(G, lines, node_positions)
#     connect_proximity(G, node_positions, max_distance=250)
#     return G

# def find_best_oriented_label(symbol_center, nearby_texts, symbol_box):
#     best_label = "Unlabeled"
#     best_score = -1
#     sx1, sy1, sx2, sy2 = symbol_box
#     symbol_width = sx2 - sx1
#     symbol_height = sy2 - sy1

#     for (tx, ty), txt, conf, text_bbox, angle in nearby_texts:
#         distance_val = distance.euclidean(symbol_center, (tx, ty))
#         rel_x_center = (tx - symbol_center[0]) / (symbol_width + 1e-6)
#         rel_y_center = (ty - symbol_center[1]) / (symbol_height + 1e-6)
#         abs_angle_deg = abs(angle)

#         score = 0
#         proximity_score = np.exp(-distance_val / (max(symbol_width, symbol_height) * 2 + 1e-6))
#         score += 0.3 * proximity_score
#         score += 0.3 * conf

#         alignment_score = 0
#         if abs_angle_deg < 15: # Horizontal text
#             if abs(rel_x_center) < 0.4 and (rel_y_center < -0.7 or rel_y_center > 0.7):
#                 alignment_score += 0.4
#             elif abs(rel_y_center) < 0.4 and (rel_x_center < -0.7 or rel_x_center > 0.7):
#                 alignment_score += 0.2
#         elif abs_angle_deg > 75 and abs_angle_deg < 105: # Roughly vertical (90 degrees)
#             if rel_x_center > 0.5 and abs(rel_y_center) < 0.5: # To the right, vertically aligned
#                 alignment_score += 0.6
#             elif rel_x_center < -0.5 and abs(rel_y_center) < 0.5: # To the left, vertically aligned
#                 alignment_score += 0.4

#         score += 0.4 * alignment_score

#         if score > best_score:
#             best_score = score
#             best_label = txt

#     return best_label

# def connect_components(G, lines, node_positions):
#     for line in lines:
#         start = (line[0], line[1])
#         end = (line[2], line[3])
#         start_node = find_nearest_node(start, node_positions)
#         end_node = find_nearest_node(end, node_positions)
#         if start_node != end_node:
#             G.add_edge(start_node, end_node, type="direct")

# def connect_proximity(G, positions, max_distance=250):
#     for i in range(len(positions)):
#         for j in range(i + 1, len(positions)):
#             if distance.euclidean(positions[i], positions[j]) < max_distance:
#                 if not G.has_edge(i, j):
#                     G.add_edge(i, j, type="proximity")

# def find_nearest_node(point, positions):
#     distances = [distance.euclidean(point, pos) for pos in positions]
#     return np.argmin(distances)

# def visualize_graph(G, image, show_original=True):
#     plt.figure(figsize=(14, 14), dpi=150) # Adjust figure size for a single plot
#     img_height, img_width = image.shape[:2]
#     ax = plt.subplot(111) # Create a single subplot

#     ax.set_xlim(0, img_width)
#     ax.set_ylim(img_height, 0)
#     ax.set_aspect('equal')
#     ax.set_facecolor('white')

#     pos = {n: (G.nodes[n]["pos"][0], img_height - G.nodes[n]["pos"][1]) for n in G.nodes}

#     for u, v, data in G.edges(data=True):
#         x, y = [pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]]
#         ax.plot(x, y,
#                 color='#2C3E50' if data['type'] == 'direct' else '#AAB7B8',
#                 linewidth=3 if data['type'] == 'direct' else 1.5,
#                 linestyle='-' if data['type'] == 'direct' else '--', alpha=0.8)

#     symbol_map = {
#         "Valve": {'marker': '^', 'size': 20},
#         "Pipe": {'marker': '_', 'size': 30},
#         "Sensor": {'marker': 's', 'size': 20},
#         "Control_Panel": {'marker': 'd', 'size': 20},
#         "Uncategorized": {'marker': 'o', 'size': 20}
#     }

#     color_map = {
#         "Valve": "#FF5733",
#         "Pipe": "#5DADE2",
#         "Sensor": "#58D68D",
#         "Control_Panel": "#F4D03F",
#         "Uncategorized": "#AAB7B8"
#     }

#     for node in G.nodes:
#         node_type = G.nodes[node]["type"]
#         label = G.nodes[node].get("label", "Unlabeled")
#         color = color_map.get(node_type, "#AAB7B8")
#         if label == "Unlabeled":
#             color = "#E74C3C"  # red highlight for missing label

#         marker = symbol_map.get(node_type, symbol_map["Uncategorized"])['marker']
#         size = symbol_map.get(node_type, symbol_map["Uncategorized"])['size']
#         x, y = pos[node]

#         ax.scatter(x, y, s=size, c=color, marker=marker, edgecolors='black', linewidths=1.5, alpha=0.9)
#         ax.text(x, y - 8, f"{label}", fontsize=6, color='black', ha='center', va='bottom')
#         ax.text(x, y + 8, f"({node_type})", fontsize=5.5, color='gray', ha='center', va='top')

#     ax.grid(True, color='#D5DBDB', linestyle='--', linewidth=0.6)
#     ax.set_title("Generated Graph with OCR Labels", fontsize=18) # Updated title
#     ax.axis('off')

#     plt.tight_layout()
#     plt.savefig("static/predict/generated_graph.jpg", bbox_inches='tight') # Save the generated graph
#     plt.close()
    
#     # plt.show()

# # Example usage
# # if __name__ == "__main__":
# #     image_path = r"static/uploads/4.jpg"
# #     G = main(image_path)

# def makegraph(img_path):
#     G = main(img_path)
# # makegraph("static/uploads/4.jpg")

import cv2
import numpy as np
import networkx as nx
from ultralytics import YOLO
from scipy.spatial import distance
from paddleocr import PaddleOCR
from shapely.geometry import Polygon

def main(image_path):
    model = YOLO(r"best.pt")
    image = cv2.imread(image_path)

    results = model.predict(image_path)
    boxes = results[0].boxes.xyxy.tolist()
    classes = [model.names[int(c)] for c in results[0].boxes.cls.tolist()]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 3)
    edges = cv2.Canny(blurred, 20, 80)
    lines = detect_lines(edges)

    texts_around_objects = run_ocr_around_objects(image, boxes)
    G = build_graph_with_oriented_ocr(boxes, classes, lines, image.shape, texts_around_objects)
    visualize_graph(G, image)  # Now uses OpenCV to save

    print(f"\n✅ Labeling Summary: {sum(1 for n in G.nodes if G.nodes[n]['label'] != 'Unlabeled')} labeled / {len(G.nodes)} total symbols")
    return G

def detect_lines(edges):
    lines = cv2.HoughLinesP(edges, 0.8, np.pi / 180, 15, minLineLength=20, maxLineGap=30)
    return lines.reshape(-1, 4).tolist() if lines is not None else []

def run_ocr_around_objects(image, boxes):
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=True)
    object_texts = []
    padding = 80

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)
        crop_region = image[max(0, y1 - padding):min(image.shape[0], y2 + padding),
                             max(0, x1 - padding):min(image.shape[1], x2 + padding)]
        results = ocr.ocr(crop_region, cls=True)
        texts_around = []
        if results and results[0]:
            for line in results[0]:
                box_coords = line[0]
                text, conf = line[1]
                angle = line[2] if len(line) > 2 else 0.0
                original_box_coords = [[int(coord[0] + max(0, x1 - padding)), int(coord[1] + max(0, y1 - padding))] for coord in box_coords]
                cx = (original_box_coords[0][0] + original_box_coords[2][0]) / 2
                cy = (original_box_coords[0][1] + original_box_coords[2][1]) / 2
                texts_around.append(((cx, cy), text.strip(), conf, original_box_coords, angle))
        object_texts.append(texts_around)
    return object_texts

def build_graph_with_oriented_ocr(boxes, classes, lines, img_shape, texts_around_objects):
    G = nx.Graph()
    node_positions = []

    for i, (box, cls, nearby_texts) in enumerate(zip(boxes, classes, texts_around_objects)):
        center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
        best_label = find_best_oriented_label(center, nearby_texts, box)
        G.add_node(i, type=cls, pos=center, box=box, label=best_label)
        node_positions.append(center)

    connect_components(G, lines, node_positions)
    connect_proximity(G, node_positions, max_distance=250)
    return G

def find_best_oriented_label(symbol_center, nearby_texts, symbol_box):
    best_label = "Unlabeled"
    best_score = -1
    sx1, sy1, sx2, sy2 = symbol_box
    symbol_width = sx2 - sx1
    symbol_height = sy2 - sy1

    for (tx, ty), txt, conf, text_bbox, angle in nearby_texts:
        distance_val = distance.euclidean(symbol_center, (tx, ty))
        rel_x_center = (tx - symbol_center[0]) / (symbol_width + 1e-6)
        rel_y_center = (ty - symbol_center[1]) / (symbol_height + 1e-6)
        abs_angle_deg = abs(angle)

        score = 0
        proximity_score = np.exp(-distance_val / (max(symbol_width, symbol_height) * 2 + 1e-6))
        score += 0.3 * proximity_score
        score += 0.3 * conf

        alignment_score = 0
        if abs_angle_deg < 15:
            if abs(rel_x_center) < 0.4 and (rel_y_center < -0.7 or rel_y_center > 0.7):
                alignment_score += 0.4
            elif abs(rel_y_center) < 0.4 and (rel_x_center < -0.7 or rel_x_center > 0.7):
                alignment_score += 0.2
        elif abs_angle_deg > 75 and abs_angle_deg < 105:
            if rel_x_center > 0.5 and abs(rel_y_center) < 0.5:
                alignment_score += 0.6
            elif rel_x_center < -0.5 and abs(rel_y_center) < 0.5:
                alignment_score += 0.4

        score += 0.4 * alignment_score

        if score > best_score:
            best_score = score
            best_label = txt

    return best_label

def connect_components(G, lines, node_positions):
    for line in lines:
        start = (line[0], line[1])
        end = (line[2], line[3])
        start_node = find_nearest_node(start, node_positions)
        end_node = find_nearest_node(end, node_positions)
        if start_node != end_node:
            G.add_edge(start_node, end_node, type="direct")

def connect_proximity(G, positions, max_distance=250):
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            if distance.euclidean(positions[i], positions[j]) < max_distance:
                if not G.has_edge(i, j):
                    G.add_edge(i, j, type="proximity")

def find_nearest_node(point, positions):
    distances = [distance.euclidean(point, pos) for pos in positions]
    return np.argmin(distances)

# def visualize_graph(G, image):
#     img_height, img_width = image.shape[:2]
#     canvas = np.ones((img_height, img_width, 3), dtype=np.uint8) * 255

#     pos = {n: G.nodes[n]["pos"] for n in G.nodes}
#     for u, v, data in G.edges(data=True):
#         color = (44, 62, 80) if data['type'] == 'direct' else (170, 183, 184)
#         thickness = 3 if data['type'] == 'direct' else 1
#         cv2.line(canvas,
#                  (int(pos[u][0]), int(pos[u][1])),
#                  (int(pos[v][0]), int(pos[v][1])),
#                  color, thickness)

#     for node in G.nodes:
#         node_type = G.nodes[node]["type"]
#         label = G.nodes[node].get("label", "Unlabeled")
#         x, y = int(pos[node][0]), int(pos[node][1])

#         color_map = {
#             "Valve": (51, 87, 255),
#             "Pipe": (218, 165, 32),
#             "Sensor": (88, 214, 141),
#             "Control_Panel": (244, 208, 63),
#             "Uncategorized": (170, 183, 184),
#             "Unlabeled": (231, 76, 60)
#         }
#         color = color_map.get(node_type, color_map["Uncategorized"])
#         if label == "Unlabeled":
#             color = color_map["Unlabeled"]

#         cv2.circle(canvas, (x, y), 50, color, -1)
#         cv2.putText(canvas, label, (x - 8, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 0), 1)
#         cv2.putText(canvas, f"({node_type})", (x - 9, y + 15), cv2.FONT_HERSHEY_SIMPLEX, 5, (100, 100, 100), 1)

#     canvas =  cv2.resize(canvas,(1088,1088))

#     cv2.imwrite("static/predict/generated_graph.jpg", canvas)

# To generate graph
def visualize_graph(G, image, target_size=(1088, 1088)):
    original_height, original_width = image.shape[:2]
    target_width, target_height = target_size

    # Calculate scale factors
    scale_x = target_width / original_width
    scale_y = target_height / original_height

    # Resize original image to fit canvas
    resized_image = cv2.resize(image, target_size)
    canvas = np.ones_like(resized_image) * 255

    # Scaled node positions
    pos = {
        n: (
            int(G.nodes[n]["pos"][0] * scale_x),
            int(G.nodes[n]["pos"][1] * scale_y)
        )
        for n in G.nodes
    }

    for u, v, data in G.edges(data=True):
        color = (44, 62, 80) if data['type'] == 'direct' else (170, 183, 184)
        thickness = 3 if data['type'] == 'direct' else 1
        cv2.line(canvas, pos[u], pos[v], color, thickness)

    for node in G.nodes:
        node_type = G.nodes[node]["type"]
        label = G.nodes[node].get("label", "Unlabeled")
        x, y = pos[node]

        color_map = {
            "Valve": (51, 87, 255),
            "Pipe": (218, 165, 32),
            "Sensor": (88, 214, 141),
            "Control_Panel": (244, 208, 63),
            "Uncategorized": (170, 183, 184),
            "Unlabeled": (231, 76, 60)
        }
        color = color_map.get(node_type, color_map["Uncategorized"])
        if label == "Unlabeled":
            color = color_map["Unlabeled"]

        radius = max(10, int(50 * min(scale_x, scale_y)))
        font_scale = max(0.4, min(scale_x, scale_y) * 1.2)

        cv2.circle(canvas, (x, y), radius, color, -1)
        cv2.putText(canvas, label, (x - radius // 2, y - radius // 2), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 0), 1)
        cv2.putText(canvas, f"({node_type})", (x - radius // 2, y + radius // 2), cv2.FONT_HERSHEY_SIMPLEX, font_scale * 0.9, (100, 100, 100), 1)

    cv2.imwrite("static/predict/generated_graph.jpg", canvas)
def makegraph(img_path):
    G = main(img_path)

    return G

# Example usage:
# makegraph("static/uploads/4.jpg")