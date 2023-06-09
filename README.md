# monoDepth_Tello
This repository has my ongoing work on Monocular SLAM on DJI Tello.
The implementation in this commit is a basic monocular depth estimation model MiDas v2.1 Small.
Currently working occupancy grids and performing motion planning using Disparity/ Follow the Gap where the approach is as follows:
1) Find the closest point in the Depth ranges array.
2) Draw a safety bubble around this closest point and set all points inside this bubble to 0. All other non-zero points are now considered “gaps” or “free space”.
3) Find the max length “gap”, in other words, the largest number of consecutive non-zero elements in your ranges array.
4) Find the best goal point in this gap.

MonoDepth Results:

Original Image vs Depth Map Distance
![comp](https://user-images.githubusercontent.com/109377585/227813864-d4fd1942-4e2c-4494-b345-55e3040b66a1.jpg)
Third Person
![fpv_tello](https://user-images.githubusercontent.com/109377585/227813649-eae86c04-19d6-4372-896c-4df835557deb.jpg)


Comparison with Intel Realsense RGBD maps
![mono_realsense](https://user-images.githubusercontent.com/109377585/231362740-ccefdbf1-0782-4083-9709-1815b1f1e00e.jpg)

