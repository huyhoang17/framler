import os
import yaml
import subprocess

import requests
from tqdm import tqdm

from framler.log import get_logger

logger = get_logger(__name__)


def load_config():
    fpath = os.path.join(
        os.path.dirname(__file__), "config.yaml")
    with open(fpath) as f:
        cfg = yaml.load(f)

    return cfg


def req_files(req, fpath):
    with open(fpath, 'wb') as handle:
        for block in tqdm(req.iter_content(1024)):
            handle.write(block)


def download_driver():
    cfg = load_config()["driver"]

    try:
        req = requests.get(cfg["download_link"], stream=True)
        req.raise_for_status()
    except Exception as e:
        logger.exception(e)
        return

    untar_fd = os.path.join(os.path.expanduser('~'), cfg["untar_folder"])
    if not os.path.exists(untar_fd):
        os.makedirs(untar_fd)

    # download file using requests
    tarname = cfg["download_link"].split('/')[-1]
    tarname = os.path.join(untar_fd, tarname)
    req_files(req, tarname)

    # untar file
    fname = os.path.join(untar_fd, tarname)
    tar_cmd = "tar -xvzf " + fname + " -C " + untar_fd
    subprocess.call(tar_cmd.split())
    logger.info("Untar completed!")
