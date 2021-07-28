from func import *
from metrics import *
from params import *
import argparse
import os, subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, choices=['light','heavy'], default = 'heavy', help='diff workload request')

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

count_file=2000
config_list = [init_config for _ in range(count_file)]

for i in range(count_file):
    params_dict = {}
    params_dict = determine_dict(params_aof,params_rdb, params_activedefrag, 
                                params_etc, params_dict,args.mode, i)
    # print(f"i={i}\n params_dict={params_dict}\n")
    config_list[i] = config_generator(config_list[i], random_choice(params_dict),args.mode)
    # config_list[i] += "\nlogfile "+"'./logfile/logfile"+"%s'" %index_size(i)
    
# conf file generate step
for i in range(count_file):
    index = range(1, 2001)
    file_generator("config" + str(index[i]), './configfile2/',config_list[i], "conf")
