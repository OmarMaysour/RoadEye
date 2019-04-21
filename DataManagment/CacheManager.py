import abc


class CacheManager(abc.ABC):
    @abc.abstractmethod
    def cache(self, dto):
        pass

    @abc.abstractmethod
    def get_oldest_cache(self):
        pass

    @abc.abstractmethod
    def delete_cache(self, dto):
        pass
