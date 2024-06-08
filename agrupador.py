import cv2
import numpy as np
import pyautogui
import os
import time
import math


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def group_objects(points, filename, original_position):
    print("group_objects", filename, points)
    
    if len(points) < 2:
        return
    
    pos1, pos2 = points[0], points[1]

    if distance(pos1, pos2) >= 30:
        
        pyautogui.mouseDown(pos1)
        pyautogui.mouseUp(pos1)

        # Pequena pausa para evitar problemas de sincronização
        time.sleep(0.2)

        pyautogui.mouseDown(pos2)
        pyautogui.mouseUp(pos2)
        
        time.sleep(0.2)
    else:
        print("As posições estão muito próximas, não foi possível agrupar.")


def find_objects_on_screen(template):
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9  # Ajuste conforme necessário
    loc = np.where(result >= threshold)

    points = []
    template_height, template_width = template.shape[:2]
    for pt in zip(*loc[::-1]):
        center_pt = (pt[0] + template_width // 2, pt[1] + template_height // 2)
        if all(distance(center_pt, existing_pt) >= 20 for existing_pt in points):
            points.append(center_pt)

    return points

def load_images_from_folder(folder):
    return [(filename, cv2.imread(os.path.join(folder, filename))) for filename in os.listdir(folder) if cv2.imread(os.path.join(folder, filename)) is not None]

def main():
    itens = 'c://Workspace/agrupador/itens'
    guarda = 'c://Workspace/agrupador/guarda'
    images = load_images_from_folder(itens)
    guardaReal = load_images_from_folder(guarda)
    time.sleep(5)
    original_position = pyautogui.position()
    while True:
        for filename, template in images:
            item_points = find_objects_on_screen(template)
            while len(item_points) > 1:
                group_objects(item_points, filename, original_position)
                item_points = find_objects_on_screen(template)
                
        time.sleep(0.2)
        pyautogui.mouseDown(original_position)
        pyautogui.mouseUp(original_position)
        
        
        

if __name__ == "__main__":
    main()