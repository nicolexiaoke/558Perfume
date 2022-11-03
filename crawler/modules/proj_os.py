import os
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
import warnings


# ----------- functions -------------

def Get_Root_dir():
    path = __file__
    for _ in range(3):
        path = os.path.split(path)[0]
    return path

# ----------- global settings -----------

LOGGER.setLevel(logging.WARNING)
warnings.filterwarnings("ignore")