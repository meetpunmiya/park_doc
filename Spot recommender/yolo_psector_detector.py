import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time
from flask import Flask, render_template

app = Flask(__name__)

class ParkingRecommendation:
    def __init__(self, video_path='parking2.mp4', model_path='yolov8s.pt', coco_path='coco.txt'):
        self.video_path = video_path
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(video_path)
        self.class_list = self.load_class_list(coco_path)
        self.area1 = [(52, 364), (30, 417), (409, 408), (382, 340)]
        self.area2 = [(396, 338), (426, 404), (764, 355), (707, 308)]

    def load_class_list(self, coco_path):
        with open(coco_path, 'r') as f:
            return f.read().split("\n")

    def get_parking_recommendation(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            time.sleep(0.1)
            frame = cv2.resize(frame, (1020, 500))
            results = self.model.predict(frame)
            px = pd.DataFrame(results[0].boxes.data).astype("float")
            list1 = []
            list2 = []

            for index, row in px.iterrows():
                x1, y1, x2, y2, _, d = map(int, row)
                c = self.class_list[d]
                if 'car' in c:
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    if cv2.pointPolygonTest(np.array(self.area1, np.int32), ((cx, cy)), False) >= 0:
                        list1.append(c)
                    if cv2.pointPolygonTest(np.array(self.area2, np.int32), ((cx, cy)), False) >= 0:
                        list2.append(c)

            a1 = len(list1)
            spots_left1 = 6 - a1
            a2 = len(list2)
            spots_left2 = 6 - a2

            if a2 == 6 and a1 < 6:
                recommendation = "A"
            else:
                recommendation = "B"

            print(recommendation)
            yield recommendation

    def close(self):
        self.cap.release()

parking_recommendation = ParkingRecommendation()
#--
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendation')
def get_recommendation():
    recommendation = next(parking_recommendation.get_parking_recommendation())
    return recommendation

if __name__ == '__main__':
    app.run(debug=True)
