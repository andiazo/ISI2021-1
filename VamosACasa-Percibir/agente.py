import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import time
import webbrowser
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
        heigth = im1.size[0]
        weigth = im1.size[1]

        # numpy array with the maze where:
        # 1 is for road
        # 2 is for house
        # 3 is for owls
        # 4 is for car
        # 0 is for another things
        perception = np.zeros((weigth,heigth))

        # Classify pixels by colors
        for h in range(heigth):
            for w in range(weigth):
                if(base_pixels[h,w] == (102,102,102)):
                    perception[w][h] = 1 # ROAD
                elif(base_pixels[h,w] == (102,0,0) or base_pixels[h,w] == (237,248,1)):
                    perception[w][h] = 2 # HOUSE
                elif(base_pixels[h,w] == (51,51,51)):
                    perception[w][h] = 3 # OWL
                elif(base_pixels[h,w] == (136,1,46)):
                    perception[w][h] = 4 # CAR
                else:
                    base_pixels[h,w] = (0,0,0)
        
        # Save image processed
        name_canvas0 = "canvas_img_" + str(level) + "_0.png"
        im1.save(name_canvas0)

        # Show heatmap
        plt.imshow(perception, cmap='hot', interpolation='nearest')
        plt.show()
        print("Perceive complete!")
        print("NOTE: you could see the perception in the image 'canvas_img_<<level>>_0.png'")
        print("where <<level>> is the current level.")

        return perception

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

def main():
    agente = Agent()
    agente.perceive(1)

if (__name__ == "__main__"):
    main()