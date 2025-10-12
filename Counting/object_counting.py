import numpy as np
from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *

# ----------------------------
# VIDEO SETUP
# ----------------------------
# For webcam:
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)

cap = cv2.VideoCapture('../videos/cars.mp4')

# ----------------------------
# MODEL & CLASSES
# ----------------------------
model = YOLO('../yolo_weights/yolov8n.pt')

classnames = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
    'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
    'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
    'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# ----------------------------
# MASK & TRACKER
# ----------------------------
mask = cv2.imread('mask.png', 0)
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

# Optional: counting line (you can change)
limits = [400, 297, 673, 297]
totalCount = []

# ----------------------------
# MAIN LOOP
# ----------------------------
while True:
    success, img = cap.read()
    if not success:
        break

    # Resize mask once per frame to match frame size
    mask = cv2.resize(mask, (img.shape[1], img.shape[0]))
    imgRegion = cv2.bitwise_and(img, img, mask=mask)

    # Run YOLO detection
    results = model(imgRegion, stream=True)
    detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1

            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            currentClass = classnames[cls]

            # Filter by vehicle type and confidence
            if currentClass in ["car", "truck", "bus", "motorcycle"] and conf > 0.3:
                cvzone.putTextRect(img, f'{currentClass} {conf}',
                                   (max(0, x1), max(35, y1)),
                                   scale=0.7, thickness=1, offset=3)
                cvzone.cornerRect(img, (x1, y1, w, h), l=9)
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))

    # ----------------------------
    # SORT TRACKING
    # ----------------------------
    trackerResults = tracker.update(detections)
    cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)

    for result in trackerResults:
        x1, y1, x2, y2, Id = result
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2 - x1, y2 - y1

        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
        cvzone.putTextRect(img, f'ID {int(Id)}', (max(0, x1), max(35, y1)),
                           scale=1, thickness=1, offset=5)

        # Center of object
        cx, cy = x1 + w // 2, y1 + h // 2
        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        # Count when crossing line
        if limits[0] < cx < limits[2] and (limits[1] - 15) < cy < (limits[1] + 15):
            if totalCount.count(Id) == 0:
                totalCount.append(Id)
                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

    # Show count
    cv2.putText(img, f'Count: {len(totalCount)}', (50, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (50, 50, 255), 3)

    # Display
    cv2.imshow("Image", img)
    cv2.imshow("Image Region", imgRegion)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
