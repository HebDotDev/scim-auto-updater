#Import section
import time
import configparser
import os
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import chrome
from selenium.webdriver import firefox
from selenium.webdriver import edge
import msvcrt
from msvcrt import getch
import sys
import threading
from threading import Timer

from pathlib import Path


#functions

def input_listener():
    while True:
        user_input = input()
        if user_input.lower() == 'exit' or user_input.lower() == 'e' or user_input.lower() == 'quit' or user_input.lower() == 'q':
            print("Exiting program...")
            print("You can close this window now")

            os._exit(0)
        elif user_input.lower() == 'settings' or user_input.lower() == 'setting':
            print("entering settings menu")
            
            config = read_config()
            print(config.sections())
            
            print("Current Settings :\n",config.__str__())
            print({section: dict(config[section]) for section in config.sections()})
        else:
            print("that is not a valid command, try -help or -h to get some help / see the available commands")



def open_ia_in_browser(browser_pref = "firefox"):

    cfg = read_config()

    match browser_pref:
        case "firefox":
            driver = webdriver.Firefox()
        case "chrome":
            driver = webdriver.Chrome()
        case "edge":
            driver = webdriver.Edge()
        case _:
            print("oh, there is somethin wrong with the chosen Browser")
            return


    driver.set_window_size(1024, 600)
    driver.maximize_window()
    driver.implicitly_wait(10)

    scim_url = cfg.get('DEFAULT','DefaultURL')
    driver.get(scim_url)
    
    manage_consent_option(driver)
    manage_patreon_modal(driver)

    

    if cfg.get('DEFAULT','togglefullscreenmap') == 'True':
        toggle_fullscreen_option(driver)

    return driver

def toggle_fullscreen_option(driver : webdriver):

    map_canvas = driver.find_element(By.XPATH,'.//canvas[@class="leaflet-zoom-animated"]')
    fullscreen_toggle = map_canvas.find_element(By.XPATH, '//a[@class="leaflet-control-fullscreen-button leaflet-bar-part"]')
    fullscreen_toggle.click()

def manage_consent_option(driver : webdriver):

    manage_bt = driver.find_element(By.XPATH,'.//button[@class = "fc-button fc-cta-manage-options fc-secondary-button"]')
    manage_bt.click()
    confirm_choice_bt = driver.find_element(By.XPATH, '//button[@class = "fc-button fc-confirm-choices fc-primary-button"]')
    confirm_choice_bt.click()
    

def manage_patreon_modal(driver : webdriver):

    modal = driver.find_element(By.XPATH, './/div[@class = "modal fade show"]')
    closing_modal = modal.find_element(By.XPATH, './/button[@class = "close"]')
    closing_modal.click()

def manage_cookie_banner(driver : webdriver):
    banner = driver.find_element(By.XPATH,'.//div[@class = "cc-window cc-banner cc-type-info cc-theme-block cc-bottom cc-color-override-688238583"]')
    banner_bt = banner.find_element(By.XPATH, './/a[@class = "cc-btn cc-dismiss"]')
    banner_bt.click()

def update_update_time():
    pass


def update_savefile(driver : webdriver):
    savefolder = identify_savefolder()
    os.chdir(savefolder)
    files = filter(os.path.isfile, os.listdir(savefolder))
    files = [os.path.join(savefolder, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    print("Loading: ",files[-1])
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(files[-1])
    print("\nupdated savefile")


def open_map_on_start(driver :webdriver):
    
    savefolder = identify_savefolder()
    os.chdir(savefolder)
    files = filter(os.path.isfile, os.listdir(savefolder))
    files = [os.path.join(savefolder, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    print("loading: ",files[-1])
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(files[-1])

def identify_savefolder():

    save_game_path = os.getenv('LOCALAPPDATA') + '\FactoryGame\Saved\SaveGames'
    savefolder = save_game_path + '\\' + os.listdir(save_game_path)[0]
    return savefolder


def init_config():

    config = configparser.ConfigParser()
    setup_undone = True
    ToggleFullscreenMap_done = False
    CustomSavesPATH_done = False
    BrowserPref_done = False
    Auto_Save_update_timer_done = False

    while(setup_undone):

        if not ToggleFullscreenMap_done:
            ToggleFullscreenMap = input("Should the Map be opened on Fullscreen on start ? Type True or False\t").lower()
            if ToggleFullscreenMap == 'false' or ToggleFullscreenMap == 'true':
                ToggleFullscreenMap_done = True
                ToggleFullscreenMap = ToggleFullscreenMap.capitalize()
            
        if not CustomSavesPATH_done:
            CustomSavesPATH = input("Do you want to use a custom saves Folder ? Type True or False\t").lower()
            if CustomSavesPATH == 'false' or CustomSavesPATH == 'true':
                CustomSavesPATH_done = True
                CustomSavesPATH = CustomSavesPATH.capitalize()

        if not BrowserPref_done:
            BrowserPref = input("In which Browser should i open the interactive map? Choices are firefox, chrome and edge(least stable)\t").lower()
            if BrowserPref == 'firefox' or BrowserPref == 'chrome' or BrowserPref == 'edge':
                BrowserPref_done = True
        
        if not Auto_Save_update_timer_done:
            Auto_Save_update_timer = input("How often should i update the save file to the map ? (usually 5-10) answer in Minutes\t")
            if Auto_Save_update_timer.isdigit():
                Auto_Save_update_timer_done = True
                Auto_Save_update_timer = int(Auto_Save_update_timer) * 60
        
        if ToggleFullscreenMap_done and CustomSavesPATH_done and BrowserPref_done and Auto_Save_update_timer_done:
            setup_undone = False
        else:
            print("Oh, it seems like there was something wrong with some of your answers, please re-answer these Questions. Take a close look at what is expected")

    config['DEFAULT'] = {
        'DefaultURL' : 'https://satisfactory-calculator.com/en/interactive-map',
        'Default savegame path':"%%LOCALAPPDATA%%\FactoryGame\Saved\SaveGames",
        'Custom savegame path':"%%LOCALAPPDATA%%\FactoryGame\Saved\SaveGames",
        'ToggleFullscreenMap': ToggleFullscreenMap,
        'CustomSavesPATH': CustomSavesPATH,
        'BrowserPref' : BrowserPref,
        'Auto Save update timer': Auto_Save_update_timer,
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def read_config():
    config = configparser.ConfigParser()
    config.sections()
    config.read(".//config.ini")

    return config

def update_config(config : configparser):
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


# MAIN

def main():


    #global satisfactory_savegame_path
    #satisfactory_savegame_path = '%LOCALAPPDATA%\FactoryGame\Saved\SaveGames'

    config = configparser.ConfigParser()
    config.sections()

    if exists(".//config.ini"):
        config.read(".//config.ini")


    else:
        print("config file missing!")
        print("creating ...")
        init_config()


    config.read(".//config.ini")

    update_timer = int(config.get('DEFAULT','Auto Save update timer'))
    browser_pref = config.get('DEFAULT','browserpref')

    current_driver = open_ia_in_browser(browser_pref=browser_pref)

    listener_thread = threading.Thread(target=input_listener)
    listener_thread.daemon = True
    listener_thread.start()

    open_map_on_start(current_driver)

    while(True):

        print("type exit or e to quit the programm")
        update_savefile(current_driver)
        time.sleep(update_timer)

    

if __name__ == '__main__':
    main()