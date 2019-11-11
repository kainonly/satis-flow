from app import Config, Satis, Oss
from os import path, walk, unlink, mkdir
from json import dumps
from time import time
import utils

try:
    print('初始化...')
    config = Config()
    satis = Satis(config)
    oss = Oss(config)

    satis_path = path.abspath('./factory/satis.json')
    public_path = path.abspath('./factory/public')
    composer_path = path.abspath('./factory/composer')

    if path.exists('./factory') is False:
        mkdir('./factory')

    if path.exists(public_path) is False:
        mkdir(public_path)

    if path.exists(composer_path) is False:
        mkdir(composer_path)

    print('登录私有仓库')
    satis.registry_login()

    print('验证镜像有效性')
    satis.image_check_exists()

    print('正在获取外部接口...')
    response = utils.links_satis(config.external_url)
    if response.status_code != 200:
        raise Exception(response.reason)

    print('同步配置')
    with open(satis_path, 'wb') as fb:
        for context in response.iter_content():
            fb.write(context)

    print('正在构建私有仓库...')
    satis.factory_satis({
        satis_path: {
            'bind': '/build/satis.json',
            'mode': 'ro'
        },
        composer_path: {
            'bind': '/composer',
            'mode': 'rw'
        },
        public_path: {
            'bind': '/build/public',
            'mode': 'rw'
        }
    })
    build_time = time()
    print('构建成功')

    print('检测对象存储是否存在对应文件')
    exists_objects = []
    for data in oss.find('composer'):
        exists_objects.append(data.key)
    if exists_objects:
        oss.delete(exists_objects)
    origin_index = path.join(public_path, 'index.html')
    if path.exists(origin_index):
        unlink(origin_index)

    print('正在上传至对象存储')
    objects = []
    for root, dirs, files in walk(public_path):
        for file in files:
            oss.add(
                path.normpath(
                    path.join('composer', path.relpath(root, public_path), file)
                ).replace('\\', '/'),
                path.join(root, file)
            )
    print('上传完成')

    sync_time = time()
    with open(path.join(public_path, 'info.json'), 'wb') as fb:
        fb.write(dumps({
            "build-time": build_time,
            "sync-time": sync_time
        }).encode())
    print('流程完毕')
except Exception as message:
    exit(message)
