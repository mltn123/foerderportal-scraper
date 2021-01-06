# -*- encoding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import subprocess
import argparse
from threading import Thread
import threading

import sys
from time import sleep
from tqdm.auto import tqdm, trange
import os


umlautdict = {
     r'ä': 'ae',
     r'ü': 'ue',
     r'ö':'oe',
    }

global items
items = 0

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stadt", nargs = '*', default=None, help="Stadt/Gemeinde", required=True)
parser.add_argument("-b", "--bundesland",nargs = '*', default="", help="Bundesland", required=False)
parser.add_argument("-l", "--laufzeit", default="", help="Laufzeit von", required=False)
# parser.add_argument("-v", "--verbund", default=False, action='store_true', help="nur Verbundprojekte")
parser.add_argument("-lfd", "--lfdvorhaben", default=False, action='store_true', help="Nur lfd. Vorhaben")
parser.add_argument("-t", "--threads", default=5, help="Parallele Threads")
options = parser.parse_args()




maxthreads = int(options.threads)
print(maxthreads)
sema = threading.Semaphore(value=maxthreads)



def run(x):
    save_location = x
    currentdir = os.getcwd()


    #sema = threading.BoundedSemaphore(maxthreads)
    sema.acquire()
    for item in umlautdict.keys():
        save_location = save_location.replace(item, umlautdict[item])


    path = currentdir + '\\Output\\'+ str(save_location) + "\\"
    #print(path)

    # Set Firefox preferences so that the file automatically saves to disk when downloaded
    if not os.path.exists('Output'):
        os.makedirs('Output')
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.preferences.instantApply",True)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
    fp.set_preference("browser.helperApps.alwaysAsk.force",False)
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.dir", currentdir + "\\Output\\" + str(save_location) + "\\"  )
    fp.set_preference("browser.download.downloadDir", currentdir + "\\Output\\" + str(save_location) + "\\"  )
    fp.set_preference("browser.download.defaultFolder", currentdir + "\\Output\\" + str(save_location) + "\\"  )


    driver = webdriver.Firefox(firefox_profile=fp)


    driver.get("https://foerderportal.bund.de/foekat/jsp/SucheAction.do?actionMode=searchmask")









    # elem.clear()

    # bundesland.send_keys(options.bundesland)
    for i in range(len(options.bundesland)-1):
        driver.find_element_by_css_selector('#gemeindeZeile > td:nth-child(7) > input:nth-child(1)').click()
    for i in range(len(options.bundesland)):
        driver.find_element_by_css_selector(f'#suche_bundeslandSuche_{i}_').send_keys(options.bundesland[i])




    if options.lfdvorhaben == False:
        driver.find_element_by_css_selector('#suche_lfdVhbN').click()
    driver.find_element_by_css_selector('#suche_nurVerbundJ').click()
    submit_button = driver.find_element_by_css_selector("#suche_general_search")


    driver.find_element_by_css_selector("#suche_gemeindeSuche_0_").send_keys(x)
    # bundesland = driver.find_element_by_css_selector('#suche_bundeslandSuche_0_')
    driver.find_element_by_css_selector('#suche_laufzeitVonSuche_0_').send_keys(options.laufzeit)
    submit_button.click()



    items = driver.find_element_by_css_selector(".content_background_outer > h1:nth-child(3)").text #cosmetics
    items = int("".join(filter(str.isdigit, str(items)))) #cosmetics

    with tqdm(total=items) as progress_bar:
        select = Select(WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'listselect_suche_listrowfrom'))))
        progress = len(select.options)
        for index in range(len(select.options)):
            select = Select(WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'listselect_suche_listrowfrom'))))
            select.select_by_index(index)
            percentage = (index / progress) * 100
        #    print ("" + sys.argv[1] +  " "+ str(percentage) + "%")

        #    verbundprojekte = len(driver.find_elements_by_partial_link_text('J'))
            verbundprojekte = len(driver.find_elements_by_css_selector("[title^='Detailansicht von Förderkennzeichen']"))
            #print (verbundprojekte)

            for index in range((verbundprojekte)):
                progress_bar.update(1) # update progress
                try:


                        #counter = counter + 1
                        #print(str(counter) + "/" + "max." + str((progress*10)))
                        #link = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.PARTIAL_LINK_TEXT, 'J')))[index].click()
                        WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "[title^='Detailansicht von Förderkennzeichen']")))[index].click() # Detailansicht
                        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sucheVerbund > a:nth-child(3)'))).click() #verbundliste
                        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.nobreak_hz:nth-child(4)'))).click() #download
                        #breakpoint()
                        driver.execute_script("window.history.go(-3)")





                        attempts = 0
                        while attempts < 5:
                            try:
                                select = Select(WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'listselect_suche_listrowfrom'))))
                                attempts +=1
                            except StaleElementReferenceException as ex:
                                select = Select(WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, 'listselect_suche_listrowfrom'))))
                                #print ("stale")
                                continue
                            except NoSuchElementException as ex:
                            #    print("NoSuchElement " + str(ex))

                                continue

                except TimeoutException as ex:
                #    print("Timeout " + str(ex))
                    # driver.back()
                    # driver.back()
                    driver.execute_script("window.history.go(-2)")
                    continue

                except NoSuchElementException as ex:
                #    print("NoSuchElement " + str(ex))
                    driver.execute_script("window.history.go(-2)")
                    continue
        select = Select(WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'listselect_suche_listrowfrom'))))
    subprocess.call('copy *.csv merged.csv', shell=True, cwd=path)
    driver.close()
    sema.release()


for i in range(len(options.stadt)):
    threads = []
    thread = Thread(target=run, args=(options.stadt[i],))
    threads.append(thread)
    for x in threads:
        x.start()
