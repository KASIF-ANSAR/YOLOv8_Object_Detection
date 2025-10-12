 
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

---

## 🚗 Vehicle Counting

- Detects cars, buses, trucks, and motorbikes.
- Uses **YOLOv8** for detection and **SORT tracker** for maintaining unique IDs.
- Counts vehicles crossing a defined line in the frame.
- Provides real-time visualization with bounding boxes, IDs, and count on screen.

---

## 🧍 People Counting

- Detects people in crowded areas.
- Supports counting in **two directions**: `Up` and `Down`.
- Uses **masks** to focus on regions of interest.
- Shows total counts for each direction in real-time.

---

## 🏎️ Speed-aware Vehicle Counter

- Tracks vehicles **and calculates their speed** in km/h.
- Uses:
  - Pixel displacement between frames
  - Video FPS
  - Pixel-to-meter ratio (adjustable in `speed_counter.py`)
- Counts only vehicles that **cross the counting line faster than a specified speed threshold** (default: 50 km/h).
- Visualizes:
  - Bounding boxes with unique IDs
  - Vehicle speed above the box
  - Counted vehicles turn the line green

---

## 🛠️ How It Works

1. Load video feed and YOLOv8 model.
2. Apply mask to focus on a region of interest.
3. Detect objects with YOLOv8.
4. Track objects using SORT tracker to maintain IDs across frames.
5. For speed counter:
   - Compute distance traveled per frame for each object.
   - Convert pixel distance → real-world distance using `pixel_to_meter_ratio`.
   - Multiply by FPS to get speed in meters/sec, then convert to km/h.
   - Count objects based on speed and crossing line criteria.
6. Display results with OpenCV overlays.

---

 



