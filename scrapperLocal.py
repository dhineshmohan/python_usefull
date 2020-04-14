from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_actions import WebDriverActions
from time import sleep
import datetime
import os
import sys
import logging
import re
import json

html_page_count = 0

def initialise_driver(proxy_flag):
    webdriver_actions = WebDriverActions(proxy_flag)  # creating an object of the webdriver_actions class
    driver = webdriver_actions.init_driver("chrome", "/usr/bin/chromedriver",{"profile.managed_default_content_settings.images":2, "disk-cache-size":4096}, 1)  # creating a driver object with the specified conditions
    driver.set_window_size(1920, 1080)
    return webdriver_actions, driver

def write_file(contents, index):
    global html_page_count
    html_page_count += 1
    date = datetime.datetime.now()
    date = str(date)[:10]
    date = re.sub(r'-', '_', date, re.I|re.S)
    filename = 'output' + str(html_page_count) + '.html'
    filepath = '/home/dhinesh/Prohance/data/prohance_data/' + date + '/' + index + '/' + filename
    print (filepath)
    #/home/dhinesh/Prohance/data/prohance_data/2018_12_31
    with open(filepath, "w") as f:
        f.write(contents)


def get_json(input_data):
    process_json = '{"bank_statement" : {"process_template" : "Bank Statement Template", "process_type" : "Bank Statement", "process_catagory" : "Bank Statement Processing", "serial_pref" : "BANK"}, "final_statement" : {"process_template" : "Financial Statement Template", "process_type" : "Financial Statement", "process_catagory" : "Financial Statement Processing", "serial_pref" : "FIN"}, "itr_statement" : {"process_template" : "ITR Statement Template", "process_type" : "Financial Statement", "process_catagory" : "Financial Statement Processing", "serial_pref" : "ITR"} }'
    process_data = json.loads(process_json)
    
    req_json = {}
    if input_data['processingType'] == 'STATEMENT':
        req_json = process_data['bank_statement']
    elif input_data['processingType'] == 'Financial Statement':
        req_json = process_data['final_statement']
    elif input_data['processingType'] == 'ITRV Statement Template':
        req_json = process_data['itr_statement']
    return req_json

def do_login(driver, webdriver_actions, index):
    driver.get("http://eagle.hinagro.com:8080/prohance/")
    write_file(driver.page_source, index)
    login_id_element = webdriver_actions.is_element_present(driver, id="tlogin")
    password_element = webdriver_actions.is_element_present(driver, id="tpwd")
    login_id_element.send_keys('narayanan.p')
    password_element.send_keys('falcon$999')
    login_button = webdriver_actions.is_button_clickable(driver, "/html/body/div[2]/div/div/div[1]/div/form/div[2]/div/div/input")
    login_button.click()
    sleep(2)
    write_file(driver.page_source, index)

    session_active_obj = re.search(r'There\s+is\s+another\s+session\s+active\s+with\s+the\s+same\s+username.*?Would\s+you\s+like', driver.page_source, re.I|re.S)
    if session_active_obj:
        logging.info ("Previous session is still active. Hence terminating")
        terminate_button = webdriver_actions.is_button_clickable(driver, '//*[@id="loadContent"]/div/div/div[4]/div/div/input')
        terminate_button.click()
        sleep(2)
        write_file(driver.page_source, index)
    logging.info("Logging fine")

def get_task_create_page(driver, webdriver_actions, index):
    workflow_link = webdriver_actions.is_button_clickable(driver, '/html/body/div[4]/div[1]/div/div/ul[1]/li[4]/a')
    workflow_link.click()
    sleep(2)
    logging.info("Clicking on workflow link")
    write_file(driver.page_source, index)

    work_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="swipe-area"]')))
    work_link.click()
    sleep(2)
    logging.info("Clicking on side menu bar")
    write_file(driver.page_source, index)

    process_link = webdriver_actions.is_button_clickable(driver, '//*[@id="level2_139"]/li[4]')
    process_link.click()
    sleep(2)
    logging.info("Clicking on process management link")
    write_file(driver.page_source, index)

    driver.switch_to.frame(driver.find_element_by_name('contentFrame'))
    #sleep(3)
    write_file(driver.page_source, index)

def select_from_dropdown(button, value):
    for option in button.find_elements_by_tag_name("option"):
        if value in option.text:
            option.click()
            break

def fill_form(driver, webdriver_actions, req_json, input_data, index):
    process_tem_button = webdriver_actions.is_button_clickable(driver, '//*[@id="templateId"]')
    process_tem_button.click()
    select_from_dropdown(process_tem_button, req_json['process_template'])
    id_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'projectName')))
    id_element.send_keys(input_data['perfiosTransactionId'])

    serial_no_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'refCode')))
    serial_num = req_json['serial_pref'] + index
    logging.info (serial_num)
    serial_no_element.send_keys(serial_num)

    descr_element = webdriver_actions.is_button_clickable(driver, '//*[@id="right_table"]/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr[4]/td[2]/div/textarea')
    descr_element.send_keys(input_data['downloadUrl'])

    env_button = webdriver_actions.is_button_clickable(driver, '//*[@id="complexityId"]')
    env_button.click()
    select_from_dropdown(env_button, input_data['environment'])

    process_type_button = webdriver_actions.is_button_clickable(driver, '//*[@id="typeId"]')
    process_type_button.click()
    select_from_dropdown(process_type_button, req_json['process_type'])

    process_ctgy_button = webdriver_actions.is_button_clickable(driver, '//*[@id="categoryId"]')
    process_ctgy_button.click()
    select_from_dropdown(process_ctgy_button, req_json['process_catagory'])
    
    driver.execute_script('document.getElementsByName("endDate")[0].removeAttribute("readonly")')
    end_date_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'endDate')))
    today = datetime.datetime.now()
    today = str(today)[:10]
    today = datetime.datetime.strptime(today, '%Y-%m-%d').strftime('%d %b %Y')
    end_date_element.send_keys(str(today))

    hour_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'projectHours')))
    hour_element.send_keys('2')

    window_before = driver.window_handles[0]
    mana_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/form/div[2]/div/table[1]/tbody/tr/td[2]/table/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr[10]/td[2]/span[1]/a/img')))
    if not mana_element:
        logging.error ("Not able to find the element")
    else:
        mana_element.click()
    driver.switch_to.default_content()
    window_after = driver.window_handles[1]
    driver.switch_to_window(window_after)
    sleep(2)
    write_file(driver.page_source, index)

    radio_select = driver.find_element_by_css_selector(req_json['manager'])
    radio_select.click()

    add_button = webdriver_actions.is_button_clickable(driver, '//*[@id="bodyDiv"]/div[1]/form/div[2]/div/table/tbody/tr/td[2]/button')
    add_button.click()
    sleep(2)
    driver.switch_to_window(window_before)
    logging.info("Feilds are filled completely")

    driver.switch_to.frame(driver.find_element_by_name('contentFrame'))
    write_file(driver.page_source, index)

def add_task(driver, webdriver_actions, req_json, input_data, index):
    #sleep(4)
    addnew_link = webdriver_actions.is_button_clickable(driver, '//*[@id="headerTable"]/div[2]/span/span[3]')
    addnew_link.click()
    logging.info("Clicking on add new task button")
    sleep(2)

    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element_by_name('contentFrame'))
    #sleep(3)
    write_file(driver.page_source, index)

    fill_form(driver, webdriver_actions, req_json, input_data, index)

    save_button = webdriver_actions.is_button_clickable(driver, '/html/body/div[1]/form/div[2]/div/table[1]/tbody/tr/td[2]/table/tbody/tr/td/table[2]/tbody/tr/td/input[2]')
    save_button.click()
    sleep(2)
    write_file(driver.page_source, index)

    id_exists_obj = re.search(r'Process.*?cannot\s+be\s+added\s+as\s+it\s+already\s+exists', driver.page_source, re.I|re.S)
    if id_exists_obj:
        print ("Cant create task, task already exist")
        logging.error("Cant create task, process already exist")
    else:
        logging.info("Task created successfully")

    driver.switch_to.default_content()
    contents = driver.page_source
    write_file(driver.page_source, index)

def do_logout(driver, webdriver_actions, index):
    driver.get("http://eagle.hinagro.com:8080/prohance/session.do")
    sleep(2)
    write_file(driver.page_source, index)
    logging.info("Logged out successfully")
    print ("Logged out")



def create_task_by_scrapping(input_data, manager_id, index):
    logging.info ("Creating task for "+str(input_data))
    global html_page_count
    html_page_count = 0
    #input_data = json.loads(res)
    req_json = get_json(input_data)
    req_json["manager"] = manager_id
    webdriver_actions, driver = initialise_driver(0)
    do_login(driver, webdriver_actions, index)
    get_task_create_page(driver, webdriver_actions, index)
    add_task(driver, webdriver_actions, req_json, input_data, index)
    do_logout(driver, webdriver_actions, index)
    driver.quit()
