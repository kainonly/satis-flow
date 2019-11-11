import os
import docker
from .config import Config


class Satis:
    def __init__(self, config: Config):
        self._config = config
        self.client = docker.DockerClient(
            base_url=config.base_url
        )

    def registry_login(self) -> dict:
        return self.client.login(
            username=self._config.username,
            password=self._config.password,
            registry=self._config.registry
        )

    def image_check_exists(self):
        repository = self._config.repository
        image = self.client.images.get(repository)
        if image is None:
            self.client.images.pull(repository)

    def factory_satis(self):
        return self.client.containers.run(
            image=self._config.repository,
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
