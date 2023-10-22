import numpy as np
import cv2
import os
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def triangulateFunctionGraph(ax, XYZ, cmap=cm.magma):
    tri = Delaunay(XYZ[:, :2])
    ax.plot_trisurf(
        XYZ[:, 0], XYZ[:, 1], XYZ[:, 2],
        triangles=tri.simplices, cmap=cmap
    )


def readFaceImage(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    rows, cols = image.shape
    xyz = np.array([[x, y, float(image[y, x])] for y in range(rows) for x in range(cols)])
    return xyz


def triangulateFace(image_path):
    # Load the face image
    face_image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)

    # Load the face detection model (for example, Haar Cascade)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # Assuming the first detected face is the one you want to vectorize
        x, y, w, h = faces[0]

        # Crop the image to the region containing the detected face
        cropped_face = face_image[y:y + h, x:x + w]

        # Convert the cropped face to grayscale
        face_gray = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2GRAY)

        # Perform vectorization on the cropped grayscale image
        contours, _ = cv2.findContours(face_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create a list to store the vectorized paths
        vector_paths = []

        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            vector_paths.append(approx)

        # Now, you can perform triangulation or any other operation on vector_paths
        triangulateFunctionGraph(ax, vector_paths)
        plt.show()
    else:
        print("No face detected in the image.")


# Call triangulateFace function to perform vectorization and triangulation
triangulateFace(image_path='')
