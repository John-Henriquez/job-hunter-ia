from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def fetch_jobs(self):
        """
        Obtiene vacantes desde una fuente externa.
        """
        pass