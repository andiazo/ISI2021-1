# The function BFS was take from https://www.iteramos.com/pregunta/8113/representar-y-resolver-un-laberinto-dado-una-imagen
# and modified
import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import time
import webbrowser
import math
from queue import Queue
from PIL import Image

class Agent:

    # PERCEIVE
    def perceive(self, level):
        # Take window screenshot
        print("Perceiving...")
        name_screenshot = "screenshot_" + str(level) + ".png"
        pyautogui.screenshot(name_screenshot)

        # Locating canvas
        print("Locating canvas...")
        canvas = self.locatecanvas(name_screenshot)
        
        # Setting the coords of canvas, take a screenshot and save
        canvas_coords = (canvas[1][0], canvas[0][0], canvas[1][-1]-canvas[1][0], canvas[0][-1]-canvas[0][0])
        im = pyautogui.screenshot(region=canvas_coords)
        name_canvas = "canvas_img_" + str(level) + ".png"
        im.save(name_canvas)
        
        # Open the canvas screenshot
        im1 = Image.open(name_canvas)
        base_pixels = im1.load()
        im2 = Image.open(name_canvas)
        base_pixels2 = im2.load()
        heigth = im1.size[0]
        weigth = im1.size[1]
        print(heigth,weigth)
        
        # Proccessing Image
        house_list = []
        car_list = []
        
        bound = 0
        if(level == 1):
            bound = 15
        elif(level == 2):
            bound = 8
        else:
            bound = 15
        
        # Classify pixels by colors
        for w in range(weigth):
            for h in range(heigth):
                if(base_pixels[h,w] == (102,102,102)):
                    for k in range(1,bound):
                        if(h+k < heigth and base_pixels[h+k,w] != (102,102,102)):
                            base_pixels2[h,w] = (0,0,0)
                        if(h-k >= 0 and base_pixels[h-k,w] != (102,102,102)): #(228,222,41)):
                            base_pixels2[h,w] = (0,0,0)
                        if(w-k >= 0 and base_pixels[h,w-k] != (102,102,102)):# (228,222,41)):
                            base_pixels2[h,w] = (0,0,0)
                        if(w+k < weigth and base_pixels[h,w+k] != (102,102,102)): #(228,222,41)):
                            base_pixels2[h,w] = (0,0,0)
                elif(base_pixels[h,w] == (102,0,0) or base_pixels[h,w] == (237,248,1)):
                    house_list.append((h,w))
                elif(base_pixels[h,w] == (213, 215, 38) or base_pixels[h,w] == (219, 215, 44) or base_pixels[h,w] == (204, 208, 42) or base_pixels[h,w] == (230, 223, 44) or base_pixels[h,w] == (228, 222, 41) or base_pixels[h,w] == (58, 86, 96) or base_pixels[h,w] == (57, 82, 92)):
                    for i in range(h-20,h+20):
                        for j in range(w-25,w+25):
                            if(i < heigth and j < weigth):
                                base_pixels[i,j] = (0,255,100)
                elif(base_pixels[h,w] == (136,1,46)):
                    car_list.append((h,w))
                else:
                    base_pixels[h,w] = (0,0,0)
                    base_pixels2[h,w] = (0,0,0)
        
        # Locate car
        sumy_c = 0
        sumx_c = 0
        for coords_c in car_list:
            sumx_c += coords_c[0]
            sumy_c += coords_c[1]

        x_c = sumx_c/len(car_list)
        y_c = sumy_c/len(car_list)
        print("Center of car: x:", x_c, "y:", y_c)

        # Locate house
        sumy_h = 0
        sumx_h = 0
        for coords_h in house_list:
            sumx_h += coords_h[0]
            sumy_h += coords_h[1]

        x_h = sumx_h/len(house_list)
        y_h = sumy_h/len(house_list)
        print("Center of house: x:", x_h, "y:", y_h)

        # Draw Rectangle Car
        x1_c = int(x_c - 27)#0.09*weigth)
        y1_c = int(y_c - 27)#0.05*heigth)
        for i in range(x1_c,x1_c+int(27*2)):
            for j in range(y1_c, y1_c+int(27*2)):
                base_pixels[i,j] = (102,102,102)
                base_pixels2[i,j] = (102,102,102)
        base_pixels[x_c,y_c] = (0,255,255)

        # Draw Rectangle House
        x1_h = int(x_h - 50)#0.14*weigth)
        y1_h = int(y_h - 50)#0.07*heigth)
        for i in range(x1_h,x1_h+int(50*2)):
            for j in range(y1_h, y1_h+int(50*2)):
                base_pixels[i,j] = (102,102,102)
                base_pixels2[i,j] = (102,102,102)
        base_pixels[x_h,y_h] = (0,255,100)
        base_pixels2[x_h,y_h] = (0,255,100)

        #Set star and end points
        if(level == 1):
            start = (int(x_c), int(y_c))
            end = (int(x_h+10), int(y_h))
        elif(level == 2):
            start = (int(x_c), int(y_c))
            end = (int(x_h), int(y_h))
        elif(level == 3):
            start = (int(x_c), int(y_c))
            end = (int(x_h), int(y_h+1))

        base_pixels[start[0],start[1]] = (102,102,102)
        base_pixels[end[0],end[1]] = (102,102,102)
        base_pixels2[start[0],start[1]] = (102,102,102)
        base_pixels2[end[0],end[1]] = (102,102,102)
        print(start,end)

        # Show heatmap
        # plt.imshow(im1)
        # plt.show()
        print("Perceive complete!")
        print("NOTE: you could see the perception in the image 'canvas_img_<<level>>_0.png'")
        print("where <<level>> is the current level.")

        # Save image processed
        name_canvas0 = "canvas_img_" + str(level) + "_0.png"
        name_canvas02 = "canvas_img_" + str(level) + "_02.png"
        im1.save(name_canvas02)
        im2.save(name_canvas0)
        
        return (car_list,house_list, start, end, base_pixels2, level)

    # THINKING
    def think(self, start, end, base_pixels, level):

        path,actions = self.BFS(start, end, base_pixels)
        p_n = "Canvas_img_"+str(level)+"_0.png"
        path_img = Image.open(p_n)
        path_pixels = path_img.load()

        for position in path:
            x,y = position
            path_pixels[x,y] = (255,0,0) # red

        path_name = "think_"+str(level)+".png"
        path_img.save(path_name) 

        print("Think complete!")
        return actions
    
    # ACTION
    def act(self, actions, level):
        
        # Take screenshots
        name_screenshot = "screenshot.png"
        pyautogui.screenshot(name_screenshot)

        # Locate canvas
        coords = self.locatecanvas(name_screenshot)
        x = coords[1][0] + (coords[1][-1] - coords[1][0])//2
        y = coords[0][0] + (coords[0][-1] - coords[0][0])//2

        # Click on the play button
        pyautogui.moveTo(x, y, duration=2)
        pyautogui.click()

        l = 0
        u = 0
        r = 0
        d = 0
        actions_to_do = []
        for i in range(len(actions)):
            if(i == 0):
                a_prev = actions[i]
            else:
                a = actions[i]
                if(a == a_prev):
                    if (a == 'L'):
                        l += 1
                    elif(a == 'U'):
                        u += 1
                    elif(a == 'R'):
                        r += 1
                    elif(a == 'D'):
                        d += 1
                else:
                    if (a_prev == 'L'):
                        actions_to_do.append(["L",l])
                        l = 0
                    elif(a_prev == 'U'):
                        actions_to_do.append(["U",u])
                        u = 0
                    elif(a_prev == 'R'):
                        actions_to_do.append(["R",r])
                        r = 0
                    elif(a_prev == 'D'):
                        actions_to_do.append(["D",d])
                        d = 0
                    a_prev = a

        print("Actions to solve the maze: ",actions_to_do)
        for a in actions_to_do:
            # Set time
            if(level == 1):
                t = (a[1]+5)/115
            elif(level == 2):
                t = (a[1])/115
            elif(level == 3):
                t = (a[1])/115
            # Press Keys
            if(a[0] =='L'):
                pyautogui.keyDown('a')
                time.sleep(t)
                pyautogui.keyUp('a')
            elif(a[0] == 'U'):
                pyautogui.keyDown('w')
                time.sleep(t)
                pyautogui.keyUp('w')
            elif(a[0] == 'R'):
                pyautogui.keyDown('d')
                time.sleep(t)
                pyautogui.keyUp('d')
            elif(a[0] == 'D'):
                pyautogui.keyDown('s')
                time.sleep(t)
                pyautogui.keyUp('s')
        print("Action Complete!")

    def locatecanvas(self, name_img):
        image = Image.open(name_img)
        data = np.asarray(image)
        r,g,b=(0,1,2)
        r_query = 153
        g_query = 0
        b_query = 0
        resultado = np.where((data[:,:,r] == r_query) & (data[:,:,g] == g_query) & (data[:,:,b] == b_query))
        return resultado

    # INITIALIZE - Open website and set up
    def initialize(self):

        print("Initializing...")
        
        # Open page on new tab of default web browser
        webbrowser.open('https://www.juegosinfantilespum.com/laberintos-online/12-auto-buhos.php')
        print("Opening web, waiting 5 seconds...")
        for i in range(5,0,-1):
            time.sleep(1)
            print(i, end=" ")
        print("Open web")
        
        # Take screenshots
        name_screenshot = "screenshot.png"
        pyautogui.screenshot(name_screenshot)
        # Locate canvas
        coords = self.locatecanvas(name_screenshot)

        x = coords[1][0] + (coords[1][-1] - coords[1][0])//2
        y = coords[0][0] + (coords[0][-1] - coords[0][0])//2

        # Click on the play button
        pyautogui.moveTo(x, y, duration=2)
        pyautogui.click()
        print("Click on play button!")

    # INIT 
    def __init__(self):
        print("Agent created")

    def isRoad(self,value):
        if value == (102,102,102):
            return True

    def getAdjacent(self,n):
        x,y = n
        return [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]

    def BFS(self, start, end, pixels):
        directions = ['L','U','R','D'] # Left, Up, Rigth, Down
        actions = Queue()
        actions.put('L')
        queue = Queue()
        queue.put([start])
        
        while not queue.empty():
            act = actions.get()
            path = queue.get() 
            pixel = path[-1]

            if pixel == end:
                return path, act

            for adjacent,direction in zip (self.getAdjacent(pixel),directions):
                x,y = adjacent
                if self.isRoad(pixels[x,y]):
                    pixels[x,y] = (127,127,127) # see note
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.put(new_path)
                    new_action = list(act)
                    new_action.append(direction)
                    actions.put(new_action)

        print("No answer was found :(")

def main():
    agente = Agent()
    while True:
        play = input("Do you want to play? Enter 1: ")
        if (play == '1'):
            l = int(input("Please enter the level 1, 2 or 3: "))
            _,_,start,end,base_pixels,level = agente.perceive(l)
            actions = agente.think(start, end, base_pixels, level)
            agente.act(actions, level)
        else:
            print("See you soon!")
            break

if (__name__ == "__main__"):
    main()