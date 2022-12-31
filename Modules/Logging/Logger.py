import configparser
import os
import logging
from pathlib import Path
from datetime import date
import sys


def LoggingConfiguration(AppName):
    today=date.today()
    StrDate=str(today.strftime("%b-%d-%Y"))
    Path(str(AppName+"_Logs/")).mkdir(parents=True,exist_ok=True)
    logging.basicConfig(filename=str(AppName)+"_Logs/"+str(AppName)+"_"+StrDate+".log", filemode='w+',format="%(asctime)s - %(message)s",level="INFO")
    return(logging.getLogger())

config = configparser.RawConfigParser()
#ini_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..config.ini')
ini_path=Path(os.path.join(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent),"config.ini")

config.read(ini_path)


Logger=LoggingConfiguration(config.get('LOGGING','app_name'))
