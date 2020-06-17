import os
import sys
import time
from utils.likes import *
from utils.wall import *
import pickle
import vk_api

headers = dict(Authorization="",
               Cookie="")

root = "collected_data/"
os.makedirs(root, exist_ok=True)

def get_all_posts_from_folder(folder):
    posts = []
    files = os.listdir(folder)
    for i, name in enumerate(files):
        path = os.path.join(folder, name)
        posts.extend(get_all_posts(path))
        print(f"[i] Getting posts: {i / len(files) * 100: .3f}%")

    with open("collected_data/posts/all", "wb") as f:
        pickle.dump(posts, f, 2)
    return sys.getsizeof(posts)


def check_posts_friends_like(posts_filename, root_dir, chunk_size=200):
    path_to_progress_file = os.path.join(root_dir, "progress")
    path_to_result_file = os.path.join(root_dir, "liked_posts")
    progress_saver = []
    result = {}
    with open(posts_filename, "r") as f:
        posts = f.read().split(';')

    print(f"Posts count - {len(posts)}")

    if os.path.exists(path_to_progress_file):
        with open(path_to_progress_file, "rb") as f:
            progress_saver = pickle.load(f)

    if os.path.exists(path_to_result_file):
        with open(path_to_result_file, "rb") as f:
            result = pickle.load(f)

    for i in range(0, len(posts), chunk_size):
        if i in progress_saver:
            continue
        start_time = time.time()
        posts_chunk = [k.replace('post', 'wall') for k in posts[i: i + chunk_size]]
        # print(posts_chunk)
        r = get_friends_likes(posts_chunk, headers)
        if r:
            print(r)

        result.update(r)
        progress_saver.append(i)

        with open(path_to_progress_file, "wb") as f:
            pickle.dump(progress_saver, f, 2)

        with open(path_to_result_file, "wb") as f:
            pickle.dump(result, f, 2)
        delta = time.time() - start_time
        print(f"[i] Checking friend's likes - {i / len(posts) * 100: .2f}% - {delta: .3f} s - {len(result)}")


check_posts_friends_like(os.path.join(root, "all_posts"), root, 100)

#
# target_id = <secret>
# api = vk_api.VkApi(
#     token="<secret>").get_api()
#
# groups = api.groups.get(user_id=target_id, count=1000, extended=1)['items']
# groups = list(filter(lambda x: not x['is_closed'] and not x.get('deactivated'), groups))
# print(len(groups))
# groups = [i['id'] for i in groups]
# wall_count = get_wall_count(groups)
# with open(os.path.join(root, "wall_count"), "wb") as f:
#     pickle.dump(wall_count, f)
#
# print(sum(wall_count.values()))
# ##############


# checked_groups = list(map(lambda x: int(x.split('.')[0]), os.listdir('collected_data/wall')))
# with open(os.path.join(root, "wall_count"), "rb") as f:
#     wall_count = pickle.load(f)
#
# wall_count = {k: v for k, v in sorted(wall_count.items(), key=lambda x: x[1])}
# print(len(wall_count))
# print(set(wall_count.keys()).intersection(set(checked_groups)))
# for i in checked_groups:
#     if i in wall_count:
#         wall_count.pop(i)
#
# print(len(wall_count))
# with open(os.path.join(root, "wall_count"), "wb") as f:
#     pickle.dump(wall_count, f)

