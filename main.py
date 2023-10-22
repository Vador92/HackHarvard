import subprocess
import schedule
import time
import os
import FaceDatabase.FaceTriangulate

def job():
    FaceDatabase.FaceTriangulate.triangulateFace()


def main():
    script_name = "getScreenShotCam.py"  # Replace with the actual script filename
    process = subprocess.Popen(["python", script_name], shell=True)

    # Delete all files in the "SessionCapture" folder at the start
    session_capture_folder = "SessionCapture"
    for filename in os.listdir(session_capture_folder):
        file_path = os.path.join(session_capture_folder, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Schedule the 'job' function to run every 60 seconds
    schedule.every(60).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
