#region Python Imports
import json
import random
import time
from pathlib import Path
import pyautogui
from rapidfuzz import fuzz
from Functions.gui import *
import easyocr
import cv2
import numpy as np
#endregion

#region Start External Scripts and Tools
#region Start Gui
#TODO Find a way to run Gui and Script at the same time
#endregion
#regionStart OCR
reader = easyocr.Reader(['en'])
#endregion
#endregion

#region Data Import
#region Imported Variables
window = MainWindow()
wanted_name = window.namecheck()
wanted_nature = window.naturecheck()
bot_enable = window.startbot()
bot_disable = window.stopbot()
bot_exit = window.closebot()
#endregion

#region Imported Databases #TODO: Adicionar JSON com todas as abilidades do jogo
base_dir = Path(__file__).parent
moves_path = base_dir / 'Databases' / 'moves.json'
abilities_path = base_dir / 'Databases' / 'abilities.json'
species_path = base_dir / 'Databases' / 'species.json'
types_path = base_dir / 'Databases' / 'types.json'
natures_path = base_dir / 'Databases' / 'natures.json'
#endregion

#region Imported Images
#endregion
#endregion

#region Flags
flag_in_battle = False
flag_stuck = "OK"
flag_db_loaded = False
flag_first_run = False
#endregion

#region Configs
cfg_pokemon_name_confidence = 80
cfg_pokemon_nature_confidence = 80
cfg_pokemon_ability_confidence = 80
cfg_threshold_min = 0
cfg_threshold_max = 255
cfg_denoise = 3
#endregion

#region Screen regions #TODO: Mudar estas cordenas
sideparty_region = [1234, 470, 1365, 767]
battlecheck_region = [1100, 650, 1300, 750]
select_oth_pk_region = [565, 114, 794, 159]
pokecenter_region = [500, 100, 650, 250]
#endregion

#region Actions Locations on Screen #TODO: Mudar estas cordenas
fight_btn_x, fight_btn_y = 647, 650
run_btn_x, run_btn_y = 845, 730
choose_other_pk_btn_x, choose_other_pk_btn_y = 678, 240
move1_x, move1_y = 522, 586
move2_x, move2_y = 814, 589
move3_x, move3_y = 522, 652
move4_x, move4_y = 814, 652
#endregion

#region Functions

#region Database Import
def import_dbs():
    try:
        with moves_path.open('r', encoding='utf-8') as f:
            moves_db = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None
    try:
        with species_path.open('r', encoding='utf-8') as f:
            species_db = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None
    try:
        with types_path.open('r', encoding='utf-8') as f:
            types_db = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None
    try:
        with natures_path.open('r', encoding='utf-8') as f:
            natures_db = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None
    try:
        with abilities_path.open('r', encoding='utf-8') as f:
            abilities_db = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None

    return moves_db, species_db, types_db, natures_db, abilities_db
#endregion

#region Name and Nature Verification
def name_exists(wanted, names_list):
    w = wanted.strip().lower()
    return any(n.get('name', '').lower() == w for n in names_list)


def nature_exists(wanted, nature_list):
    w = wanted.strip().lower()
    return any(n.get('nature', '').lower() == w for n in nature_list)
#endregion

#region Movement Functions
def walk(direction, walk_time):
    pyautogui.keyDown(direction)
    time.sleep(random.uniform(walk_time / 2, walk_time * 1.5))
    pyautogui.keyUp(direction)


def single_press(direction):
    pyautogui.keyDown(direction)
    time.sleep(random.uniform(0.1, 0.5))
    pyautogui.keyUp(direction)
    time.sleep(random.uniform(0.1, 0.5))
#endregion

#region Fight Functions
def use_move(move_number):
    match move_number:
        case "1":
            time.sleep(random.uniform(0.5, 2))
            pyautogui.click(fight_btn_x, fight_btn_y)
            time.sleep(random.uniform(0.5, 2))
            pyautogui.click(move1_x, move1_y)
            return None
        case "2":
            time.sleep(random.uniform(0.5, 2))
            pyautogui.click(fight_btn_x, fight_btn_y)
            time.sleep(random.uniform(0.5, 2))
            pyautogui.click(move2_x, move2_y)
            return None
        case "3":
            time.sleep(random.uniform(0.5, 2))
            pyautogui.click(fight_btn_x, fight_btn_y)
            time.sleep(random.uniform(0.5, 2))
            pyautogui.click(move3_x, move3_y)
            return None
        case "4":
            time.sleep(random.uniform(0.5, 2))
            pyautogui.click(fight_btn_x, fight_btn_y)
            time.sleep(random.uniform(0.5, 2))
            pyautogui.click(move4_x, move4_y)
            return None
        case _:
            print("Invalid move number")
            stuck = "Move invalid"
            return stuck


def run_away():
    time.sleep(random.uniform(0.5, 2))
    pyautogui.click(run_btn_x, run_btn_y)
    time.sleep(random.uniform(0.5, 2))


#TODO: Implementar Atirar pokebola
#TODO: Trocar de Pokemon
#endregion

#region Pokémon Verification Functions

def verify_pokemon(wanted, found):
    return fuzz.ratio(wanted, found) >= cfg_pokemon_name_confidence


def verify_nature(wanted, found):
    return fuzz.ratio(wanted, found) >= cfg_pokemon_nature_confidence


def verify_ability(wanted, found):
    return fuzz.ratio(wanted, found) >= cfg_pokemon_ability_confidence

#TODO: Verificar Shiny
#endregion

#region Text Inspection Functions

def inspect_name():
    inspect = reader.readtext('pokemon_name_image.png')
    text = [t[1] for t in inspect]
    return text


def inspect_nature():
    inspect = reader.readtext('pokemon_nature_image.png')
    text = [t[1] for t in inspect]
    return text


def inspect_ability():
    inspect = reader.readtext('pokemon_ability_image.png')
    text = [t[1] for t in inspect]
    return text
#endregion

#region Image Get and Treatment Functions

def configure_regions():
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    x, y, w, h = cv2.selectROI("Drag to select region", img, True, False)
    cv2.destroyAllWindows()
    region = img[y:y + h, x:x + w]
    return region


def print_region(region):
    screenshot = pyautogui.screenshot(region=region)
    return screenshot


def image_treatment(image_path):
    img = cv2.imread(image_path)
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(grayscale, cfg_threshold_min, cfg_threshold_max, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.medianBlur(threshold, cfg_denoise)
    return denoised
    #Do Morphology if only necessary - This could cause letters to stick AB-> A
    #morph = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    #clean = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)
#endregion
#endregion

#region Main Script
while bot_enable:
    print("Bot enabled ")
    pyautogui.moveTo(cursor_away, cursor_away)

    # check if battle
    overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region)

    if overworld_screen is not None:  # we're not in battle
        chat_debug("no battle")

        # check if 1st pokemon alive (if party 2, check 1st pok, if party 6, check 5th pok)
        fainted_on_screen = len(list(pyautogui.locateAllOnScreen("fainted_pkmn.png", region=sideparty_region)))

        while fainted_on_screen == party_num - 1:
            chat_debug("pokemon fainted")

            # go up right in the corner
            walk("up", 5)
            walk("right", 5)
            overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region)
            if overworld_screen is None:
                in_battle = True
                break
            # go to pokecenter, heal, go back
            move_between_pc_grass(grass_to_pc)
            heal_at_pcenter()
            move_between_pc_grass(pc_to_grass)
            break

        # check if wiped (in pokemon center)
        pokecenter_on_screen = pyautogui.locateCenterOnScreen("pokecenter.png", region=pokecenter_region)

        if fainted_on_screen != party_num - 1:  # if not 5/6 fainted
            chat_debug("party_num not " + str(party_num - 1))
            if pokecenter_on_screen is None:  # and it's not because we wiped and are at pc
                chat_debug("we not in pc")

                # Walk in grass square
                chat_debug("walking around in grass")
                while not in_battle:
                    for step in range(random.randint(1, 5)):
                        single_press("down")
                    for step in range(random.randint(1, 4)):
                        single_press("up")
                    overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region,
                                                                      grayscale=True)
                    if overworld_screen is None:
                        in_battle = True
                    else:
                        pass
            else:
                # walk to grass
                chat_debug("wiped! walking back to grass")
                leave_pcenter()
                move_between_pc_grass(pc_to_grass)

    else:
        in_battle = True
        while in_battle:
            chat_debug("battle")
            for try_attack in range(10):  # try attacking for 10 seconds
                use_move(move4_x, move4_y)

            current_pk_dead = pyautogui.locateCenterOnScreen("fainted_in_battle.png", region=select_oth_pk_region)
            overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region)

            # Check if battle finished
            if overworld_screen is not None:
                in_battle = False
                break

            # Check if current pk dead
            if current_pk_dead is not None:  # select a pokemon screen is visible
                pyautogui.click(choose_other_pk_btn_x, choose_other_pk_btn_y)
                time.sleep(5)

                # Try to run
                run_away()
                overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region)
                while overworld_screen is None:
                    run_away()
                    overworld_screen = pyautogui.locateCenterOnScreen("not_battle.png", region=battlecheck_region)
                pyautogui.moveTo(cursor_away, cursor_away)
                in_battle = False
#endregion