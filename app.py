import cv2
from ultralytics import YOLO
import random
import numpy as np
from graphonly import makegraph
# Configuration
MODEL_PATH = r'best.pt'  # Your trained model path
# IMAGE_PATH = r'4.jpg'  # Path to your test image
CLASS_NAMES = ['Valve', 'Pipe', 'Sensor', 'Control_Panel','Uncategorized']  # Your class names
COLORS = {cls: [random.randint(0, 255) for _ in range(3)] for cls in CLASS_NAMES}
nums = [0,0,0,0,0]

def visualize_predictions(IMAGE_PATH):
    # Load model
    model = YOLO(MODEL_PATH)
    
    # Load image
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        raise FileNotFoundError(f"Image not found at {IMAGE_PATH}")
    
    # Run inference
    results = model.predict(image, conf=0.3, iou=0.5)
    
    # Draw predictions
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy().astype(int)
        print("chotu", class_ids)

        class_ids = result.boxes.cls.cpu().numpy().astype(int)

# Count occurrences of 0 to 4
        counts = {i: np.count_nonzero(class_ids == i) for i in range(5)}

        print(counts)
        nums[0] = counts[0]
        print("chotu ", nums[0])
        nums[1] = counts[1]
        nums[2] = counts[2]
        nums[3] = counts[3]
        nums[4] = counts[4]
        
        for box, conf, cls_id in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = map(int, box)
            class_name = CLASS_NAMES[cls_id]
            color = COLORS[class_name]
            
            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            
            # Create label text
            label = f"{class_name}: {conf:.2f}"
            
            # Get text size
            (text_width, text_height), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            
            # Draw text background
            cv2.rectangle(image, (x1, y1 - text_height - 10),
                          (x1 + text_width, y1 - 10), color, -1)
            
            # Put text
            cv2.putText(image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Show results
    cv2.imwrite('static/predict/Predictions.jpg', image)


from flask import Flask, render_template, request, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import cv2 as cv

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('index.html', title="Welcome Page")

import time
@app.route('/process-image', methods=['POST'])
def process_image():
    image = request.files['image']
    filename = secure_filename(image.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(save_path)

    visualize_predictions(save_path)
    makegraph(save_path)
    timestamp = int(time.time())

    return jsonify({
        "original_image_url": url_for('static', filename=f'uploads/{filename}') + f"?v={timestamp}",
        "annotated_image_url": url_for('static', filename=f'predict/Predictions.jpg') + f"?v={timestamp}",
        "graph": url_for('static', filename=f'predict/generated_graph.jpg') + f"?v={timestamp}",
        # "graph": "generated_graph.jpg",
        f"{CLASS_NAMES[0]}": nums[0],
        f"{CLASS_NAMES[1]}": nums[1],
        f"{CLASS_NAMES[2]}": nums[2],
        f"{CLASS_NAMES[3]}": nums[3],
        f"{CLASS_NAMES[4]}": nums[4],
    })

if __name__ == '__main__':
    app.run(debug=True)
