from seleniumwire import webdriver
#pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from ..Logging import Logger
import os
import json
from pathlib import Path
import configparser

def FrontEndAuth():
    try:
        Logger.Logger.info("Performing front End authentication")
        print("Performing Front end authentication...")
        config = configparser.RawConfigParser()
        ini_path=Path(os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent),"config.ini")
        config.read(ini_path)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options,executable_path=ChromeDriverManager().install())
        driver.delete_all_cookies()
        driver.get("https://twitter.com/i/flow/login")
        time.sleep(5)
        UsernameBox=driver.find_element(by="xpath",value=("/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input"))
        UsernameBox.send_keys(str(config.get('FRONTEND','username')))
        driver.find_element(by="xpath",value=('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')).click()
        time.sleep(3)
        PasswordBox=driver.find_element(by="xpath",value=("/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input"))
        PasswordBox.send_keys(str(config.get('FRONTEND','password')))
        time.sleep(1)
        driver.find_element(by="xpath",value=('/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')).click()
        time.sleep(5)
        for x in driver.requests:
            if str("Bearer") in str(x.headers):    
                BearerToken= str(x.headers['authorization'])
                break 
        Cookies={}
        Cookies['Bearer']=BearerToken
        for x in driver.get_cookies():
            Cookies[x['name']]=x['value']
        driver.quit()
        json_object = json.dumps(Cookies, indent=4)
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'FrontEndCookies.json'), "w") as outfile:
            outfile.write(json_object)
    except Exception as e:
        Logger.Logger.warning("An error occured during authentication:")
        Logger.Logger.warning(str(e))


