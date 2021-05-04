from func import *
from metrics import *
from params import *
import argparse
import os, subprocess

<<<<<<< HEAD
parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, choices=['light','heavy'], default = 'light', help='diff workload request')

args = parser.parse_args()

def main():

=======
def main():

>>>>>>> b849812c352762e614922a16c23efc78dd8c2930
    # original conf file copy
    init_config = ""

    # readline_all.py
    f = open("init_config.conf", 'r')
    while True:
        line = f.readline()
        if not line: break
        init_config += line
    f.close()


    config_list = [init_config for _ in range(count_file)]

    for i in range(count_file):
        params_dict = {}
        params_dict = determine_dict(params_aof,params_rdb, params_activedefrag, 
                                    params_etc, params_dict,args.mode, i)
        # print(f"i={i}\n params_dict={params_dict}\n")
        config_list[i] = config_generator(config_list[i], random_choice(params_dict))
        # config_list[i] += "\nlogfile "+"'./logfile/logfile"+"%s'" %index_size(i)
        
    # conf file generate step
    for i in range(count_file):
        index = range(range_start, range_end)
        file_generator("config" + str(index[i]), './configfile/',config_list[i], "conf")


    RESULT_INTERNAL_FILE = "result_internal_"+str(instance_count)+".csv"
    RESULT_EXTERNAL_FILE = "result_external_"+str(instance_count)+".csv"
    MODE = "w"

    FILE_LENGTH = 1

    '''
        if the file exists because of abnormal shutdown, appending with exist files
        no file: FILE_LENGTH = 1
        existed file : FILE_LENGTH > 1
    '''
    if os.path.isfile(RESULT_EXTERNAL_FILE) and os.path.isfile(RESULT_INTERNAL_FILE):
        print('exist those files')
        MODE = "a"
        in_rf = open(RESULT_INTERNAL_FILE, "r")
        ex_rf = open(RESULT_EXTERNAL_FILE, "r")
        FILE_LENGTH = len(in_rf.readlines())
        assert FILE_LENGTH == len(ex_rf.readlines())
        in_rf.close()
        ex_rf.close()


    in_f = open(RESULT_INTERNAL_FILE, MODE)
    ex_f = open(RESULT_EXTERNAL_FILE, MODE)


    if MODE == "w":
        ResultMetricsName_GeneratorFile(internal_metrics_list, in_f)
        ResultMetricsName_GeneratorFile(external_metrics_list, ex_f)


    range_start_ = range_start + FILE_LENGTH - 1

    for i in range(range_start_, range_end):
        #redis 서버 실행
        #os.system("/home/jieun/redis-5.0.2/src/redis-server "+"configfile/config"+str(i)+".conf")
        connect_redis = ['/home/jieun/redis-5.0.2/src/redis-server','configfile/config{}.conf'.format(str(i))]
        fd_popen = subprocess.Popen(connect_redis, stdout=subprocess.PIPE).stdout

        # memtier_benchmark 실행
        cmd = ['/home/jieun/memtier_benchmark/memtier_benchmark', '--request=1000', '--clients=1', '--thread=1', '--data-size=128', '--key-minimum=10000000', '--key-maximum=99999999', '--ratio=1:1']
        fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout

        external_data = []
        for j in range(13):
            data = fd_popen.readline() 
            if j >= 9:
                external_data.append(data)

        external_list = ExternalMetrics_IntoList(external_data)

        ResultMetricsValue_GeneratorFile(external_list, external_metrics_list, ex_f)
        print(f"---saving {str(i)}th sample results on result_external_{str(instance_count)}")

        # # 캐시 비우기
        cmd = ['sudo', 'echo', '3', '>', '/proc/sys/vm/drop_caches']
        fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout  

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
        os.system("rm -rf /home/jieun/redis-logs/appendonly.aof")
        os.system("rm -rf /home/jieun/redis-logs/dump.rdb")
        os.system("rm -rf /home/jieun/redis-logs/temp*")


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
