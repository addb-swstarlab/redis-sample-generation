instance_count = 1
count_file = 700
range_start = instance_count * count_file + 1 # 0 * 6250 + 1 = 1
range_end = (instance_count + 1) * count_file + 1 # (0 + 1) * 6250 + 1 = 6251

params_aof = {
    "appendonly": ["boolean", ["yes", "no"], None],
    "appendfsync": ["categorical", ['always', 'everysec', 'no'], None],
    "auto-aof-rewrite-percentage": ["numerical_categorical", ['50', '100', '150', '200'], None],
    "auto-aof-rewrite-min-size": ['numerical_categorical', ['16mb', '32mb', '64mb', '128mb'], None],
    "no-appendfsync-on-rewrite": ['boolean', ['yes', 'no'], None],
    "aof-rewrite-incremental-fsync": ['boolean', ['yes', 'no'], None],
    "aof-use-rdb-preamble": ['boolean', ['yes', 'no'], None]
}

params_rdb = {
    # "save": ['string', [3,[[700, 1200],[1, 20]], [[100, 500],[1, 50]], [[300, 900],[7500, 12500]]], []],
    "save": ['numerical_categorical', [3,[['700', '900', '1100'],['1', '5']], [['100','300', '500'],['10', '50']], [['30', '60', '90'],['10000', '15000']]], []],
    "rdbcompression": ['boolean', ['yes', 'no'], None],
    "rdbchecksum": ['boolean', ['yes', 'no'], None],
    "rdb-save-incremental-fsync": ['boolean', ['yes', 'no'], None]
}

params_activedefrag = {
    "activedefrag": ['boolean', ['yes', 'no'], None],
    "active-defrag-threshold-lower": ['numerical_categorical', ['10','30'], None],
    "active-defrag-threshold-upper": ['numerical_categorical', ['70','100'], None],
    "active-defrag-cycle-min": ["numerical_categorical", ['5', '25'], None],
    "active-defrag-cycle-max": ['numerical_categorical', ['50','75'], None]
}

# params_maxmemory = {
#     "maxmemory": ['numerical_categorical', ['1gb', '2gb', '3gb', '4gb', '5gb', '6gb', '7gb', '8gb', '9gb', '10gb'],
#                   None],
#     "maxmemory-policy": ["categorical", ["volatile-lru", "allkeys-lru", "volatile-lfu", "allkeys-lfu", "volatile-random",
#                                          "allkeys-random", "volatile-ttl", "noeviction"], None],
#     "maxmemory-samples": ['numerical_range', [1, 10], None]
# }

params_etc = {
    # "loglevel": ["categorical", ['debug', 'verbose', 'notice', 'warning'], None],
    # "lazyfree-lazy-eviction": ['boolean', ['yes', 'no'], None],
    # "lazyfree-lazy-expire": ['boolean', ['yes', 'no'], None],
    # "lazyfree-lazy-server-del": ['boolean', ['yes', 'no'], None],
    "hash-max-ziplist-entries": ['numerical_categorical', ['128','256', '512', '1024'], None],
    "hash-max-ziplist-value": ['numerical_categorical', ['16','32', '64', '128'], None],
    "activerehashing": ['boolean', ['yes', 'no'], None],
    "hz": ['numerical_categorical', ['1', '10','40','80'], None]
    # "dynamic-hz": ['boolean', ['yes', 'no'], None]
}

