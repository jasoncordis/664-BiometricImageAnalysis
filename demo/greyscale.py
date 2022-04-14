import numpy as np
import cv2
import sys
import collections

from skimage import data
from skimage.filters import try_all_threshold
from skimage import io
from skimage.filters import threshold_minimum
from skimage.util import img_as_ubyte

import math

def greyscale_heads(filename):

    thresh = io.imread(filename)

    thresh_min = threshold_minimum(thresh)
    binary_min = thresh > thresh_min

    image_min = img_as_ubyte(binary_min)

    io.imsave('min.png', image_min)
    
    # Reading image
    font = cv2.FONT_HERSHEY_COMPLEX
    img3 = cv2.imread('min.png', cv2.IMREAD_COLOR)
    img2 = cv2.imread(filename, cv2.IMREAD_COLOR)

    # Reading same image in another 
    # variable and converting to gray scale.
    img = cv2.imread('min.png', cv2.IMREAD_GRAYSCALE)
    img = cv2.bitwise_not(img)
    # Converting image to a binary image
    # ( black and white only image).
    _, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)
      
    # Detecting contours in image.
    contours, _= cv2.findContours(threshold, cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
      
    # Going through every contours found in the image.

    eyes = []
    bodies = []

    a = 0

    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        str1 = 'width', w, 'height', h
        if(w > 1 and h > 1 and w <= 4 and h <= 4):
            print('eye found')
            eyes.append(a)
        else:
            bodies.append(a)
        a = a + 1

    validEye = 0

    eyePairs = []

    eyeCoordsX = []
    eyeCoordsY = []

    diagonal = 0

    overlaps = []


    regularBodies = []

    bodiesCoordsX = []
    bodiesCoordsY = []

    body = 0

    for b in bodies:
        bodyCoordsX = []
        bodyCoordsY = []
        
        cnt = contours[b]
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        print('body x')
        n = approx.ravel()
        for a in range(0, len(n), 2):
            print(n[a])
            bodyCoordsX.append(n[a])
        print('body y')
        for b in range(1, len(n), 2):
            print(n[b])
            bodyCoordsY.append(n[b])

        for i in bodyCoordsX:
            print(i, bodyCoordsX.count(i))
            if(bodyCoordsX.count(i) >= 4):
                diagonal = 1
                
        for i in bodyCoordsY:
            print(i, bodyCoordsY.count(i))
            if(bodyCoordsY.count(i) >= 4):
                diagonal = 1

        bodiesCoordsX.append(bodyCoordsX)
        bodiesCoordsY.append(bodyCoordsY)

        if(diagonal == 1):
            print('diagonal')
            #cv2.drawContours(img2, [approx], 0, (255, 0, 255), 1)
            overlaps.append(body)
        else:
            #cv2.drawContours(img2, [approx], 0, (255, 255, 255), 1)
            regularBodies.append(body)

        diagonal = 0
        body = body+1

    for i in eyes:
        cnt = contours[i]
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        #cv2.drawContours(img2, [approx], 0, (0, 255, 0), 1) 


        eyeX = []
        eyeY = []

        n = approx.ravel()
        for a in range(0, len(n), 2):
            eyeX.append(n[a])

        for b in range(1, len(n), 2):
            eyeY.append(n[b])

        eyeCoordsX.append(eyeX)
        eyeCoordsY.append(eyeY)
            
        print('eye')


    for x in eyeCoordsX:
        print(x)
    for y in eyeCoordsY:
        print(y)


    x_dist = sys.maxsize
    y_dist = sys.maxsize

    for i in range(0, len(eyes)-1):
        for a in range(i+1, len(eyes)):
            for n in eyeCoordsX[i]:
                for b in eyeCoordsX[a]:
                    if(abs(n - b) <= 3):
                        x_dist = abs(n-b)
                        #print('eye', i, 'and eye', a, 'at x', n, b)
                        break
            for n in eyeCoordsY[i]:
                for b in eyeCoordsY[a]:
                    if(abs(n - b) <= 3):
                        y_dist = abs(n-b)
                        #print('eye', i, 'and eye', a, 'at 6', n, b)
                        break
            if(x_dist <= 3 and y_dist <= 3):
                print('eyes', i, 'and', a, 'are valid')
                eyePairs.append(i)
                eyePairs.append(a)
            x_dist = sys.maxsize
            y_dist = sys.maxsize


    #for i in eyePairs:
        #print(i)

    for i in range(0, len(eyePairs), 2):
        eye1 = eyePairs[i]
        eye2 = eyePairs[i+1]

        eye1_x = 0
        eye2_x = 0

        if(max(eyeCoordsX[eye1]) > max(eyeCoordsX[eye2])):
             eye1_x = min(eyeCoordsX[eye1])
             eye2_x = max(eyeCoordsX[eye2])
        else:
             eye1_x = max(eyeCoordsX[eye1])
             eye2_x = min(eyeCoordsX[eye2])

        eye1_y = 0
        eye2_y = 0

        if(max(eyeCoordsY[eye1]) > max(eyeCoordsY[eye2])):
             eye1_y = min(eyeCoordsY[eye1])
             eye2_y = max(eyeCoordsY[eye2])
        else:
             eye1_y = max(eyeCoordsY[eye1])
             eye2_y = min(eyeCoordsY[eye2])


        eye_middleX = int((eye1_x+eye2_x)/2)
        eye_middleY = int((eye1_y+eye2_y)/2)

        min_distX = sys.maxsize
        min_distY = sys.maxsize

        closestBody = -1

        for b in range(0, len(bodies)):
            for x in range(0, len(bodiesCoordsX[b])):
                if((abs(bodiesCoordsX[b][x]-eye_middleX) + abs(bodiesCoordsY[b][x]-eye_middleY)) < (min_distX + min_distY)):
                    min_distX = abs(bodiesCoordsX[b][x]-eye_middleX)
                    min_distY = abs(bodiesCoordsY[b][x]-eye_middleY)
                    closestBody = b

        if(closestBody != -1):
            closestBodyX_max = max(bodiesCoordsX[closestBody])
            closestBodyY_max = max(bodiesCoordsY[closestBody])
            closestBodyX_min = min(bodiesCoordsX[closestBody])
            closestBodyY_min = min(bodiesCoordsY[closestBody])

            if(closestBodyY_min < eye_middleY and closestBodyY_max > eye_middleY and closestBodyX_min < eye_middleX and closestBodyX_max > eye_middleX):
                    eye_middleY = eye_middleY + 1
            else:
                if(abs(closestBodyY_min - eye_middleY) > 3):
                        if(closestBodyY_max > eye_middleY):
                                eye_middleY = eye_middleY + 2
                        else:
                            if(abs(closestBodyY_min - eye_middleY) > 8):
                                    eye_middleY = eye_middleY - 2
                            else: 
                                    eye_middleY = eye_middleY - 1                
                                
                elif(abs(closestBodyY_max - eye_middleY) > 3):
                    if(closestBodyY_max > eye_middleY):
                        eye_middleY = eye_middleY + 2
                    else:
                        eye_middleY = eye_middleY - 2

            if(abs(closestBodyX_max - eye_middleX) > 3):
                if(closestBodyX_max > eye_middleX):
                    eye_middleX = eye_middleX + 1
                else:
                    eye_middleX = eye_middleX - 1

            elif(abs(closestBodyX_min - eye_middleX) > 3):
                if(closestBodyX_max > eye_middleX):
                        eye_middleX = eye_middleX + 1
                else:
                        eye_middleX = eye_middleX - 1

        # Center coordinates
        center_coordinates = (eye_middleX , eye_middleY )
         
        # Radius of circle
        radius = 1
          
        # Blue color in BGR
        color = (0, 0, 255)
          
        # Line thickness of 2 px
        thickness = 1
          
        # Using cv2.circle() method
        # Draw a circle with blue line borders of thickness of 2 px
        cv2.circle(img2, center_coordinates, radius, color, thickness)
        img2[eye_middleY,eye_middleX] = [0, 0, 255]



    print('paired')
    for b in eyePairs:
        print(b)

    unpaired = []

    for p in range(0, len(eyes)):
        if(p not in eyePairs):
            unpaired.append(p)

    print('unpaired')
    for p in unpaired:
        print(p)


    if(len(unpaired)>1):

        x_dist = 0
        y_dist = 0

        print('len bodies', len(bodies))

        print('overlaps')

        for i in overlaps:
            print(i)

            
        for i in overlaps:
            for a in regularBodies:
                for n in bodiesCoordsX[i]:
                    for b in bodiesCoordsX[a]:
                        if(abs(n - b) <= 4):
                            x_dist = abs(n-b)
                            #print('eye', i, 'and eye', a, 'at x', n, b)
                            break
                for n in bodiesCoordsY[i]:
                    for b in bodiesCoordsY[a]:
                        if(abs(n - b) <= 4):
                            y_dist = abs(n-b)
                            #print('eye', i, 'and eye', a, 'at 6', n, b)
                            break
                if(x_dist <= 4 and y_dist <= 4):
                    print('eyes', i, 'and', a, 'are valid')
                    overlap1_x = min(bodiesCoordsX[i])
                    overlap2_x = max(bodiesCoordsX[i])
                    overlap_midX = int((overlap1_x + overlap2_x)/2)
                    overlap1_y = min(bodiesCoordsY[i])
                    overlap2_y = max(bodiesCoordsY[i])
                    overlap_midY = int((overlap1_y + overlap2_y)/2)
                    #cv2.rectangle(img2, (overlap_midX+1, overlap_midY+1),(overlap_midX-1, overlap_midY-1), (128,0,255), 1)
                    # Center coordinates
                    center_coordinates = (overlap_midX , overlap_midY )
                    # Radius of circle
                    radius = 1
                    # Blue color in BGR
                    color = (0, 0, 255)
                    # Line thickness of 2 px
                    thickness = 1

                    noEye = 0

                    for p in eyePairs:
                        if((abs(max(eyeCoordsX[p]) - min(bodiesCoordsX[i])) <= 10) and (abs(max(eyeCoordsY[p]) - min(bodiesCoordsY[i])) <= 10)):
                            noEye = noEye + 1

                    if(noEye < 1):
                        cv2.circle(img2, center_coordinates, radius, color, thickness)
                        img2[overlap_midY,overlap_midX] = [0, 0, 255]
                x_dist = sys.maxsize
                y_dist = sys.maxsize

        for i in overlaps:
            for p in unpaired:
                x_dist = sys.maxsize
                y_dist = sys.maxsize
                for n in bodiesCoordsX[i]:
                    for b in eyeCoordsX[p]:
                        if(abs(n - b) <= 2):
                            x_dist = abs(n-b)
                            print('eye', i, 'and eye', a, 'at x', n, b)
                            break
                for n in bodiesCoordsY[i]:
                    for b in eyeCoordsY[p]:
                        if(abs(n - b) <= 2):
                            y_dist = abs(n-b)
                            print('eye', i, 'and eye', a, 'at 6', n, b)
                            break
                if(x_dist <= 2 and y_dist <= 2):
                    print('OVERLAP EYES')
                    overlapEye1_x = min(bodiesCoordsX[i])
                    overlapEye2_x = max(bodiesCoordsX[i])
                    overlapEye3_x = min(eyeCoordsX[p])
                    overlapEye4_x = max(eyeCoordsX[p])

                    overlapEye1_y = min(bodiesCoordsY[i])
                    overlapEye2_y = max(bodiesCoordsY[i])
                    overlapEye3_y = min(eyeCoordsY[p])
                    overlapEye4_y = max(eyeCoordsY[p])

                    overlapEye_midX = 0
                    overlapEye_midY = 0

                    overlapEyeY = []

                    if((abs(overlapEye1_x - overlapEye3_x) < 2) or abs(overlapEye2_x-overlapEye4_x) < 2):
                        overlapEye_midX = int((overlapEye3_x + overlapEye4_x)/2)
                        #print('eye x', overlapEye4_x, overlapEye3_x)
                        #print('eye y', overlapEye4_y, overlapEye3_y)
                        #print('body x', overlapEye1_x, overlapEye2_x)
                        #print('body y', overlapEye1_y, overlapEye2_y)
                        if((overlapEye4_x - overlapEye3_x)%2==1):
                            #print('hello')
                            overlapEye_midX = overlapEye_midX + 1

                        if(overlapEye4_y > overlapEye2_y):
                            print('overlap eye', overlapEye2_y, overlapEye4_y)
                            overlapEye_midY = int((overlapEye3_y + overlapEye2_y)/2)
                            # Center coordinates
                            center_coordinates = (overlapEye_midX , overlapEye_midY)
                            # Radius of circle
                            radius = 1
                            # Blue color in BGR
                            color = (0, 0, 255)
                            # Line thickness of 2 px
                            thickness = 1
                            cv2.circle(img2, center_coordinates, radius, color, thickness)
                            img2[overlapEye_midY,overlapEye_midX] = [0, 0, 255]
                            #img2 = cv2.rectangle(img2, (overlapEye_midX+1, overlapEye_midY+1),(overlapEye_midX-1, overlapEye_midY-1), (153,153,0), 1)

                        else:
                            #print('brooo')
                            overlapEye_midY = int((overlapEye3_y + overlapEye2_y)/2) - 2
                            # Center coordinates
                            center_coordinates = (overlapEye_midX , overlapEye_midY )
                            # Radius of circle
                            radius = 1
                            # Blue color in BGR
                            color = (0, 0, 255)
                            # Line thickness of 2 px
                            thickness = 1
                            cv2.circle(img2, center_coordinates, radius, color, thickness)
                            img2[overlapEye_midY,overlapEye_midX] = [0, 0, 255]
                            #img2 = cv2.rectangle(img2, (overlapEye_midX+1, overlapEye_midY+1),(overlapEye_midX-1, overlapEye_midY-1), (153,153,0), 1)
        
                    x_dist = sys.maxsize
                    y_dist = sys.maxsize

    # Showing the final image.
    cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)
      
    # Using resizeWindow()
    cv2.resizeWindow("Resized_Window", 800, 800)
      
    # Displaying the image
    cv2.imshow("Resized_Window", img2)
      
    # Exiting the window if 'q' is pressed on the keyboard.
    if cv2.waitKey(0) & 0xFF == ord('q'): 
        cv2.destroyAllWindows()
