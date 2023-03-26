# monoDepth_Tello
This repository has my ongoing work on Monocular SLAM on DJI Tello.
The implementation in this commit is a basic monocular depth estimation model MiDas v2.1 Small.
Currently working occupancy grids and performing motion planning using Disparity/ Follow the Gap where the approach is as follows:
1) Find the closest point in the Depth ranges array.
2) Draw a safety bubble around this closest point and set all points inside this bubble to 0. All other non-zero points are now considered “gaps” or “free space”.
3) Find the max length “gap”, in other words, the largest number of consecutive non-zero elements in your ranges array.
4) Find the best goal point in this gap.
