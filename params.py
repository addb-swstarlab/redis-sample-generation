import numpy as np

#count_file: int = 5000

# evaluate default configuration
count_file: int = 5
range_start: int = 1
range_end: int = count_file + 1

params_addb = {
    "lazyfree-lazy-eviction": ["boolean", ["yes", "no"], None],
    "lazyfree-lazy-expire": ["boolean", ["yes", "no"], None],
    "lazyfree-lazy-server-del": ["boolean", ["yes", "no"], None],
    "auto-aof-rewrite-min-size": ['boolean', ["yes", "no"], None],
    "hash-max-ziplist-value": ['numerical', [str(i) for i in range(16,257)], None],
    "activerehashing": ['boolean', ['yes', 'no'], None],
    "hz": ['numerical', [str(i) for i in range(1,76)], None]
}

