from ultralytics import YOLO
import numpy as np
import cv2
from Utility.utilities import COCOLabels, ColorLabels, Common ,LimitedSizeDict
import logging
import time

class Main:
    def __init__(self, result1=None):
        self.track_record= LimitedSizeDict(size_limit=80)
        self.result1 = result1

    def add_text(self, class_id, track_id, box, input_image):
        x_coord1, y_coord1, x_coord2, y_coord2 = [int(i) for i in box]
        padding = 5
        text: str = f"{COCOLabels(class_id).name}:{track_id}"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        cv2.rectangle(input_image, (x_coord1 - padding, y_coord1 + padding),
                      (x_coord1 + text_width + padding, y_coord1 - text_height - padding),
                      ColorLabels[COCOLabels(class_id).name].value, cv2.FILLED)
        cv2.putText(input_image, text, (x_coord1, y_coord1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                    cv2.LINE_AA)
    def draw_rectangle(self, class_id, box, input_image):
        x_coord1, y_coord1, x_coord2, y_coord2 = [int(i) for i in box]
        colour = ColorLabels[COCOLabels(class_id).name].value
        cv2.rectangle(input_image, (x_coord1, y_coord1), (x_coord2, y_coord2), colour, 2)

    def main_operation(self, results1, frame):
        self.result1 = results1

        if self.result1.shape[1] == 7:
            self.result1[:, [0, 1, 2, 3, 4, 6]] = self.result1[:, [0, 1, 2, 3, 4, 6]].astype(int)

            # Add text & rectangle for all class
            for i in results1:

                self.add_text(class_id=i[-1],
                              track_id=i[4],
                              box=i[:4],
                              input_image=frame,
                              )
                self.draw_rectangle(class_id=i[-1], box=i[:4], input_image=frame)

        return frame


def process(video_path):
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    main_instance = Main(result1=None)
    cap = cv2.VideoCapture(video_path)
    frame_number = 0

    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                logging.info("Frame read failed, retrying...")
                cap.release()
                time.sleep(2)  # Wait a bit before trying to reconnect
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    logging.error("Error: Could not reopen video source.")
                    break
                continue

            # Reset frame read error count on successful read
            frame_number += 1
            if frame_number % 2 == 0:
                # Process the frame with YOLO
                results = model.track(frame, persist=True, conf=0.20)
                results1 = results[0].boxes.data.cpu().numpy()
                results1 = results1.astype(object)
                frame = main_instance.main_operation(results1, frame)
                cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
                cv2.imshow('Video', frame)

            # Press 'q' to exit the video loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            continue

    # Release the video capture object and close display windows
    if cap:
        cap.release()
    cv2.destroyAllWindows()
    logging.info("Video processing finished")


if __name__ == "__main__":
    model = YOLO("/home/nextbraingpu2/Music/PycharmProjects/pythonProject1/assets/weight/ppe.pt")
    video_path = "rtsp://admin:srivas123@192.168.1.22"  #rtsp://admin:srivas123@192.168.1.20
    process(video_path)
