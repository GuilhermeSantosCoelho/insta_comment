# -*- coding: utf-8 -*-    
from src.logger import logger, loggerMapClicked
from cv2 import cv2
from os import listdir
from random import randint
from random import random
import numpy as np
import mss
import pyautogui
import time
import sys
import yaml
import win32com.client as comclt, time
from random import randrange

# Load config file.
stream = open("config.yaml", 'r')
c = yaml.safe_load(stream)
ct = c['threshold']
ch = c['home']
pause = c['time_intervals']['interval_between_moviments']
pyautogui.PAUSE = pause

cat = """
                                                                ,#%%%%(,                      
                                             *%%&%&&&&&&&(...                   
                                           *&&&&&&#*(#/,.., /./                 
                                 .///     .#%%&(........(...#(,...(             
                           .(,.,.,,.,..,,//................/*,,,,*,/            
       .#%%%&&&%%%%&#,    /.,,,....,,,,..,,*............/,,*,,,,,,,,,           
    /&%&&%&%%&&%&&%&/..,*,,.(#%%*,,,.../#((#/........./,,*,,,,,,,,,,.           
  ,&&%&&%(&%%*.........../****/%#%(((((#(*,.,(....../,#/(,*,,,,,,,,/            
 (..,.................... %#%%###*,***,.*(.............,,,,,,,,,*,%             
. ....,,,...............,(****///*...............,@@@#(&..,*,,,(,*              
#/,,,,,,,*,*,//.................................@@@@(....,./*/*                 
%*,,,,,,,,,,,,,**,..*#, ......................,@@@@@@@@&,... *                  
 ,,,,,,,,,,*,**(#(/*@@@@@@&,.................,@@/     .@% % ../                 
 ./,,,,,,,,,*,,*,,*/#%&@@@@@@@%,............,&(%       ,@&%%...*            .   
   ./*,,,,,,,,,,*/....@@@@.    (@@....... .....@&.    /(   *.....,  *., *  /    
       ,/*****/*/(...&#@@.      *@..............,@@@@@&%&#........%.      ,(/   
                 *../&%@@#     .@@....(%&%&%&&%&&%#, ........,*....#    (%,#%(  
                 *..,//   /@@@@@% /&%%&&%&&%%&&&&&&&%% ............,   /%%.#%%#,
                 *......*#%&&(../&&&&&&&&&&&%&&&&&&%&%%#......,**,.*  *(#.(#%%/,
                 /.............(%&&&&&&&&&&&%&&&&&&&&&%%#..........% ./#(.#%#%/*
          ,* * . /........,,...&&&&&%%&&&%#######%&&&&&&%.........(. *#%/.##*%,,
        /.        /............%&&&&&%&###########%&&&&&%........(...*,%/.%((*/ 
                   /....,*,.....%&&&&&&%#%*,,/####%&%&%%,......*......*#//(/*   
                   *,*.........../&%&%&%#,,,,,,##%&&&&%....../.........         
            * *....    ,*........./*....,*,,,(&%&&%%(.................          
          ,  /             .//..*........../%&&%/...............,*.#//.         
                             .*...........,....................,##,,,,,/        
                             *.........../...................#%&(,,,,,,,        
                             *........,,....................%%%%,,,,,,*         
                            ...................**.*....#&&&%&%&#,,,,.,          
                            *....................,...(%&&&&&&&&&,,*/            
                            *.............,,*,,**//(&%&%&&&&&&&&%&              
                            ,(,......./&&&&&&&&&&&&&&&&&&&%&%%*                 
                             &&&&&&&&&&&&&&&&&&&&&&&%&&%/.                      
                              %%&%&&&&&&&&&&&&&&%&/,(  .                        
                               ,%&&&&%&&&&&#,                                   
                                   ,,,,,,*                                      
                                  ,,,,,,,,                                      
                                   ,,,,,(                                      
=========================================================================
========== 💰 Have I helped you in any way? All I ask is a tip! 🧾 ======
========== ✨ Faça sua boa ação de hoje, manda aquela gorjeta! 😊 =======
=========================================================================
======================== vvv BCOIN BUSD BNB vvv =========================
============== 0xbd06182D8360FB7AC1B05e871e56c76372510dDf ===============
=========================================================================
===== https://www.paypal.com/donate?hosted_button_id=JVYSC6ZYCNQQQ ======
=========================================================================

>>---> Press ctrl + c to kill the bot.

>>---> Some configs can be found in the config.yaml file.

"""

def addRandomness(n, randomn_factor_size=None):
    """Returns n with randomness
    Parameters:
        n (int): A decimal integer
        randomn_factor_size (int): The maximum value+- of randomness that will be
            added to n

    Returns:
        int: n with randomness
    """

    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    # logger('{} with randomness -> {}'.format(int(n), randomized_n))
    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)


def remove_suffix(input_string, suffix):
    """Returns the input_string without the suffix"""

    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images(dir_path='./targets/'):
    """ Programatically loads all images of dir_path as a key:value where the
        key is the file name without the .png suffix

    Returns:
        dict: dictionary containing the loaded images as key:value pairs.
    """

    file_names = listdir(dir_path)
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets

def load_users():
    with open('users_list.txt') as f:
        users = f.readlines()

    return users

def clickBtn(img, timeout=3, threshold = ct['default']):
    logger(None, progress_indicator=True)
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(img, threshold=threshold)

        if(len(matches) == 0):
            has_timed_out = time.time() - start > timeout
            continue

        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        return True

    return False

def printScreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:,:,:3]

def positions(target, threshold=ct['default'],img = None):
    if img is None:
        img = printScreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def comment():
    numbers_used = []
    if clickBtn(images['input_coment'], timeout = 10):
        logger('Selecionado o campo de comentário')
        for i in range(num_users_in_comment):
            randomNumber = randrange(len(users))
            while numbers_used.__contains__(randomNumber):
                randomNumber = randrange(len(users))
            numbers_used.append(randomNumber)
            actualUser = users[randomNumber]
            logger('Digitando comentário: ' + actualUser)
            for letra in actualUser:
                wsh.SendKeys(letra)
                time.sleep(0.1)

            wsh.SendKeys(" ")
        if clickBtn(images['botao_comentar'], timeout = 10):
            logger('Comentário publicado')
            

def main():
    """Main execution setup and loop"""
    # ==Setup==

    global images
    global users
    global wsh
    global num_users_in_comment
    users = load_users()
    images = load_images()
    wsh = comclt.Dispatch("WScript.Shell")
    num_users_in_comment = int(input("Digite a quantidade de pessoas por comentário: "))
    

    # print(cat)
    time.sleep(7)
    t = c['time_intervals']

    last = {
        "comment" : 0
    }
    # =========

    while True:
        now = time.time()

        if now - last["comment"] > addRandomness(t['comment_interval_seconds']):
            last["comment"] = now
            comment()

        #clickBtn(teasureHunt)
        logger(None, progress_indicator=True)

        sys.stdout.flush()
        time.sleep(1)

if __name__ == '__main__':
    main()