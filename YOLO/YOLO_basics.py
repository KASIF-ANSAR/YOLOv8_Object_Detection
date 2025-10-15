import cv2
from ultralytics import YOLO


model = YOLO('../YOLO-weights/yolov8l.pt')
results = model("images/2.jpeg",show=True)
cv2.waitKey(0)
