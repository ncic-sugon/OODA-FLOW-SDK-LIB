import os
import argparse
import glob
import shutil
from tqdm import trange, tqdm
import time


def main(job_id, user_name, log_id):
    src_O2_path = "/home/newnfs/liu1234/data/O2_result"

    src_A4_path = "/home/newnfs/liu1234/data/A4_result"

    dst_O2_path = "/home/newnfs/%s/jobs/%s/O2_result" % (user_name, job_id)

    dst_A4_path = "/home/newnfs/%s/jobs/%s/A4_result" % (user_name, job_id)

    cat_log_path = "/home/newnfs/%s/jobs/%s/log" % (user_name, log_id)

    if not os.path.exists(dst_A4_path):
        os.makedirs(dst_A4_path)

    if not os.path.exists(dst_O2_path):
        os.makedirs(dst_O2_path)
    if not os.path.exists(os.path.join(dst_O2_path, "airport")):
        os.mkdir(os.path.join(dst_O2_path, "airport"))

    if not os.path.exists(os.path.join(dst_O2_path, "harbor")):
        os.mkdir(os.path.join(dst_O2_path, "harbor"))

    for item in tqdm(glob.glob("{}/*.jpg".format(os.path.join(src_O2_path, "airport")), recursive=True)):
        shutil.copyfile(item, os.path.join(os.path.join(dst_O2_path, "airport"), os.path.basename(item)))

    for item in tqdm(glob.glob("{}/*.jpg".format(os.path.join(src_O2_path, "harbor")), recursive=True)):
        shutil.copyfile(item, os.path.join(os.path.join(dst_O2_path, "harbor"), os.path.basename(item)))

    for item in tqdm(glob.glob("{}/*.jpg".format(src_A4_path), recursive=True)):
        shutil.copyfile(item, os.path.join(dst_A4_path, os.path.basename(item)))

    if os.path.exists(cat_log_path):
        with open(cat_log_path, "r") as fr:
            for line in fr.readlines():
                print(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-job_id", '--job_id', type=str)
    parser.add_argument("-user_name", '--user_name', type=str, default="admin")
    parser.add_argument("-log_id", "--log_id", type=str, default="20200514-detection")
    args = parser.parse_args()
    job_id = args.job_id
    user_name = args.user_name
    log_id = args.log_id
    main(job_id, user_name, log_id)
