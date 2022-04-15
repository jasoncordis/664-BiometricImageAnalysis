from skimage import data, filters
import cv2
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys


currentPos = []
potentialHead = []

potentialHeadCoord = []

fish = []

head = []

intersections = []
connect = []
potentialFish = []

zeroArray = []

discont = []


def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):

    dim = None
    (h, w) = image.shape[:2]


    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized


def find_verticals1(arr, countX, img2):
    if(arr):
        arr.sort()
        counter = arr[0]
        vertical = 0
        verticalSize = 0
        currConnection = -1
        currNum = 0
        removed = -1
        possibleDiagonal = 0
        reset = 0

        #vertical up in last 10, vertical down in last 10,
        #consistent for 10 pixels
        #start head bounds, x and 2 y-values
        #end head bounds, x and 2 y-values

        for p in potentialHead:
            p[7] = p[7] + 1


        if(len(intersections)>0):
            intersect = 0
            intersectFishBoundaryFound = 0
            intersectFishBoundary = 0
            intersectY = 0
            
            for num in arr:
                    for i in intersections:
                        #print('fishboundary', i[1], 'num', num)
                        intersectFishBoundary = i[1]
                        #print('intersectFishBoundary', intersectFishBoundary)
                        if(abs(i[1] - num) <= 1):
                            intersectFishBoundaryFound = 1
                            intersectFishBoundary = i[1]
                            #print('fishboundary', intersectFishBoundary)
                        if(abs(i[0] - num) <= 1):
                           intersect = 1
                           i[2] = -1
                        else:
                            intersectY = i[0]

                        if(i[2] == -1):
                            intersect = 1

            if(intersect == 0):
                img2 = cv2.rectangle(img2, (countX , intersectY ), (countX+1, intersectY ), (255,0,255), 10)
                
            if(intersectFishBoundaryFound == 0):
                img2 = cv2.rectangle(img2, (countX , intersectFishBoundary), (countX+1, intersectFishBoundary), (255,0,255), 10)
            
        
        for num in arr:
            #print(num)
            currNum = num
               
            if(reset):
                counter = num

            for p in potentialHead:
                p[0] = p[0] + 1
                p[1] = p[1] + 1
            #print('verticalSize', verticalSize)
            #print('count num', counter, num)
            
            for q in connect:
                if(num == q):
                    #print('connection found at', num)

                    if(counter != num):
                        for c in connect:
                            if(abs((counter - 1) - c) <= 1):
                                #print('update connection to ', counter - 1)
                                for f in fish:
                                    if(f[0] == c):
                                        f[0] = counter - 1
                                    if(f[1] == c):
                                        f[1] = counter - 1
                                connect.remove(c)
                                connect.append(counter-1)
                    
                    foundConnection = 1
                    currConnection = num
                    if(vertical == 1 and verticalSize <= 1):
                        verticalSize = 0
                        vertical = 0
                    elif(vertical == 1 and verticalSize > 1 and num == counter):
                        verticalSize = verticalSize + 1
                        #print('vertical up', verticalSize)
                        for connect1 in connect:
                            if(abs(num-verticalSize-connect1) <=1):
                                print('INTERSECTION', num-verticalSize)
                                intersectValue = num-verticalSize
                                alreadyIntersected = 0
                                for i in intersections:
                                    if((abs(i[0] - intersectValue)) <= 1):
                                       alreadyIntersected = 1

                                if(alreadyIntersected == 0):
                                    intersectFish = 0
                                    intersectBoundary = 0
                                    for f in fish:
                                        print(f)
                                        print(abs(f[0] - intersectValue))
                                        print(abs(f[1] - intersectValue))
                                        if(abs(f[0] - intersectValue) <= 1):
                                            intersectFish = 1
                                            intersectBoundary = f[1]
                                        elif(abs(f[1] - intersectValue) <= 1):
                                            intersectFish = 1
                                            intersectBoundary = f[0]

                                    if(intersectFish == 1):
                                        #print('intersection confirmed')
                                        intersections.append([num-verticalSize, intersectBoundary, 0])
                        
                        removed = num
                        #print('we remove', num)
                        for f in fish:
                            if(f[0] == num):
                                f[0] = num-verticalSize
                            if(f[1] == num):
                                f[1] = num-verticalSize
                        connect.remove(num)
                        connect.append(num-verticalSize)
                        #print('new point:', num-verticalSize)
                        vertical = 0
                        verticalSize = 0
                        currConnection = -1
                    elif(vertical == 1 and verticalSize > 1 and num != counter):
                        verticalSize = verticalSize - 1
                        potentialHead[-1][1] = 0

                        if (((potentialHead[-1][5] - (counter - 1)) <= 1) or ((counter - 1)-potentialHead[-1][5] <=1)): 
                            print('head found111')
                            middleX = potentialHead[-1][7]/2
                            middleX = countX - middleX
                            middleY = potentialHead[-1][5] - potentialHead[-1][4]
                            middleY = middleY/2
                            middleY = potentialHead[-1][4] + middleY

                            middleX1 = int(round(middleX)) + 5
                            middleX2 = int(round(middleX)) - 5

                            middleY1 = int(round(middleY)) + 5
                            middleY2 = int(round(middleY)) - 5

                            #print('test', middleX1, middleX2, middleY1, middleY2)

                            if(potentialHead[-1][7] > 30 and fish[0][2] != 1):
                                img2 = cv2.rectangle(img2, (middleX1, middleY1), (middleX2, middleY2), (0,0,255), 10)
                                #cv2.imshow('image3', img2)
                                fish[0][2] = 1
                                           
                        #print('vertical down111asdf', verticalSize)

                        #print('counter', counter)
                        #print('verticalSize', verticalSize)
                        #print('num', num)
                        #print('currConnection', currConnection)

                        #print('currConnection - verticalSize', currConnection-verticalSize)
                        #print('currConnection - verticalSize - counter', abs(currConnection - verticalSize - counter))
                        
                        if((abs(currConnection - verticalSize - counter)) >= 7):
                            print('vertical line actually')
                            print('new line at 111111', counter - 1, 'and', counter - verticalSize)
                            connect.append(counter - 1)
                            connect.append(counter - verticalSize - 1)
                            arr2 = [counter, counter - verticalSize - 1, countX]
                            potentialFish.append(arr2)
                            counter = num + 1
                            vertical = 0
                            verticalSize = 0
                            reset = 1
                        else:
                            for f in fish:
                                if(f[0] == currConnection):
                                    f[0] = counter - 1
                                if(f[1] == currConnection):
                                    f[1] = counter - 1
                            connect.remove(currConnection)
                            removed = currConnection
                            connect.append(counter - 1)
                            vertical = 0
                            verticalSize = 0
                            currConnection = -1
                            reset = 0

                        
                        #print('potential head', q)
                        if(potentialHead[-1][1] - potentialHead[-1][0] < 60):
                            potentialHead[-1][4] = q
                            potentialHead[-1][7] = 0

                        
            if(counter == num):
                vertical = 1
                counter = counter + 1
                verticalSize = verticalSize+1
            elif(counter != num):
                if(vertical == 1 and verticalSize > 1 and currConnection == -1):
                    #print('new line at 111111', counter - 1, 'and', counter - verticalSize)
                    connect.append(counter)
                    connect.append(counter - verticalSize - 1)
                    arr2 = [counter, counter - verticalSize - 1, countX]
                    potentialFish.append(arr2)
                    counter = num + 1
                    vertical = 0
                    verticalSize = 0
                    reset = 1

                    
                    
                elif(vertical == 1 and verticalSize > 1):
                    potentialHead[-1][1] = 0
                    #print('vertical down', verticalSize)
                    #print('potential head', q)

                    if (((potentialHead[-1][5] - (counter - 1)) <= 1) or ((counter - 1)-potentialHead[-1][5] <=1)): 
                            #print('head found')
                            middleX = potentialHead[-1][7]/2
                            middleX = countX - middleX
                            middleY = potentialHead[-1][5] - potentialHead[-1][4]
                            middleY = middleY/2
                            middleY = potentialHead[-1][4] + middleY

                            middleX1 = int(round(middleX)) + 5
                            middleX2 = int(round(middleX)) - 5

                            middleY1 = int(round(middleY)) + 5
                            middleY2 = int(round(middleY)) - 5

                            #print('test', middleX1, middleX2, middleY1, middleY2)
                            
                            #img2 = cv2.imread(filename)
                            #img2 = cv2.rectangle(img2, (middleX1, middleY1), (middleX2, middleY2), (0,0,255), 10)
                            #cv2.imshow('image3', img2) 
                    
                    if(potentialHead[-1][1] - potentialHead[-1][0] < 60):
                        potentialHead[-1][4] = q
                        potentialHead[-1][7] = 0


                    for f in fish:
                        if(f[0] == currConnection):
                            f[0] = counter
                        if(f[1] == currConnection):
                            f[1] = counter       
                    connect.remove(currConnection)
                    removed = currConnection
                    connect.append(counter)
                    vertical = 0
                    verticalSize = 0
                    currConnection = -1
                    reset = 1
                else:
                   for q in connect:
                       if(num + 1 == q):
                           for f in fish:
                               if(f[0] == q):
                                   f[0] = num
                               if(f[1] == q):
                                   f[1] = num
                                
                           connect.remove(q)
                           connect.append(num)
                           #print('connection found at', num)
                           foundConnection = 1
                           currConnection = num

                       elif(num - 1 == q):
                           for f in fish:
                               if(f[0] == q):
                                   f[0] = num
                               if(f[1] == q):
                                   f[1] = num
                        
                           connect.remove(q)
                           connect.append(num)
                           #print('connection found at', num)
                           foundConnection = 1
                           currConnection = num
                           
                   counter = num + 1

        for q in connect:
            if(num + 1 == q):
                    for f in fish:
                        if(f[0] == q):
                            f[0] = num
                        if(f[1] == q):
                            f[1] = num
                               
                    connect.remove(q)
                    connect.append(num)
                    #print('connection found at asdf', num)
                    foundConnection = 1
                    currConnection = num
                    if(vertical == 1 and verticalSize > 1):
                        verticalSize = verticalSize + 1
                        potentialHead[-1][0] = 0
                        #print('vertical up', verticalSize)
                        removed = num
                        connect.remove(num)
                        connect.append(num-verticalSize)
                        #print('new point:', num-verticalSize)
                        vertical = 0
                        verticalSize = 0
                        currConnection = -1

            elif(num - 1 == q):
                    for f in fish:
                        if(f[0] == q):
                            f[0] = num
                        if(f[1] == q):
                            f[1] = num
                    connect.remove(q)
                    connect.append(num)
                    #print('connection found at asdf', num)
                    foundConnection = 1
                    currConnection = num
                    if(vertical == 1 and verticalSize > 1):
                        verticalSize = verticalSize + 1
                        #print('vertical up', verticalSize)
                        removed = num
                        connect.remove(num)
                        connect.append(num-verticalSize)
                        potentialHead[-1][0] = 0
                        #print('new point:', num-verticalSize)
                        vertical = 0
                        verticalSize = 0
                        currConnection = -1

        exitNum = 0

        if(currNum not in connect and currNum != removed):
            #print('test')
            for q in connect:
                #print(currNum, 'connect', q)
                if(currNum > q):
                    if(((currNum - q) <= 2)):
                        for f in fish:
                            if(f[0] == q):
                                f[0] = currNum
                            if(f[1] == q):
                                f[1] = currNum
                        connect.remove(q)
                        connect.append(currNum)
                        exitNum = 1
                elif(currNum < q):
                    if(((q - currNum) <= 2)):
                        connect.remove(q)
                        connect.append(currNum)
                        exitNum = 1

            if(exitNum == 0):
                #print('removed', removed)
                connect.append(currNum + 1)
                #print('last', currNum)
                if(vertical == 1):
                    #print('remove', currConnection)
                    connect.remove(currConnection)
                    for f in fish:
                            if(f[0] == currConnection):
                                f[0] = currNum
                            if(f[1] == currConnection):
                                f[1] = currNum
                    
                    #print('Vertical down, size', verticalSize)
                    #print('potential head', currNum + 1)

                    if (((potentialHead[-1][5] - (counter - 1)) <= 1) or ((counter - 1)-potentialHead[-1][5] <=1)): 
                        #print('head found')
                        middleX = potentialHead[-1][7]/2
                        middleX = countX - middleX
                        middleY = potentialHead[-1][5] - potentialHead[-1][4]
                        middleY = middleY/2
                        middleY = potentialHead[-1][4] + middleY

                        middleX1 = int(round(middleX)) + 5
                        middleX2 = int(round(middleX)) - 5

                        middleY1 = int(round(middleY)) + 5
                        middleY2 = int(round(middleY)) - 5

                        #print('test', middleX1, middleX2, middleY1, middleY2)
                        if(potentialHead[-1][7] > 30 and fish[0][2] != 1):
                            img2 = cv2.rectangle(img2, (middleX1, middleY1), (middleX2, middleY2), (0,0,255), 10)
                            #cv2.imshow('image3', img2)
                            fish[0][2] = 1
                    if((potentialHead[-1][0] - potentialHead[-1][1]) < 60): 
                        potentialHead[-1][5] = currNum + 1
                        min_dist = sys.maxsize
                        for connect1 in connect:
                                if(connect1 != (currNum + 1) and (abs(connect1-currNum) < min_dist)):
                                    min_dist = abs(connect1-currNum)
                                    potentialHead[-1][4] = connect1
                        potentialHead[-1][7] = 0
                        potentialHead[-1][1] = 0

        #for q in connect:
            #print("connect", q)

        #print('num connections:', len(connect), '\n')

        #for asdf in potentialHead:
            #print(asdf, '\n')

def binaryFile1(filename):
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(img,100,200)
    contours, h = cv2.findContours(edges,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        cv2.drawContours(img,[cnt],0,(0,0,255),2)
    plt.figure(figsize = (20,15))
    plt.imshow(img, aspect = 'auto')

    image=np.zeros((700,700,3),np.uint8)

    array = []

    for i in contours:
        for j in i:
                if(j[0][0] <= 275 and j[0][1] <= 590):
                    array.append(j[0])
                    image[j[0][1], j[0][0]]=[0,0,255]

    sortedarray =  sorted(array, key=lambda x: x[0] )

    unique = []
    for i in sortedarray:
        if not (any((i == x).all() for x in unique)):
            unique.append(i)

    for a in sortedarray:
        if(a[0] == 0):
            discont.append(a[1])

    discont.sort()

    index = 0

    found = 0

    for i in range(0,len(discont),2):
        connect.append(discont[i])
        connect.append(discont[i+1])

        arr1 = [discont[i], discont[i+1], 0]
        potentialFish.append(arr1)
        potentialHead.append([0, 0, -1, -1, -1, -1, 0, 0])
        fish.append([discont[i], discont[i+1], 0])

    maxnum = 0

    zeroArray.sort()

    counter = 0

    posIndex = 1

    countX = 0

    img2 = cv2.imread(filename)

    for arr in unique:
        if(arr[0] != posIndex and arr[0] != 0):
            print('Find vertical for ', posIndex)
            find_verticals1(currentPos, countX, img2)
            countX = countX + 1
            posIndex = posIndex + 1
            currentPos.clear()
            currentPos.append(arr[1])
        else:
            currentPos.append(arr[1])

    print(' \n Potential Fish starting boundaries')
    for arr in potentialFish:
        print('[' + str(arr[0]), str(arr[1]) + '] at x:', arr[2])

    print('Fish Ending boundaries')
    for f in fish:
        print(f)

    print('Head tracker data:') 
    for qwer in potentialHead:
        print(qwer)
        
    img2 = image_resize(img2, height = 300)

    cv2.imwrite("new.png", img2)

    cv2.imshow('image', img2)

    plt.imshow(img)
    plt.show()

