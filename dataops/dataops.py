from src.helpers.monitor import Monitoring


class DataOps:
    def __init__(
        self,
        temporal_folder: str = r"data\landing\temporal",
        persistent_folder: str = r"data\landing\persistent",
    ):
        self._monitoring = Monitoring(interval=5)
        self.temporal_folder = temporal_folder
        self.persistent_folder = persistent_folder

        self.layers = self._load_layers()

    def _load_layers(self) -> None:
        pass
