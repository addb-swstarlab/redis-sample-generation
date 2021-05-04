import os
try:
    import numpy as np
except:
    os.system("pip3 install --user numpy")
    import numpy as np

instance_count = 1
count_file = 10 # 20000
range_start = 1
range_end = count_file + 1
# range_start = instance_count * count_file + 1 # 0 * 6250 + 1 = 1
# range_end = (instance_count + 1) * count_file + 1 # (0 + 1) * 6250 + 1 = 6251

params_aof = {
    "appendonly": ["boolean", ["yes", "no"], None],
    "appendfsync": ["categorical", ['always', 'everysec', 'no'], None],
    "auto-aof-rewrite-percentage": ["numerical", [str(i) for i in range(50,301)], None],
    "auto-aof-rewrite-min-size": ['numerical', ['{}mb'.format(i) for i in range(32,513)], None],
    "no-appendfsync-on-rewrite": ['boolean', ['yes', 'no'], None],
    "aof-rewrite-incremental-fsync": ['boolean', ['yes', 'no'], None],
    "aof-use-rdb-preamble": ['boolean', ['yes', 'no'], None]
}

params_rdb = {
    # "save": ['string', [3,[[700, 1200],[1, 20]], [[100, 500],[1, 50]], [[300, 900],[7500, 12500]]], []],
    "save": ['numerical', [3,
                                [[str(i) for i in range(700,1101)],[str(i) for i in range(1,10)]],
                                [[str(i) for i in range(100,501)],[str(i) for i in range(10,101)]],
                                [[str(i) for i in range(30,91)],[str(i) for i in range(8000,12501)]]], []],
    "rdbcompression": ['boolean', ['yes', 'no'], None],
    "rdbchecksum": ['boolean', ['yes', 'no'], None],
    "rdb-save-incremental-fsync": ['boolean', ['yes', 'no'], None]
}

params_activedefrag = {
    "activedefrag": ['boolean', ['yes', 'no'], None],
    "active-defrag-threshold-lower": ['numerical', [str(i) for i in range(1,31)], None],
    "active-defrag-threshold-upper": ['numerical', [str(i) for i in range(70,101)], None],
    "active-defrag-cycle-min": ["numerical", [str(i) for i in range(1,31)], None],
    "active-defrag-cycle-max": ['numerical', [str(i) for i in range(70,91)], None]
}

heavy_params_maxmemory = {
    "maxmemory": ['numerical', ['{}gb'.format(round(i,1)) for i in np.arange(2.5,5.0,0.1)],None],
    "maxmemory-policy": ["categorical", ["volatile-lru", "allkeys-lru", "volatile-lfu", "allkeys-lfu", "volatile-random",
                                         "allkeys-random", "volatile-ttl", "noeviction"], None],
    "maxmemory-samples": ['numerical', [str(i) for i in range(1,21)], None],
    "lazyfree-lazy-eviction": ["boolean", ["yes", "no"], None],
    "lazyfree-lazy-expire": ["boolean", ["yes", "no"], None],
    "lazyfree-lazy-server-del": ["boolean", ["yes", "no"], None],
}

light_params_maxmemory = {
    "maxmemory": ['numerical', ['2gb'], None],
    "maxmemory-policy": ["categorical", ["noeviction"], None],
    "maxmemory-samples": ['numerical', ['5'], None],
    "lazyfree-lazy-eviction": ["boolean", ["no"], None],
    "lazyfree-lazy-expire": ["boolean", ["no"], None],
    "lazyfree-lazy-server-del": ["boolean", ["no"], None],
}

params_etc = {
    # "loglevel": ["categorical", ['debug', 'verbose', 'notice', 'warning'], None],
    # "lazyfree-lazy-eviction": ['boolean', ['yes', 'no'], None],
    # "lazyfree-lazy-expire": ['boolean', ['yes', 'no'], None],
    # "lazyfree-lazy-server-del": ['boolean', ['yes', 'no'], None],
    "hash-max-ziplist-entries": ['numerical', [str(i) for i in range(128,1025)], None],
    "hash-max-ziplist-value": ['numerical', [str(i) for i in range(16,257)], None],
    "activerehashing": ['boolean', ['yes', 'no'], None],
    "hz": ['numerical', [str(i) for i in range(1,101)], None]
    # "dynamic-hz": ['boolean', ['yes', 'no'], None]
}

