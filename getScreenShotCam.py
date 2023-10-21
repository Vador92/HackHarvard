import cv2
import torch
import shutil


# Load YOLOv5 model (you need to have YOLOv5 and its dependencies installed)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # You can choose a different YOLOv5 variant (e.g., 'yolov5m', 'yolov5l', 'yolov5x')

# Set the confidence threshold
confidence_threshold = 0.7

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use the appropriate camera index

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
            destination_folder = "SessionCapture"

            # Use shutil.move to move the file to the destination folder
            shutil.move(screenshot_file_path, destination_folder)

            # Print the file path
            print(f"File Path of the Screenshot: {screenshot_file_path}")

            # You can add additional logic here, like saving the timestamp or notifying someone
            print("Person detected with confidence > 0.7. Screenshot taken.")

    # Display the frame
    cv2.imshow('Camera Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# The file path has been printed, and you can use 'screenshot_file_path' for any later purpose
#using this file path we feed it into a server api call