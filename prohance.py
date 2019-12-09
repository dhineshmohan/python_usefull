from time import sleep
import datetime
import re
import json
import redis
from rq import use_connection
from configparser import ConfigParser
import shlex, subprocess

def check_time():
    current_time = datetime.datetime.now()
    current_time = str(current_time)[11:]
    time_elements = []
    time_elements = current_time.split(':')
    if int(time_elements[0]) >= 25:
        write_log("Its 08:00 PM hence killing the script")
        write_log("#SCRIPT END")
        return True

def get_manager_id(mana_list):
    cfg = ConfigParser()
    cfg.read('/home/dhinesh/Credentials/Prohance/managerListCfg.ini')
    manager = mana_list.pop()
    write_log("Manger assined for this task is "+manager)
    mana_list.insert(0, manager)
    mana_id = cfg.get('selector', manager)
    return mana_id, mana_list

def write_log(msg):
    date = datetime.datetime.now()
    date = str(date)[:10]
    date = re.sub(r'-', '_', date, re.I|re.S)
    filename = '/home/dhinesh/Prohance/Logs/prohance_logs_' + date + '.log'
    msg = 'KFetcher:' + str(datetime.datetime.now()) + ': ' + msg + "\n"
    with open(filename, "a") as f:
        f.write(msg)



index = ''
non_bank_list = ['Muzammil', 'Bindu', 'Chandrakala', 'Vanita']
bank_list = ['Shankar', 'Harishkumar', 'Varun', 'Peter', 'Premkumar', 'Sahana', 'Shilpa', 'Shivanna', 'Shobha', 'Shreedevi', 'Sreedhara']
while(True) :
    my_connection = redis.StrictRedis(host='localhost', port=6379, db=0, password=None)
    if (check_time()) :
        break
    result = my_connection.lpop('test_qu')
    if (result == None):
        write_log("Queue is empty. Sleeping")
        sleep(5)
    else:
        try:
            res_obj = re.search(r'^b\'(.*?)\'$', str(result), re.I)
            result = res_obj.group(1)
            write_log("JSON found for the task - "+str(result))
            input_data = json.loads(result)
            if input_data['processingType'] == 'STATEMENT':
                manager_id, bank_list = get_manager_id(bank_list)
            elif input_data['processingType'] == 'Financial Statement' or input_data['processingType'] == 'ITRV Statement':
                manager_id, non_bank_list = get_manager_id(non_bank_list)
            txt = open('/home/dhinesh/Credentials/Prohance/serial')
            index = txt.read()
            index = int(index) + 1
            write_log("Index for this task - "+str(index))
            try:
                arguments = str(result) + "\n" + str(manager_id) + "\n" + str(index)
                write_log("#START_TASK_CREATION")
                p = subprocess.Popen(['perl', 'task.pl', arguments], stdout=subprocess.PIPE)
            except Exception as e:
                print ("Exception occurred :"+str(e))
        except Exception as e:
            print ("Exception occurred : "+str(e))