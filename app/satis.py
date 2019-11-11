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

    def factory_satis(self, volumes: dict):
        return self.client.containers.run(
            image=self._config.repository,
            command='build ./satis.json ./public',
            init=True,
            auto_remove=True,
            volumes=volumes,
            working_dir='/build'
        )
