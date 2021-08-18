from func import (determine_dict, config_generator, random_choice, file_generator)
from metrics import *
from params import (params_aof, params_rdb, params_activedefrag, params_etc)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, choices=['light', 'heavy'], default = 'heavy', help='diff workload request')

args = parser.parse_args()

# original conf file copy
init_config = ""

# readline_all.py
f = open("init_config.conf", 'r')
while True:
    line = f.readline()
    if not line: break
    init_config += line
f.close()

count_file = 2000
config_list = [init_config for _ in range(count_file)]

params = [params_aof, params_rdb, params_activedefrag, params_etc]
for i in range(count_file):
    params_dict = {}
    params_dict = determine_dict(params, params_dict, args.mode, i)
    config_list[i] = config_generator(config_list[i], random_choice(params_dict), args.mode)
    
# conf file generate step
for i in range(count_file):
    index = range(1, 2001)
    file_generator("config" + str(index[i]), './configfile2/',config_list[i], "conf")
