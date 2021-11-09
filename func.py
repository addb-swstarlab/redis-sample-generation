from io import TextIOWrapper
import random
import os
from params import params_rdb, count_file, light_params_maxmemory, heavy_params_maxmemory

'''
gen_config function
 - determine_dict
 - random_choice
 - config_generator
 - file_generator
'''

# parameters dict 
def determine_dict(params: list, params_dict: dict, mode: str, idx: int) -> dict:
    params_aof, params_rdb, params_activedefrag, params_etc = params
    params_dict = params_etc.copy()

    if idx < count_file/2:
        persis_choice = 'aof'
    else:
        persis_choice = 'rdb'

    if persis_choice == 'aof':  ## chocie AOF
        params_aof['appendonly'][2] = 'yes'
        params_dict.update(params_aof)

    elif persis_choice == 'rdb':  ## choice RDB
        save_message_list = []
        for i in range(params_rdb['save'][1][0]):
            seconds_range: int = params_rdb['save'][1][i+1][0]
            changes_range: int = params_rdb['save'][1][i+1][1]
            seconds = random.choice(seconds_range)
            changes = random.choice(changes_range)
            save_message = str(seconds)+' '+str(changes)
            save_message_list.append(save_message)

        params_rdb['save'][2] = save_message_list
        params_dict.update(params_rdb)

    activedefrag_choice = random.choice(['yes', 'no'])
    if activedefrag_choice == 'yes':
        params_activedefrag['activedefrag'][2] = 'yes'
        params_dict.update(params_activedefrag)

    if mode == "light":
        params_dict.update(light_params_maxmemory)
    elif mode == "heavy":
        params_dict.update(heavy_params_maxmemory)

    return params_dict

def random_choice(dict: dict) -> dict:
    for name, list in dict.items():
        if name == "appendonly":
            continue
        elif name == 'save':
            continue
        elif name == 'activedefrag':
            continue
        elif list[0] == "boolean":
            list[2] = random.choice(list[1])
        elif list[0] == "categorical":
            list[2] = random.choice(list[1])
        elif list[0] == "numerical":
           list[2] = random.choice(list[1])
        elif list[0] == 'numerical_range':
            list[2] = str(random.randint(list[1][0], list[1][1]))
    return dict

def config_generator(conf_file: str, dict_: dict, mode: str) -> str:
    value = 0
    for name, list in dict_.items():
        if name == 'save':
            save_message_list = params_rdb['save'][2]
            for i in range(params_rdb['save'][1][0]):
                conf_file += ("\n"+"save "+save_message_list[i])
        elif list[0] == "boolean":
            conf_file += ("\n" + name + " " + list[2])
        elif list[0] == 'categorical':
            if name == 'maxmemory-policy' and list[2] == 'noeviction' and mode == 'heavy':
                if value and value < 2.5:
                    conf_file = conf_file.replace("maxmemory " + str(value) + "gb", "maxmemory 2.5gb")
            conf_file += ("\n" + name + " " + list[2])
        elif list[0] == 'numerical':
            if name == "maxmemory":
                value = float(list[2][:-2])
            conf_file += ("\n" + name + " " + list[2])
        elif list[0] == 'numerical_range':
            conf_file += ("\n" + name + " " + list[2])
    
    return conf_file

#file indexing
def index_size(index):
  size = len(str(count_file))
  index_str = str(index)
  diff = size - len(index_str)
  index_value = ''
  for _ in range(diff):
    index_value += '0'
  index_value += index_str
  
  return index_value

def file_generator(file_name: str, dir: str, file_content: str, file_extension: str):
    if not os.path.exists(dir):
        os.mkdir(dir)
    f = open(dir + file_name + "." + file_extension, 'w')
    f.write(file_content)
    f.close()

def metrics_name_gen_file(metrics_list: list, f: TextIOWrapper):
    col_length = len(metrics_list)

    f.write(metrics_list[0])
    for i in range(1, col_length):
        f.write(','+metrics_list[i])
    f.write('\n')


def metrics_value_gen_file(result_list: list, f: TextIOWrapper):
    for i in range(len(result_list)):
        if i == 0:
            f.write(result_list[0])
            continue
        f.write(','+result_list[i])
    f.write('\n')

def EMs_to_list(external_data):
    external_list = []

    for data in external_data:
        data = data.decode('utf-8')
        list_ = data.split(' ')
        list_ = ' '.join(list_).split()
    
        for i in range(1, len(list_)):  # list = ['Sets', , , ...]
            external_list.append(list_[i]) # 문자열

    external_list = [i.replace('---','') for i in external_list]
    
    return external_list


def IMs_to_dict(internal_data: list) -> dict:
    dict = {}

    keyspace_data: bytes = internal_data.pop()
    keyspace_data: str = keyspace_data.decode('utf-8')
    keyspace_list: list = keyspace_data.split(',')

    for data in internal_data:
        data = data.decode('utf-8')
        if data[0] == '#' or data == '\r\n':
            continue
        list_ = data.split(':')
        list_[1] = list_[1].replace('\r', '').replace('\n', '')
        if list_[1][-1] == 'K' or list_[1][-1] == 'M' or list_[1][-1] == '%' or list_[1][-1] == 'G' or list_[1][-1] == 'B':
            list_[1] = list_[1][0:len(list_[1])-1]
        dict[list_[0]] = list_[1]  # 문자열
    
    for data in keyspace_list:
        list_ = data.split('=')
        list_[1] = list_[1].replace('\r', '').replace('\n', '')
        dict[list_[0]] = list_[1]
    
    return dict 

def parsing_EM(outputs: bytes) -> list:
    if len(outputs) == 0:
        return ['0']*32
    parsedOutput = outputs.decode('utf-8').split("\n")

    First = True
    save = False
    external_data = []
    for po in parsedOutput:
        if po.startswith("-"):
            if First:
                save = True
                First = False
                continue
            else:
                save =False
                break
        if save:
            try:
                datas = po.split()
                if datas[0] == "Sets":
                    external_data.extend(datas[1:])
                elif datas[0] == "Gets":
                    external_data.extend(datas[1:])
                elif datas[0] == "Waits":
                    external_data.extend(datas[1:])
                elif datas[0] == "Totals":
                    external_data.extend(datas[1:])
            except:
                external_list = [i.replace('---','') for i in external_data]

    return external_list


    
    
