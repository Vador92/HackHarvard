#https://nseverkar.medium.com/triangulation-with-python-680227ff6a69

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
    tri = Delaunay(XYZ[:,:2])
    ax.plot_trisurf(
        XYZ[:,0], XYZ[:,1], XYZ[:,2],
        triangles=tri.simplices, cmap=cmap
    )

def readFaceImage(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    rows, cols = image.shape
    xyz = np.array([[x, y, float(image[y, x])] for y in range(rows) for x in range(cols)])
    return xyz

def triangulateFace():
    folder_path = "SessionCapture"  # Replace with the actual folder path
    files = os.listdir(folder_path)

    if "screenshot.jpg" in files:
        print("The folder is not empty.")
        # Assuming the face image filename is 'screenshot.jpg'
        face_image_filename = "screenshot.jpg"
        face_image_path = os.path.join(folder_path, face_image_filename)
        xyz = readFaceImage(face_image_path)
        triangulateFunctionGraph(ax, xyz)
        plt.show()
    else:
        print("Face image not found in the folder.")

# Call your triangulateFace function to perform the triangulation
triangulateFace()
