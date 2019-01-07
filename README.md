# OpenPose scripts

## Description
This repository contains some python scripts to perform 
**human pose estimation** using the 
[OpenPose API](https://github.com/CMU-Perceptual-Computing-Lab/openpose).

The main objective of this project is to estimate the pose of people talking in
sign language to train an action recognition system able to understand the 
american sign language.

The ASLLVD dataset have been used generate the annotations.

## Requirements (GPU)

- OpenPose v.1.4.0
- CuDNN v.5.1
- OpenCV v.4.3.1

### Setup for Image Processing Group (GPI) GPU servers

Load modules: 
`module load opencv/3.4.1 cudnn/v5.1 boost/1.66 openpose/1.4.0`

## Contents

* `extract_pose_from_image.py`
The script takes the example image and estimate the pose of the people on it. 
The output of the script is an image with the estimated skeletons.
**CAVEAT**: The path to the example image and output are hardcoded.

* `extract_pose_from_video.py`
The script takes the example video and estimate the pose of the people on it. 
The output of the script is an video with the estimated skeletons.
**CAVEAT**: The path to the example video and output are hardcoded.

* `generate_dataset.py`
The script takes the example video and estimate the pose of the people on it. 
The output of the script is an video with the estimated skeletons and a CSV 
with the keypoints of each video.
**CAVEAT**: The path to the dataset and output are hardcoded.

## Annotations format

Each annotation file (csv) is structured as follows:

| Frame Number | Person ID | Keypoint 0   | ... | Keypoint 24  |
|--------------|-----------|--------------|-----|--------------|
| 0            | 1         | [x, y, c]    | ... | [x, y, c]    |
| 1            | 1         | [x, y, c]    | ... | [x, y, c]    |
|              |           |              |     |              |

Where `x` and `y` are the pixel height and width of the keypoint. 
`c` is the confidence of the prediction. For further information see 
[OpenPose output documentation](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md#keypoint-ordering).

## Tips for developing

1. The used version of OpenCV does not have a video codec for 
   `*.mov` video format. So it is
   convenient to convert the videos to `*.avi` format in order to use 
   the specified video codec. 
   To convert all videos from `*.mov` to `*.avi` use the following command:
   `for i in *.avi; do ffmpeg -i "$i" "${i%.*}.mp4"; done`
   If you want to work with other video formats see the `ffmpeg` man
   page and the available OpenCV video codecs

## Future work

1. The version 1.4.0 of the OpenPose Python API is not compatible 
   with the hands and face models.
   To be able to use that models it is necessary to add them into the
   python wrapper, which is writed in cpp. There are work on it, like
   [This commit](https://github.com/CMU-Perceptual-Computing-Lab/openpose/commit/21eac3784c608a8b25162cae058cfb526f4cd673)
   that adds the hand model to the wrapper.

