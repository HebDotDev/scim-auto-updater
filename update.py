#Import section
import time
import requests
import configparser
import os
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import chrome
from selenium.webdriver import firefox
from selenium.webdriver import edge





global scim_url
scim_url = 'https://satisfactory-calculator.com/en/interactive-map'

global satisfactory_savegame_path
satisfactory_savegame_path = '%LOCALAPPDATA%\FactoryGame\Saved\SaveGames'

#functions

def open_ia_in_browser(browser_pref = "firefox"):
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
    
    driver.implicitly_wait(2)
    driver.get(scim_url)
    
    manage_consent_option(driver)
    manage_patreon_modal(driver)
    #manage_cookie_banner(driver)
    time.sleep(1)

    toggle_fullscreen_option(driver)


    




    return driver

def toggle_fullscreen_option(driver : webdriver):

    map_canvas = driver.find_element(By.XPATH,'.//canvas[@class="leaflet-zoom-animated"]')
    fullscreen_toggle = map_canvas.find_element(By.XPATH, '//a[@class="leaflet-control-fullscreen-button leaflet-bar-part"]')
    fullscreen_toggle.click()

def manage_consent_option(driver : webdriver):


    consent_class = driver.find_element(By.XPATH, './/div[@class = "fc-dialog-content"]')
    manage_bt = driver.find_element(By.XPATH,'.//button[@class = "fc-button fc-cta-manage-options fc-secondary-button"]')
    manage_bt.click()
    confirm_choice_bt = driver.find_element(By.XPATH, '//button[@class = "fc-button fc-confirm-choices fc-primary-button"]')
    confirm_choice_bt.click()
    

def manage_patreon_modal(driver : webdriver):
    modal = driver.find_element(By.XPATH, './/div[@class = "modal fade show"]')
    closing_modal = modal.find_element(By.XPATH, './/button[@class = "close"]')
    print(modal.text)
    print(closing_modal.text)
    closing_modal.click()

def manage_cookie_banner(driver : webdriver):
    banner = driver.find_element(By.XPATH,'.//div[@class = "cc-window cc-banner cc-type-info cc-theme-block cc-bottom cc-color-override-688238583"]')
    banner_bt = banner.find_element(By.XPATH, './/a[@class = "cc-btn cc-dismiss"]')
    print(banner_bt.text)
    banner_bt.click()

def update_update_time():
    pass

def open_map_on_start():
    pass

def identify_savefolder():
    pass

def init_config():
    config = configparser.ConfigParser()

    config['DEFAULT'] = {
        'ToggleFullscreenMap': False,
        'CustomSavesPATH': False,
        'BrowserPref' : 'firefox'
    }

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def read_config():
    pass

def update_config():
    pass


# MAIN

def main():
    config = configparser.ConfigParser()
    config.sections()

    if exists(".//config.ini"):
        print("Config file found.")
        config.read(".//config.ini")
        print(config)

    else:
        print("config file missing!")
        print("creating ...")


    config.read(".//config.ini")


    current_driver = open_ia_in_browser()
    time.sleep(120)
    current_driver.quit()


if __name__ == '__main__':
    main()