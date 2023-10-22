import cv2
import torch
import os
import time
import shutil

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

            # Take a screenshot of the frame
            cv2.imwrite("screenshot.jpg", frame)

            # Store the file path for later use
            screenshot_file_path = "screenshot.jpg"

            # OpenCV's YOLOv5 model returns detected persons as a list of bounding boxes
            # You can iterate through the bounding boxes and save each person as a separate image
            person_count = 0
            for person_bbox in results.xyxy[0]:
                if person_bbox[4] > confidence_threshold and person_bbox[5] == 0:
                    x1, y1, x2, y2 = person_bbox[:4].int()
                    person_image = frame[y1:y2, x1:x2]
                    person_file_path = os.path.join("SessionCapture", f"person_{person_count}.jpg")
                    cv2.imwrite(person_file_path, person_image)
                    person_count += 1

            # Print the file path of the main screenshot
            print(f"File Path of the Main Screenshot: {screenshot_file_path}")

            # Move the person images to the SessionCapture folder
            for i in range(person_count):
                person_image_path = os.path.join("SessionCapture", f"person_{i}.jpg")
                shutil.move(person_image_path, "SessionCapture")
                print(i)

            # You can add additional logic here, like saving the timestamp or notifying someone
            print("Person detected with confidence > 0.7. Screenshot taken.")

    # Display the frame
    cv2.imshow('Camera Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
