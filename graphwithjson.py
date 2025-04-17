import cv2
import matplotlib.pyplot as plt
import networkx as nx
from ultralytics import YOLO
from scipy.spatial import distance
from paddleocr import PaddleOCR
import numpy as np
from shapely.geometry import Polygon
import json

def main(image_path, output_json_path="graph.json"):
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

    try:
        G = build_graph_with_oriented_ocr(boxes, classes, lines, image.shape, texts_around_objects)
        graph_data = nx.node_link_data(G)
        for node in graph_data['nodes']:
            if 'pos' in node:
                node['pos'] = list(map(float, node['pos']))
            if 'box' in node:
                node['box'] = list(map(float, node['box']))
            for key, value in node.items():
                if isinstance(value, np.integer):
                    node[key] = int(value)
                elif isinstance(value, np.floating):
                    node[key] = float(value)
        for link in graph_data['links']:
            for key, value in link.items():
                if isinstance(value, np.integer):
                    link[key] = int(value)
                elif isinstance(value, np.floating):
                    link[key] = float(value)
        with open(output_json_path, 'w') as f:
            json.dump(graph_data, f, indent=4)
        print(f"\n✅ Graph data saved to {output_json_path}")
    except Exception as e:
        print(f"Error during graph generation or saving: {e}")
        return None

    print(f"\n✅ Labeling Summary: {sum(1 for n in G.nodes if G.nodes[n]['label'] != 'Unlabeled')} labeled / {len(G.nodes)} total symbols")
    return G


def detect_lines(edges):
    lines = cv2.HoughLinesP(edges, 0.8, np.pi / 180, 15, minLineLength=20, maxLineGap=30)
    return lines.reshape(-1, 4).tolist() if lines is not None else []

def run_ocr_around_objects(image, boxes):
    ocr = PaddleOCR(use_angle_cls=True, use_gpu=True)
    object_texts = []
    padding = 80  # Increased padding to capture nearby text

    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)
        crop_region = image[max(0, y1 - padding):min(image.shape[0], y2 + padding),
                             max(0, x1 - padding):min(image.shape[1], x2 + padding)]
        try:
            results = ocr.ocr(crop_region, cls=True)
            texts_around = []
            if results and results[0]:
                for line in results[0]:
                    box_coords = line[0]
                    text, conf, angle = line[1] if len(line[1]) == 3 else (line[1][0], line[1][1], 0.0) # Handle cases where angle might be missing
                    # Adjust text box coordinates to be relative to the original image
                    original_box_coords = [[int(coord[0] + max(0, x1 - padding)), int(coord[1] + max(0, y1 - padding))] for coord in box_coords]
                    cx = (original_box_coords[0][0] + original_box_coords[2][0]) / 2
                    cy = (original_box_coords[0][1] + original_box_coords[2][1]) / 2
                    texts_around.append(((cx, cy), text.strip(), float(conf), original_box_coords, float(angle)))
            object_texts.append(texts_around)
        except Exception as e:
            print(f"Error during OCR: {e}")
            return [] # Return an empty list to avoid further errors in main
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
        if abs_angle_deg < 15: # Horizontal text
            if abs(rel_x_center) < 0.4 and (rel_y_center < -0.7 or rel_y_center > 0.7):
                alignment_score += 0.4
            elif abs(rel_y_center) < 0.4 and (rel_x_center < -0.7 or rel_x_center > 0.7):
                alignment_score += 0.2
        elif abs_angle_deg > 75 and abs_angle_deg < 105: # Roughly vertical (90 degrees)
            if rel_x_center > 0.5 and abs(rel_y_center) < 0.5: # To the right, vertically aligned
                alignment_score += 0.6
            elif rel_x_center < -0.5 and abs(rel_y_center) < 0.5: # To the left, vertically aligned
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

def visualize_graph(G, image):
    plt.figure(figsize=(26, 14), dpi=150)
    img_height, img_width = image.shape[:2]
    ax1, ax2 = plt.subplot(121), plt.subplot(122)

    ax1.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    ax1.set_title("Original P&ID Diagram", fontsize=16)
    ax1.axis('off')

    ax2.set_xlim(0, img_width)
    ax2.set_ylim(img_height, 0)
    ax2.set_aspect('equal')
    ax2.set_facecolor('white')

    pos = {n: (float(G.nodes[n]["pos"][0]), float(img_height - G.nodes[n]["pos"][1])) for n in G.nodes}

    for u, v, data in G.edges(data=True):
        x, y = [pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]]
        ax2.plot(x, y,
                 color='#2C3E50' if data['type'] == 'direct' else '#AAB7B8',
                 linewidth=3 if data['type'] == 'direct' else 1.5,
                 linestyle='-' if data['type'] == 'direct' else '--', alpha=0.8)

    symbol_map = {
        "Valve": {'marker': '^', 'size': 20},
        "Pipe": {'marker': '_', 'size': 30},
        "Sensor": {'marker': 's', 'size': 20},
        "Control_Panel": {'marker': 'd', 'size': 20},
        "Uncategorized": {'marker': 'o', 'size': 20}
    }

    color_map = {
        "Valve": "#FF5733",
        "Pipe": "#5DADE2",
        "Sensor": "#58D68D",
        "Control_Panel": "#F4D03F",
        "Uncategorized": "#AAB7B8"
    }

    for node in G.nodes:
        node_type = G.nodes[node]["type"]
        label = G.nodes[node].get("label", "Unlabeled")
        color = color_map.get(node_type, "#AAB7B8")
        if label == "Unlabeled":
            color = "#E74C3C"  # red highlight for missing label

        marker = symbol_map.get(node_type, symbol_map["Uncategorized"])['marker']
        size = symbol_map.get(node_type, symbol_map["Uncategorized"])['size']
        x, y = pos[node]

        ax2.scatter(x, y, s=size, c=color, marker=marker, edgecolors='black', linewidths=1.5, alpha=0.9)
        ax2.text(x, y - 8, f"{label}", fontsize=6, color='black', ha='center', va='bottom')
        ax2.text(x, y + 8, f"({node_type})", fontsize=5.5, color='gray', ha='center', va='top')

    ax2.grid(True, color='#D5DBDB', linestyle='--', linewidth=0.6)
    ax2.set_title("Graph with OCR Labels", fontsize=18)
    ax2.axis('off')

    plt.tight_layout()
    plt.savefig("ouput_graph.jpg", bbox_inches='tight')
    plt.close()
    # plt.show()

# # Example usage
if __name__ == "__main__":
    image_path = r"static\uploads\4.jpg"
    G = main(image_path, "pid_graph1.json") # Specify the output JSON file name
    
# def json_graph(img_path):
    # G = main(img_path, "pid_graph1.json") 
#  main(img_path, "pid_graph1.json") 