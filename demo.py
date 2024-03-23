import pyautogui
import keyboard

while(True):
    if(keyboard.is_pressed("left")):
        pyautogui.moveRel(-50, 0)
    if(keyboard.is_pressed("right")):
        pyautogui.moveRel(50, 0)
    if(keyboard.is_pressed("up")):
        pyautogui.moveRel(0, -50)
    if(keyboard.is_pressed("down")):
        pyautogui.moveRel(0, 50)                        
    if(keyboard.is_pressed("`")):
        break
# pyautogui.moveTo(100, 100, duration = 1)
# pyautogui.moveRel(0, 750, duration = 1)
