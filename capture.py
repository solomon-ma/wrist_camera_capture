import requests
from PIL import ImageTk, Image
import numpy as np
import io
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')

import cv2 
import os
import urx
rob = urx.Robot("192.168.12.3")

# cu_pos = rob.getl()
num = 0
move_step = 0.01
rot_step = 0.02

a = 0.15
v = 0.15

def mkdir(path):
    folder = os.path.exist(path)

    if not folder:
        os.mkdir(path)
        print("prepare to save robot position")



cv2.namedWindow('image')


while True:

    try:
        resp = requests.get("http://"+"192.168.12.3"+":4242/current.jpg?type=color").content
    except:
        pass

    #Check the response
    if resp == None:
        #If the response is empty display an error image
        pilImage=Image.open("error.jpg")
        tkImage = ImageTk.PhotoImage(pilImage)
    else:
        #If the response is not empty format the data to get a
        #tkinter format image
        imageData = np.asarray(bytearray(resp), dtype="uint8")
        pilImage=Image.open(io.BytesIO(imageData))
        # pilImage = pilImage.save("test.jpeg")
        # tkImage = ImageTk.PhotoImage(pilImage)
    # 等待按键事件发生

    key_code = cv2.waitKey(1)

    if key_code != -1:
        print('key {} pressed!!! value={}'.format(chr(key_code), key_code))
        if key_code == 27:
            # 退出程序
            cv2.destroyWindow('image')
            print('Quit')
            break
        elif chr(key_code) == "c":
            cur_pos = rob.getl()
            with open("./capture_data/rob_pos.txt","a") as file:
                file.write(str(num) + "\t")
                file.write(str(cur_pos) + "\n")
            pilImage = pilImage.save("./capture_data/" + str(num) + ".jpeg")
            num = num + 1
        elif chr(key_code) == "w":
            cur_pos = rob.getl()
            print(cur_pos)
            rob.movel((cur_pos[0], cur_pos[1], cur_pos[2] + move_step, cur_pos[3], cur_pos[4], cur_pos[5]), a, v)
        elif chr(key_code) == "s":
            cur_pos = rob.getl()
            rob.movel((cur_pos[0], cur_pos[1], cur_pos[2] - move_step, cur_pos[3], cur_pos[4], cur_pos[5]), a, v)
        elif chr(key_code) == "a":
            cur_pos = rob.getl()
            rob.movel((cur_pos[0], cur_pos[1] + move_step, cur_pos[2], cur_pos[3], cur_pos[4], cur_pos[5]), a, v)
        elif chr(key_code) == "d":
            cur_pos = rob.getl()
            rob.movel((cur_pos[0], cur_pos[1]- move_step, cur_pos[2] , cur_pos[3], cur_pos[4], cur_pos[5]), a, v)
        elif chr(key_code) == "r":
            cur_pos = rob.getl()
            rob.movel((cur_pos[0], cur_pos[1], cur_pos[2] , cur_pos[3] + rot_step, cur_pos[4], cur_pos[5]), a, v)
        elif chr(key_code) == "q":
            cur_pos = rob.getl()
            rob.movel((cur_pos[0], cur_pos[1], cur_pos[2] , cur_pos[3] - rot_step, cur_pos[4], cur_pos[5]), a, v)


    else:
        # 没有按键按下
        open_cv_image = np.array(pilImage) 
        # Convert RGB to BGR 
        open_cv_image = open_cv_image[:, :, ::-1].copy() 
        cv2.imshow('image', open_cv_image)
        # print('no key pressed , wait 1s')


cv2.destroyWindow('image')