import pyautogui
import time
import os
import cv2
import numpy as np
import keyboard
import sys

def find_image(image_name, confidence=0.8):
    # Image(s) must be in a subfolder named images
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "images", image_name)
    
    # Check if image file exists
    if not os.path.exists(image_path):
        print(f"Error: Image {image_name} not found in the 'images' folder! (Path: {image_path})")
        return None

    # Capture screen
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    # Convert to BGR to use OpenCV

    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    
    # Load the image
    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Check if image is accepted
    if template is None:
        print(f"Error: Unable to load the template image {image_name}.")
        return None
    
    # Convert to gray for matching
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    # Match images
    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    
    # Check and calculate match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Check match quality value for debugging purposes
    #print(f"Max value from match for {image_name}: {max_val}")
    
    if max_val >= confidence:
        top_left = max_loc
        h, w = template.shape
        center = (top_left[0] + w // 2, top_left[1] + h // 2)
        return center
    
    return None

def click_on_image(image_name, confidence=0.3):
    # Search for image and click on it, for the dice specifically
    image_location = find_image(image_name, confidence)
    
    if image_location:
        # Print if image is found, for debugging
        #print(f"Found {image_name} at {image_location}")

        # Click dice
        pyautogui.click(image_location)
        return True
    else:
        print(f"Could not find {image_name}.")
    return False

def check_for_exit():
    # Check for the 'F1' key to exit the program
    if keyboard.is_pressed("F1"):
        sys.exit(0)

def main():
    flat_image = "flat13.png"
    dice_image = "dice.png"

    flat_confidence = 0.9
    dice_confidence = 0.4

    # Loop until stat is found 
    while True:
        check_for_exit()

        print(f"Searching for {flat_image}...")
        flat_location = find_image(flat_image, confidence=flat_confidence)
        
        if flat_location:
            print(f"Found the {flat_image}!")
            break
        
        #print(f"{flat_image} not found, re-rolling...")
        # If stat isn't found, roll the dice
        dice_clicked = click_on_image(dice_image, confidence=dice_confidence)
        
        if dice_clicked:
            print(f"Clicked on dice to re-roll...")

            # If dice is rolling too fast, uncomment the line below
            #time.sleep(1)
        else:
            print("Dice image not found, something went wrong")
            break

if __name__ == "__main__":
    main()
