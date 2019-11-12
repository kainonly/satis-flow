import docker
from .config import Config


class Satis:
    def __init__(self, config: Config):
        self._config = config
        self.client = docker.DockerClient(
            base_url=config.base_url
        )

    def factory_satis(self, volumes: dict):
        return self.client.containers.run(
            image=self._config.repository,
            command='build ./satis.json ./public',
            init=True,
            auto_remove=True,
            volumes=volumes,
            working_dir='/build'
        )
