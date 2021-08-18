import numpy as np

count_file: int = 10000
range_start: int = 1
range_end: int = count_file + 1

params_aof = {
    "appendonly": ["boolean", ["yes", "no"], None],
    "appendfsync": ["categorical", ['always', 'everysec', 'no'], None],
    "auto-aof-rewrite-percentage": ["numerical", [str(i) for i in range(50,201)], None],
    "auto-aof-rewrite-min-size": ['numerical', ['{}mb'.format(i) for i in range(16,257)], None],
    "no-appendfsync-on-rewrite": ['boolean', ['yes', 'no'], None],
    "aof-rewrite-incremental-fsync": ['boolean', ['yes', 'no'], None],
    "aof-use-rdb-preamble": ['boolean', ['yes', 'no'], None]
}

params_rdb = {
    # "save": ['string', [3,[[700, 1200],[1, 20]], [[100, 500],[1, 50]], [[300, 900],[7500, 12500]]], []],
    "save": ['numerical', [3,
                                [[str(i) for i in range(700,1101)],[str(i) for i in range(1,10)]],
                                [[str(i) for i in range(100,501)],[str(i) for i in range(10,101)]],
                                [[str(i) for i in range(30,91)],[str(i) for i in range(8000,12001)]]], []],
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
    "maxmemory": ['numerical', ['{}gb'.format(round(i,1)) for i in np.arange(1.0,3.0,0.1)],None],
    "maxmemory-policy": ["categorical", ["volatile-lru", "allkeys-lru", "volatile-lfu", "allkeys-lfu", "volatile-random",
                                         "allkeys-random", "volatile-ttl", "noeviction"], None],
    "maxmemory-samples": ['numerical', [str(i) for i in range(3,8)], None],
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
    "hash-max-ziplist-entries": ['numerical', [str(i) for i in range(256,751)], None],
    "hash-max-ziplist-value": ['numerical', [str(i) for i in range(16,257)], None],
    "activerehashing": ['boolean', ['yes', 'no'], None],
    "hz": ['numerical', [str(i) for i in range(1,41)], None],
    "dynamic-hz": ['boolean', ['yes', 'no'], None]
}

