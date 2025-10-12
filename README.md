 
# YOLOv8 Vehicle & People Counting

Real-time vehicle and people counting using **YOLOv8** and **SORT tracker** with Python and OpenCV.  
The project detects objects, tracks them across frames, and counts them when they cross predefined lines.

---

## Features

- **Vehicle counting:** car, truck, bus, motorbike  
- **People counting:** pedestrians moving up and down  
- **Region of interest (ROI):** Only counts objects in specific areas using masks  
- **Unique IDs:** Tracks objects using SORT to avoid double counting  
- **Real-time visualization:** Shows bounding boxes, IDs, and total count  
- **Overlay graphics:** Optional visual overlays for better presentation  

---

## How It Works

1. **YOLOv8 Object Detection**  
   - We use YOLOv8 (`yolov8n.pt` or `yolov8l.pt`) to detect objects in each frame of the video.  
   - The model predicts bounding boxes, class IDs, and confidence scores.

2. **Region of Interest (Mask)**  
   - We define a mask image to specify the counting area.  
   - Only objects inside the masked region are processed to reduce false detections.

3. **Tracking with SORT**  
   - SORT (Simple Online Realtime Tracking) assigns unique IDs to each detected object.  
   - Tracks objects across multiple frames to ensure accurate counting.  
   - Updates the positions of objects and maintains their IDs even if temporarily occluded.

4. **Counting Logic**  
   - Predefined **counting lines** (up/down) are drawn.  
   - Each tracked object's center point is checked against these lines.  
   - If the object crosses the line, it is counted once and the line turns green to indicate a successful count.

5. **Visualization**  
   - Bounding boxes with rounded corners using `cvzone.cornerRect`.  
   - Object IDs displayed above each bounding box.  
   - Total count of vehicles or people displayed on the frame.  
   - Optional graphics overlay for a professional dashboard look.

---

## Folder Structure



