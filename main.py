from func import *
from metrics import *
from params import *
from memtier import dict_cmd

from func import parsingExternalData

import time
import argparse
import os, subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, choices=['light','heavy'], default = 'light', help='diff workload request')
parser.add_argument("--persistence", type=str, choices=['aof','rdb'], default = 'aof', help='Redis persistence')

args = parser.parse_args()

if args.persistence == 'rdb':
    count_file += 10000
    range_start += 10000
    range_end += 10000


def main():
    RESULT_INTERNAL_FILE = "result_" + args.persistence + "_internal_" + str(instance_count)+".csv"
    RESULT_EXTERNAL_FILE = "result_" + args.persistence + "_external_" + str(instance_count)+".csv"
    MODE = "w"

    FILE_LENGTH = 1
    '''
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

    nf = open(args.persistence+"_nan_log.txt",MODE)
    in_f = open(RESULT_INTERNAL_FILE, MODE)
    ex_f = open(RESULT_EXTERNAL_FILE, MODE)

    if args.persistence == 'aof':
        internal_metrics_list = internal_metrics_list_aof
    else:
        internal_metrics_list = internal_metrics_list_rdb


    if MODE == "w":
        ResultMetricsName_GeneratorFile(internal_metrics_list, in_f)
        ResultMetricsName_GeneratorFile(external_metrics_list, ex_f)

    range_start_ = range_start + FILE_LENGTH - 1

    for i in range(range_start_, range_end):
        #redis 서버 실행
        connect_redis = ['/home/jieun/redis-5.0.2/src/redis-server','configfile/config{}.conf'.format(str(i))]
        fd_popen = subprocess.Popen(connect_redis, stdout=subprocess.PIPE)

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

        external_list = parsingExternalData(outs)

        ResultMetricsValue_GeneratorFile(external_list, external_metrics_list, ex_f)
        print(f"---saving {str(i)}th sample results on result_external_{str(instance_count)}")

        if not memtier_results:
            nf.write(str(i)+'\n')

        # "redis-cli info" excute
        cmd = ['/home/jieun/redis-5.0.2/src/redis-cli', 'info'] 
        fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout  
        data = fd_popen.readlines() 

        internal_dict = InternalMetrics_IntoDict(data)
        internal_list = []

        for metric in internal_metrics_list:
            if metric in internal_dict:
                internal_list.append(internal_dict[metric])
            else:
                internal_list.append("")
        
        ResultMetricsValue_GeneratorFile(internal_list, internal_metrics_list, in_f)
        print(f"---saving {str(i)}th sample results on result_internal_{str(instance_count)}")

        os.system("/home/jieun/redis-5.0.2/src/redis-cli shutdown")

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
