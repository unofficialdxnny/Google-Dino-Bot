import pyautogui as gui
import keyboard
import time
import math

def getPixel(Image, x, y):
    px = Image.load()
    return px[x, y]

top, left, width, height = 293, 0, 1920, 465
screenDimensions = {
    "top": top,
    "left": left,
    "width": width,
    "height": height
}

last = 0
total_time = 0

y_search, x_start, x_end = 350, 435, 450
y_search2 = 275

time.sleep(1)
while True:
    t1 = time.time()
    if keyboard.is_pressed('q'):
        break

    if math.floor(total_time) != last:
        x_end += 4
        if x_end >= width:
            x_end = width
        last = math.floor(total_time)

    sct_img = gui.screenshot(region=(left, top, width, height))
    bgColor = getPixel(sct_img, 440, 30)

    for i in reversed(range(x_start, x_end)):
        if getPixel(sct_img, i, y_search) != bgColor or getPixel(sct_img, i, y_search2) != bgColor:
            keyboard.press(' ')
            break

    t2 = time.time() - t1
    total_time += t2

    print(x_end)
