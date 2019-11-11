from app import Config, Satis
from os import path
import utils

try:
    print('正在初始化...')
    config = Config()
    satis = Satis(config)

    # 登录私有仓库
    print('登录私有仓库')
    satis.registry_login()

    # 验证镜像是否存在，不存在重新拉取
    print('验证镜像有效性')
    satis.image_check_exists()

    # 请求外部接口生成的satis.json，并写入本地
    print('正在获取外部接口...')
    response = utils.links_satis(config.external_url)
    if response.status_code != 200:
        raise Exception(response.reason)

    print('同步配置')
    with open(path.abspath('./factory/satis.json'), 'wb') as fb:
        for context in response.iter_content():
            fb.write(context)

    # 生产satis私有库
    print('正在构建私有仓库...')
    satis.factory_satis({
        path.abspath('./factory/satis.json'): {
            'bind': '/build/satis.json',
            'mode': 'ro'
        },
        path.abspath('./factory/composer'): {
            'bind': '/composer',
            'mode': 'rw'
        },
        path.abspath('./factory/public'): {
            'bind': '/build/public',
            'mode': 'rw'
        }
    })
    print('构建成功')
except Exception as message:
    exit(message)
