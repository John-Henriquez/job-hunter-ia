from abc import ABC, abstractmethod
from job_hunter.models.job import Job


class BaseNormalizer(ABC):

    @abstractmethod
    def normalize(self, raw_payload: dict) -> Job | None:
        """
        Transforma un raw_payload en una entidad Job.
        Retorna None si el payload es inválido.
        """
        pass