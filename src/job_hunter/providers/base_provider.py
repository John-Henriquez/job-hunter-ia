from abc import ABC, abstractmethod
from job_hunter.normalizers.base_normalizer import BaseNormalizer


class BaseProvider(ABC):

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Identificador único del proveedor"""
        pass

    @property
    @abstractmethod
    def source_version(self) -> str:
        """Versión del provider"""
        pass

    @property
    def is_active(self) -> bool:
        """Permite desactivar un provider sin eliminarlo."""
        return True

    @abstractmethod
    def fetch_jobs(self) -> list:
        """Obtiene vacantes crudas desde la fuente externa."""
        pass

    @abstractmethod
    def parse_jobs(self, raw_jobs: list) -> list[dict]:
        """Convierte las vacantes crudas en un formato estandarizado."""
        pass

    @abstractmethod
    def get_normalizer(self) -> BaseNormalizer:
        """Retorna el normalizer asociado a este provider."""
        pass