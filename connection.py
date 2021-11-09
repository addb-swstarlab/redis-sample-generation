from func import parsing_EM, metrics_name_gen_file, metrics_value_gen_file, IMs_to_dict
from params import *
import metrics
from memtier import dict_cmd

import time
import argparse
import os, subprocess

"""
mode: maxmemory params mode (params.py)
persistence
 - AOF: 명령 수행마다 기록
 - RDB: Snapshot type
"""

parser = argparse.ArgumentParser()
parser.add_argument("persistence", type=str, choices=['aof','rdb'], default = 'aof', help='Redis persistence')
parser.add_argument('target', type=int)
parser.add_argument("path", type=str)
args = parser.parse_args()

def main():
    '''
    GA config에 benchmark를 적용
    '''
    instance_count = args.target
    RESULT_INTERNAL_FILE = "result_" + args.persistence + "_internal_GA.csv"
    RESULT_EXTERNAL_FILE = "result_" + args.persistence + "_external_GA.csv"
    MODE = "w"

    FILE_LENGTH = 1
    '''
        비정상 종료로 인하여 파일이 존재하는 경우, 존재하는 파일로 추가
        if the file exists because of abnormal shutdown, appending with exist files
        no file: FILE_LENGTH = 1
        existed file : FILE_LENGTH > 1
    '''
    if os.path.isfile(RESULT_EXTERNAL_FILE) and os.path.isfile(RESULT_INTERNAL_FILE):
        print('Exist Those Files')
        MODE = "a"
        in_rf = open(RESULT_INTERNAL_FILE, "r")
        ex_rf = open(RESULT_EXTERNAL_FILE, "r")
        FILE_LENGTH = len(in_rf.readlines())
        assert FILE_LENGTH == len(ex_rf.readlines())
        in_rf.close()
        ex_rf.close()

    in_f = open(RESULT_INTERNAL_FILE, MODE)
    ex_f = open(RESULT_EXTERNAL_FILE, MODE)

    if args.persistence == 'aof':
        internal_metrics_list = metrics.internal_metrics_list_aof
    else:
        internal_metrics_list = metrics.internal_metrics_list_rdb


    if MODE == "w":
        metrics_name_gen_file(internal_metrics_list, in_f)
        metrics_name_gen_file(metrics.external_metrics_list, ex_f)

    #redis 서버 실행
    connect_redis = ['/home/jieun/redis-5.0.2/src/redis-server', args.path]
    server_popen = subprocess.Popen(connect_redis, stdout=subprocess.PIPE)

    time.sleep(5)
    # memtier_benchmark 실행
    cmd = dict_cmd[instance_count]
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    memtier_results = True
    outs = []
    try:
        outs, _ = fd_popen.communicate(timeout=10000)
    except subprocess.TimeoutExpired:
        memtier_results = False
        fd_popen.kill()

    external_list = parsing_EM(outs)
    metrics_value_gen_file(external_list, ex_f)
    print(f"---saving sample results on result_external_default")

    if not memtier_results:
        internal_list = ['0'] * len(internal_metrics_list)
        metrics_value_gen_file(internal_list, internal_metrics_list, in_f)
        print(f"---saving th sample results on result_internal_default")
    else:
        # "redis-cli info" excute
        cmd = ['/home/jieun/redis-5.0.2/src/redis-cli', 'info'] 
        fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout  
        data = fd_popen.readlines() 

        internal_dict = IMs_to_dict(data)
        internal_list = []

        for metric in internal_metrics_list:
            if metric in internal_dict:
                internal_list.append(internal_dict[metric])
            else:
                internal_list.append("")
        
        metrics_value_gen_file(internal_list, internal_metrics_list, in_f)
        print(f"---saving  sample results on result_internal_default")

    if memtier_results:
        os.system("/home/jieun/redis-5.0.2/src/redis-cli shutdown")
    else:
        server_popen.kill()

    # # 캐시 비우기
    cmd = ['sudo', 'echo', '3', '>', '/proc/sys/vm/drop_caches']
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    time.sleep(3)

    os.system("rm -rf /home/jieun/redis-logs/appendonly.aof")
    os.system("rm -rf /home/jieun/redis-logs/dump.rdb")
    os.system("rm -rf /home/jieun/redis-logs/temp*")

    time.sleep(3)
    del outs

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        os.system("/home/jieun/redis-5.0.2/src/redis-cli shutdown")
        os.system("rm -rf /home/jieun/redis-logs/appendonly.aof")
        os.system("rm -rf /home/jieun/redis-logs/dump.rdb")
        os.system("rm -rf /home/jieun/redis-logs/temp*")

        with open('error_log', 'w') as ef:
            print(e)
            ef.write(str(e))
