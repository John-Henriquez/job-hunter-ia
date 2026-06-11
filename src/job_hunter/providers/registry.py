from job_hunter.providers.base_provider import BaseProvider


class ProviderRegistry:

    def __init__(self):
        self._providers: dict[str, BaseProvider] = {}

    def register(self, provider: BaseProvider) -> None:
        if not provider.is_active:
            print(f"[Registry] Provider '{provider.source_name}' inactivo, omitido.")
            return
        self._providers[provider.source_name] = provider
        print(f"[Registry] Provider '{provider.source_name}' v{provider.source_version} registrado.")

    def get_all(self) -> list[BaseProvider]:
        return list(self._providers.values())

    def get_by_name(self, name: str) -> BaseProvider | None:
        return self._providers.get(name)

    def list_registered(self) -> list[str]:
        return list(self._providers.keys())