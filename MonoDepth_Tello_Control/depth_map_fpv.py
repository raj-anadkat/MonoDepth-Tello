import keyboard_control as kb
from djitellopy import tello
import time
import torch
import cv2
import numpy as np



# MiDas Model
model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

#  The second line uses the PyTorch hub module to download and load the pre-trained MiDaS model
midas = torch.hub.load("intel-isl/MiDaS", model_type)

# Move model to GPU if available
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)
midas.eval()

# Load transforms to resize and normalize the image
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = midas_transforms.dpt_transform
else:
    transform = midas_transforms.small_transform

def depth_to_distance(depth):
    depths = round(100*(-1.6*depth + 2),2)
    return depths

# initializing
kb.init()
drone = tello.Tello()
drone.connect()
print("Battery:" ,drone.get_battery(),"%")
global img

#starting the video stream
drone.streamon()


def getKeyBoardInput():
    roll,pitch,throttle,yaw = 0,0,0,0
    velocity = 75

    # checking for roll commands
    if kb.getKey("LEFT"):roll = -velocity
    elif kb.getKey("RIGHT"):roll = velocity
    
    # checking for pitch commands
    if kb.getKey("UP"):pitch = velocity
    elif kb.getKey("DOWN"):pitch = -velocity

    # checking for throttle commands
    if kb.getKey("w"):throttle = velocity
    elif kb.getKey("s"):throttle = -velocity
    
    # checking for yaw commands
    if kb.getKey("a"):yaw = -velocity
    elif kb.getKey("d"):yaw = velocity

    # abort and land command
    if kb.getKey("x"):drone.land()

    # take off command
    if kb.getKey("t"):drone.takeoff()

    if kb.getKey('c'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg',img)
        time.sleep(0.3)
    return [roll,pitch,throttle,yaw]


while True:
    vals = getKeyBoardInput()
    drone.send_rc_control(vals[0],vals[1],vals[2],vals[3])
    print("Battery:" ,drone.get_battery(),"%")
    start = time.time()
    img = drone.get_frame_read().frame

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Apply input transforms
    input_batch = transform(img).to(device)

    # Prediction and resize to original resolution
    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    depth_map = prediction.cpu().numpy()

    depth_map = cv2.normalize(depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F)
    depth_point = depth_map[240,320]
    depths = depth_to_distance(depth_point)
    print("Depths: ", depths, " cm")

    end = time.time()
    totalTime = end - start

    fps = 1 / totalTime

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    depth_map = (depth_map*255).astype(np.uint8)
    depth_map = cv2.applyColorMap(depth_map , cv2.COLORMAP_MAGMA)

    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
    cv2.putText(depth_map, f'Dist(cm): {int(depths) }', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
    cv2.imshow('Image', img)
    cv2.imshow('Depth Map', depth_map)

    

    k = cv2.waitKey(30) & 0xff
    # cv2.imshow("FPV FEED",img)
    # k = cv2.waitKey(30) & 0xff
