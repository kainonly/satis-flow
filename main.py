import os
import configparser
import docker

config = configparser.ConfigParser()
config.read('config.ini')

client = docker.from_env()
client.login(
    username=config['docker']['username'],
    password=config['docker']['password'],
    registry=config['docker']['registry']
)
repository = config['docker']['repository']
image = client.images.get(repository)
if image is None:
    client.images.pull(repository)

result = client.containers.run(
    image=repository,
    command='build ./satis.json ./public',
    init=True,
    auto_remove=True,
    volumes={
        os.path.abspath('./factory/satis.json'): {
            'bind': '/build/satis.json',
            'mode': 'ro'
        },
        os.path.abspath('./factory/composer'): {
            'bind': '/composer',
            'mode': 'rw'
        },
        os.path.abspath('./factory/public'): {
            'bind': '/build/public',
            'mode': 'rw'
        }
    },
    working_dir='/build'
)
