# monoDepth_Tello
This repository has my ongoing work on Monocular SLAM on DJI Tello.
The implementation in this commit is a basic monocular depth estimation model MiDas v2.1 Small.
Currently working occupancy grids and performing motion planning using Disparity/ Follow the Gap where the approach is as follows:
1) Find the closest point in the Depth ranges array.
2) Draw a safety bubble around this closest point and set all points inside this bubble to 0. All other non-zero points are now considered “gaps” or “free space”.
3) Find the max length “gap”, in other words, the largest number of consecutive non-zero elements in your ranges array.
4) Find the best goal point in this gap.

MonoDepth Results:

Depth Map and Distance:
![results](https://user-images.githubusercontent.com/109377585/227763711-054c9771-5af3-4a1a-8345-712609dc05ef.png)


Occupancy Grid (Range based)
![occupancy_grid](https://user-images.githubusercontent.com/109377585/227763715-157e356e-473a-4ee3-ad96-2167e4ae62b6.png)
