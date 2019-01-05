# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import csv
import os
import glob
from sys import platform
import numpy as np

# Remember to add your installation path here
# Option a
dir_path = os.path.dirname(os.path.realpath(__file__))
if platform == "win32": sys.path.append(dir_path + '/../../python/openpose/');
else: sys.path.append('../../python');
# Option b
# If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
# sys.path.append('/usr/local/python')

# Parameters for OpenPose. Take a look at C++ OpenPose example for meaning of components. Ensure all below are filled
try:
    from openpose import *
except:
    raise Exception('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
params = dict()
params["logging_level"] = 3
params["output_resolution"] = "-1x-1"
params["net_resolution"] = "160x80"
params["model_pose"] = "BODY_25"
params["alpha_pose"] = 0.6
params["scale_gap"] = 0.3
params["scale_number"] = 1
params["render_threshold"] = 0.05
# If GPU version is built, and multiple GPUs are available, set the ID here
params["num_gpu_start"] = 0
params["disable_blending"] = False
# Ensure you point to the correct path where models are located
params["default_model_folder"] = "/imatge/oorti/projects/openpose/models/"
# Construct OpenPose object allocates GPU memory
openpose = OpenPose(params)


# Define the codec
fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')

dataset_path = '/imatge/oorti/datasets/ASLLVD_small_AVI'
video_files = glob.glob(os.path.join(dataset_path, '*.avi'))

for video in video_files:
    # Read video
    out = cv2.VideoWriter('out/' + os.path.basename(video),fourcc, 25, (640, 480))

    with open('out/' + os.path.basename(video).split('.')[0] + '.csv', 'w') as csvfile:
        fieldnames = ['frame number', 'person', '0. Nose', '1. Neck', '2. RShoulder', '3. RElbow', 
                      '4. RWrist', '5. LShoulder', '6. LElbow', '7. LWrist', '8. MidHip', '9. RHip', '10. RKnee', 
                      '11. RAnkle', '12. LHip', '13. LKnee', '14. LAnkle', '15. REye', '16. LEye', '17. REar', '18. LEar', '19. LBigToe', 
                      '20. LSmallToe', '21. LHeel', '22. RBigToe', '23. RSmallToe', '24. RHeel']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        cap = cv2.VideoCapture(str(video))
        num_frame = 0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                # Output keypoints and the image with the human skeleton blended on it
                keypoints, output_frame = openpose.forward(frame, True)

                # Print the human pose keypoints, i.e., a [#people x #keypoints x 3]-dimensional numpy
                print(keypoints)
                # In ASLLVD videos there is a single person so we acces to the person in keypoints[0].
                points = keypoints[0]
                writer.writerow({'frame number': num_frame, 'person': 1, 
                  '0. Nose': points[0], '1. Neck': points[1], 
                  '2. RShoulder': points[2], '3. RElbow': points[3],
                  '4. RWrist': points[4], '5. LShoulder': points[5], 
                  '6. LElbow': points[6], '7. LWrist': points[7], '8. MidHip': points[8], 
                  '9. RHip': points[9], '10. RKnee': points[10],
                  '11. RAnkle': points[11], '12. LHip': points[12], '13. LKnee': points[13], 
                  '14. LAnkle': points[14], '15. REye': points[15], '16. LEye': points[16],
                  '17. REar': points[17], '18. LEar': points[18], '19. LBigToe': points[19],
                  '20. LSmallToe': points[20], '21. LHeel': points[21], '22. RBigToe': points[22], 
                  '23. RSmallToe': points[23], '24. RHeel': points[24]})

                # Save frame into video
                out.write(output_frame)
                num_frame += 1
            else:
                break

        # Release everything if job is finished
        cap.release()
        out.release()

