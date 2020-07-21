from common import Config, Oss
import requests
from os import path, walk, unlink, mkdir
import platform
import subprocess
from time import time
import json

try:
    config = Config()
    oss = Oss(config)
    public_path = 'public'
    if path.exists(public_path) is False:
        mkdir(public_path)

    response = requests.get(config.external_url)
    if response.status_code != 200:
        raise Exception(response.reason)

    with open('./satis.json', 'wb') as fb:
        fb.write(response.content)

    if platform.system() == 'Windows':
        subprocess.run(['satis\\bin\\satis.bat', '--verbose', 'build', 'satis.json', public_path])
    else:
        subprocess.run(['php', 'satis/bin/satis', '--verbose', 'build', 'satis.json', public_path])

    exists_objects = []
    for data in oss.find('composer'):
        exists_objects.append(data.key)

    if exists_objects:
        oss.delete(exists_objects)

    origin_index = path.join(public_path, 'index.html')

    if path.exists(origin_index):
        unlink(origin_index)

    with open(path.join(public_path, 'info.json'), 'wb') as fb:
        fb.write(json.dumps({"build": time()}).encode())

    objects = []
    for root, dirs, files in walk(public_path):
        for file in files:
            oss.add(
                path.normpath(
                    path.join('composer', path.relpath(root, public_path), file)
                ).replace('\\', '/'),
                path.join(root, file)
            )

except Exception as message:
    exit(message)
