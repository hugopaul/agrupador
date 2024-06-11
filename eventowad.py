import cv2
import numpy as np
import pyautogui
import os
import time
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def log_time(message, start_time):
    elapsed_time = time.time() - start_time
    print(f"{message} - Tempo decorrido: {elapsed_time:.2f} segundos")

def click_center_of_screen():
    print("Iniciando clique no centro da tela")
    start_time = time.time()
    
    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2

    pyautogui.mouseDown(center_x, center_y)
    pyautogui.mouseUp(center_x, center_y)
    
    log_time("Clique no centro da tela concluído", start_time)

def group_objects(points, filename):
    print(f"Iniciando agrupamento de objetos para {filename} com {len(points)} pontos")
    start_time = time.time()
    
    if len(points) < 2:
        return
    
    pos1, pos2 = points[0], points[1]

    if distance(pos1, pos2) >= 20:
        time.sleep(0.5)
        pyautogui.mouseDown(pos1)
        pyautogui.mouseUp(pos1)
        time.sleep(0.5)
        pyautogui.mouseDown(pos2)
        pyautogui.mouseUp(pos2)
        time.sleep(0.5)
    else:
        print("As posições estão muito próximas, não foi possível agrupar.")
    
    log_time(f"Agrupamento de objetos para {filename} concluído", start_time)
 
def click_guarda(points, filename):
    print(f"Iniciando clique de guarda para {filename} com {len(points)} pontos")
    start_time = time.time()
    
    if len(points) < 1:
        return
    
    pos1 = points[0]
    pyautogui.moveTo(pos1)
    time.sleep(0.1)
    pyautogui.mouseDown(pos1)
    pyautogui.mouseUp(pos1)
    time.sleep(0.2)
    
    log_time(f"Clique de guarda para {filename} concluído", start_time)
    
def dividir_bau(points, filename):
    print(f"Iniciando divisão de baú para {filename} com {len(points)} pontos")
    start_time = time.time()
    
    if len(points) < 1:
        return
    
    pos1 = points[0]
    pyautogui.keyDown('shift')
    time.sleep(0.3)
    pyautogui.mouseDown(pos1)
    pyautogui.mouseUp(pos1)
    time.sleep(0.3)
    pyautogui.keyUp('shift')
    time.sleep(0.3)
    pyautogui.press('1')
    pyautogui.press('enter')
    time.sleep(0.3)
    log_time(f"Divisão de baú para {filename} concluída", start_time)

def find_objects_on_screen(template):
    start_time = time.time()
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(result >= threshold)

    points = []
    template_height, template_width = template.shape[:2]
    for pt in zip(*loc[::-1]):
        center_pt = (pt[0] + template_width // 2, pt[1] + template_height // 2)
        if all(distance(center_pt, existing_pt) >= 20 for existing_pt in points):
            points.append(center_pt)

    log_time("Busca de objetos na tela concluída", start_time)
    return points

def find_objects_on_screen_marge7(template):
    start_time = time.time()
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(result >= threshold)

    points = []
    template_height, template_width = template.shape[:2]
    for pt in zip(*loc[::-1]):
        center_pt = (pt[0] + template_width // 2, pt[1] + template_height // 2)
        if all(distance(center_pt, existing_pt) >= 20 for existing_pt in points):
            points.append(center_pt)

    log_time("Busca de objetos na tela com margem 7 concluída", start_time)
    return points

def load_images_from_folder(folder):
    start_time = time.time()
    images = [(filename, cv2.imread(os.path.join(folder, filename))) for filename in os.listdir(folder) if cv2.imread(os.path.join(folder, filename)) is not None]
    log_time(f"Carregamento de imagens do diretório {folder} concluído", start_time)
    return images

def process_agrupar(images):
    for filename, template in images:
        start_time = time.time()
        item_points = find_objects_on_screen_marge7(template)
        while len(item_points) > 1:
            group_objects(item_points, filename)
            item_points = find_objects_on_screen_marge7(template)
        log_time(f"Processamento de agrupamento para {filename} concluído", start_time)

def proccess_dividir(baus):
    for filename, template in baus:
        start_time = time.time()
        print(f"Processando divisão para {filename}")
        bau_point = find_objects_on_screen(template)
        while len(bau_point) >= 1:
            dividir_bau(bau_point, filename)
            bau_point = find_objects_on_screen(template)
            break
        log_time(f"Processamento de divisão para {filename} concluído", start_time)

def process_trocar(guardaImages):
    start_time = time.time()
    #for filename, template in guardaImages:
    #    guardaPoints = find_objects_on_screen(template)
    #    contador = 0
    #    while len(guardaPoints) > 1 and contador <= 1:
    #        click_guarda(guardaPoints, filename)
    #        item_points = find_objects_on_screen(template)
    #        contador += 1
    click_center_of_screen()
    log_time("Processamento de troca concluído", start_time)

def main():
    itensAAgruparPath = 'c://Workspace/agrupador/itensAgrupar'
    bauImagePath = 'c://Workspace/agrupador/bau'
    guardaImagesPath = 'c://Workspace/agrupador/guarda'

    agruparImages = load_images_from_folder(itensAAgruparPath)
    bauDividirImages = load_images_from_folder(bauImagePath)
    guardaTrocarImages = load_images_from_folder(guardaImagesPath)

    time.sleep(2)

    while True:
        start_time = time.time()
        proccess_dividir(bauDividirImages)
        log_time("Loop de divisão concluído", start_time)

        start_time = time.time()
        process_trocar(guardaTrocarImages)
        log_time("Loop de troca concluído", start_time)

        start_time = time.time()
        process_agrupar(agruparImages)
        log_time("Loop de agrupamento concluído", start_time)
        
        time.sleep(1)
1
main()
