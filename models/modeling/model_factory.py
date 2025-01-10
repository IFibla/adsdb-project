from abc import abstractmethod, ABC


class ModelFactory(ABC):
    @abstractmethod
    def get_instance(self):
        pass

    @abstractmethod
    def get_model_filename(self):
        pass