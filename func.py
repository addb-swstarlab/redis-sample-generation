import random
import os
from params import *


def determine_dict(params_aof, params_rdb, params_activedefrag, params_etc, params_dict):

    params_dict = params_etc.copy()
    # print(f"params_etc={params_etc}\n")
    persis_choice = random.choice(['aof', 'rdb'])  ## random choice persistence
    # print('persis_choice=', persis_choice)
    if persis_choice == 'aof':  ## chocie AOF
        # print('this is aof')
        params_aof['appendonly'][2] = 'yes'
        params_dict.update(params_aof)

    elif persis_choice == 'rdb':  ## choice RDB
        # print('this is rdb')
        save_message_list = []
        for i in range(params_rdb['save'][1][0]):
            seconds_range = params_rdb['save'][1][i+1][0]
            changes_range = params_rdb['save'][1][i+1][1]
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

    return params_dict


def random_choice(dict):
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
        elif list[0] == "numerical_categorical":
           list[2] = random.choice(list[1])
        elif list[0] == 'numerical_range':
            list[2] = str(random.randint(list[1][0], list[1][1]))
    return dict


def config_generator(conf_file, dict):
    for name, list in dict.items():
        if name == 'save':
            save_message_list = params_rdb['save'][2]
            for i in range(params_rdb['save'][1][0]):
                conf_file += ("\n"+"save "+save_message_list[i])
        elif list[0] == "boolean":
            conf_file += ("\n" + name + " " + list[2])
        elif list[0] == 'categorical':
            conf_file += ("\n" + name + " " + list[2])
        elif list[0] == 'numerical_categorical':
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

def file_generator(filename, dir, filecontent, fileextension):
    f = open(dir + filename + "." + fileextension, 'w')
    f.write(filecontent)
    f.close()


def ResultMetricsName_GeneratorFile(metrics_list, f):
    col_length = len(metrics_list)

    f.write(metrics_list[0])
    for i in range(1, col_length):
        f.write(','+metrics_list[i])
    f.write('\n')


def ResultMetricsValue_GeneratorFile(result_list, metrics_list, f):
    col_length = len(metrics_list)

    for i in range(len(result_list)):
        if i == 0:
            f.write(result_list[0])
            continue
        f.write(','+result_list[i])
    f.write('\n')


def ExternalMetrics_IntoList(external_data):
    external_list = []

    for data in external_data:
        data = data.decode('utf-8')
        list = data.split(' ')
        list = ' '.join(list).split()
    
        for i in range(1, 6):  # list = ['Sets', , , ...]
            external_list.append(list[i]) # 문자열

    external_list = [i.replace('---','') for i in external_list]
    
    return external_list


def InternalMetrics_IntoDict(internal_data):
    dict = {}

    keyspace_data = internal_data.pop()
    keyspace_data = keyspace_data.decode('utf-8')
    keyspace_list = keyspace_data.split(',')

    for data in internal_data:
        data = data.decode('utf-8')
        if data[0] == '#' or data == '\r\n':
            continue
        list = data.split(':')
        list[1] = list[1].replace('\r', '').replace('\n', '')
        if list[1][-1] == 'K' or list[1][-1] == 'M' or list[1][-1] == '%' or list[1][-1] == 'G' or list[1][-1] == 'B':
            list[1] = list[1][0:len(list[1])-1]
        dict[list[0]] = list[1]  # 문자열
    
    for data in keyspace_list:
        list = data.split('=')
        list[1] = list[1].replace('\r', '').replace('\n', '')
        dict[list[0]] = list[1]
    
    return dict 

