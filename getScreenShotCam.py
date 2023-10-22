import cv2
import torch
import os
import time
import shutil
import FaceDatabase.FaceTriangulate

# Load YOLOv5 model (you need to have YOLOv5 and its dependencies installed)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # You can choose a different YOLOv5 variant (e.g., 'yolov5m', 'yolov5l', 'yolov5x')

# Set the confidence threshold
confidence_threshold = 0.7

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use the appropriate camera index

# Create the "SessionCapture" folder if it doesn't exist
if not os.path.exists("SessionCapture"):
    os.makedirs("SessionCapture")

# Flag to track if a screenshot has been taken
screenshot_taken = False

# List to store the images of detected people
person_images = []

while True:
    ret, frame = cap.read()  # Capture a frame
    if not ret:
        break

    # Perform YOLOv5 inference on the frame
    results = model(frame)

    # Check if any person is detected with confidence > 0.7
    for pred in results.pred[0]:
        if not screenshot_taken and pred[4] > confidence_threshold and pred[5] == 0:  # Class 0 represents a person
            screenshot_taken = True

            # OpenCV's YOLOv5 model returns detected persons as a list of bounding boxes
            # You can iterate through the bounding boxes and save each person as a separate image
            for person_bbox in results.xyxy[0]:
                if person_bbox[4] > confidence_threshold and person_bbox[5] == 0:
                    x1, y1, x2, y2 = person_bbox[:4].int()
                    person_image = frame[y1:y2, x1:x2]
                    person_images.append(person_image)

                    # Add print statements for debugging
                    person_file_path = os.path.join("SessionCapture", f"person_{len(person_images)}.jpg")
                    cv2.imwrite(person_file_path, person_image)
                    print(f"Saved person image: {person_image.shape} at {person_file_path}")

            # You can add additional logic here, like saving the timestamp or notifying someone
            print("Person detected with confidence > 0.7. Images saved.")

    # Display the frame
    cv2.imshow('Camera Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
