import os
import time
import pickle
from utils.wall import *


with open("collected_data/wall_count", "rb") as f:
    table = pickle.load(f)
print(table)
table = {k: v for k, v in sorted(table.items(), key=lambda x: x[1])}
table = {k: v for k, v in table.items() if v != 0}

for i, n in enumerate(table.items()):
    group_id, count = n
    print(f"Progress {i} / {len(table)} ({i / len(table) * 100: .2f}%) - {count}")
    if os.path.exists(f"collected_data/wall/{group_id}.html"):
        continue
    start_time = time.time()
    all_html = get_all_raw_wall(group_id, count)
    with open(f"collected_data/wall/{group_id}.html", "w") as f:
        f.write(all_html)
    delta = time.time() - start_time
    print(f"Progress - {delta: .3f} s - {count / delta: .3f} pps")
