import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import cv2

def saveScreenshot(url,windowSize,scName):

    chrome_options = Options()
    chrome_options.add_argument(windowSize)

    driver = webdriver.Chrome(options=chrome_options)

    wait = WebDriverWait(driver, 15) #setting up waiting time

    driver.get(url) #entering metrobi website

    time.sleep(2)

    screenshot_path = scName #sets name of sc
    driver.save_screenshot(screenshot_path) #does sc

def getCoordinates(scName,factor,invert):
    
    # Load the small image with transparency
    logo = cv2.imread("logo.png", cv2.IMREAD_UNCHANGED)

    # Check if the small image was loaded successfully

    # Create a mask to identify transparent areas
    mascara = logo[:, :, 3] == 0

    cor_fundo = [255, 255, 255]  # White

    # Apply the background color only to transparent areas
    logo[mascara, :3] = cor_fundo

    resized_logo = cv2.resize(logo, (int(logo.shape[1] * factor), int(logo.shape[0] * factor)))

    if(invert==True):
        resized_logo = cv2.bitwise_not(resized_logo)

    screenshot = cv2.imread(scName, cv2.IMREAD_UNCHANGED)

    # Encontrar a logo na screenshot
    result = cv2.matchTemplate(screenshot, resized_logo, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Obter as coordenadas do canto superior esquerdo e inferior direito da logo encontrada
    top_left = max_loc
    h, w = resized_logo.shape[:2]
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Desenhar um retângulo ao redor da logo encontrada na screenshot
    cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)

    # Mostrar a screenshot com a logo destacada
    cv2.imshow('Resultado', screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return top_left


saveScreenshot("https://metrobi.com","--window-size=640,1136","screenshotMobile.png")

saveScreenshot("https://metrobi.com","--window-size=1920,1080","screenshotDesktop.png")

saveScreenshot("https://deliver.metrobi.com/signin","--window-size=640,1136","screenshotLoginMobile.png")

saveScreenshot("https://deliver.metrobi.com/signin","--window-size=1920,1080","screenshotLoginDesktop.png")

mx,my = getCoordinates("screenshotMobile.png",0.35,False)

print("top-left position for mobile main website:")

print(mx)
print(my)

dx,dy = getCoordinates("screenshotDesktop.png",0.35,False)

print("top-left position for desktop main website:")

print(dx)
print(dy)

mx,my = getCoordinates("screenshotLoginMobile.png",0.75,False)

print("top-left position for mobile login website:")

print(mx)
print(my)

dx,dy = getCoordinates("screenshotLoginDesktop.png",0.35,True)

print("top-left position for desktop main website:")

print(dx)
print(dy)