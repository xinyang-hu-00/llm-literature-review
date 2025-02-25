import os
from typing import Literal

import yaml

from deepsearcher.embedding.base import BaseEmbedding
from deepsearcher.llm.base import BaseLLM
from deepsearcher.loader.file_loader.base import BaseLoader
from deepsearcher.loader.web_crawler.base import BaseCrawler
from deepsearcher.vector_db.base import BaseVectorDB

current_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_YAML_PATH = os.path.join(current_dir, "..", "config.yaml")

FeatureType = Literal["llm", "embedding", "file_loader", "web_crawler", "vector_db"]


class Configuration:
    def __init__(self, config_path: str = DEFAULT_CONFIG_YAML_PATH):
        # Initialize default configurations
        config_data = self.load_config_from_yaml(config_path)
        self.provide_settings = config_data["provide_settings"]
        self.query_settings = config_data["query_settings"]
        self.load_settings = config_data["load_settings"]

    def load_config_from_yaml(self, config_path: str):
        with open(config_path, "r") as file:
            return yaml.safe_load(file)

    def set_provider_config(self, feature: FeatureType, provider: str, provider_configs: dict):
        """
        Set the provider and its configurations for a given feature.

        :param feature: The feature to configure (e.g., 'llm', 'file_loader', 'web_crawler').
        :param provider: The provider name (e.g., 'openai', 'deepseek').
        :param provider_configs: A dictionary with configurations specific to the provider.
        """
        if feature not in self.provide_settings:
            raise ValueError(f"Unsupported feature: {feature}")

        self.provide_settings[feature]["provider"] = provider
        self.provide_settings[feature]["config"] = provider_configs

    def get_provider_config(self, feature: FeatureType):
        """
        Get the current provider and configuration for a given feature.

        :param feature: The feature to retrieve (e.g., 'llm', 'file_loader', 'web_crawler').
        :return: A dictionary with provider and its configurations.
        """
        if feature not in self.provide_settings:
            raise ValueError(f"Unsupported feature: {feature}")

        return self.provide_settings[feature]


class ModuleFactory:
    def __init__(self, config: Configuration):
        self.config = config

    def _create_module_instance(self, feature: FeatureType, module_name: str):
        
        class_name = self.config.provide_settings[feature]["provider"]
        module = __import__(module_name, fromlist=[class_name])
        class_ = getattr(module, class_name)
        print(self.config.provide_settings[feature]["config"])
        return class_(**self.config.provide_settings[feature]["config"])

    def create_llm(self) -> BaseLLM:
        return self._create_module_instance("llm", "deepsearcher.llm")

    def create_embedding(self) -> BaseEmbedding:
        return self._create_module_instance("embedding", "deepsearcher.embedding")

    def create_file_loader(self) -> BaseLoader:
        return self._create_module_instance("file_loader", "deepsearcher.loader.file_loader")

    def create_web_crawler(self) -> BaseCrawler:
        return self._create_module_instance("web_crawler", "deepsearcher.loader.web_crawler")

    def create_vector_db(self) -> BaseVectorDB:
        return self._create_module_instance("vector_db", "deepsearcher.vector_db")


config = Configuration()

module_factory: ModuleFactory = None
llm: BaseLLM = None
embedding_model: BaseEmbedding = None
file_loader: BaseLoader = None
vector_db: BaseVectorDB = None
web_crawler: BaseCrawler = None


def init_config(config: Configuration):
    global module_factory, llm, embedding_model, file_loader, vector_db, web_crawler
    module_factory = ModuleFactory(config)
    llm = module_factory.create_llm()
    embedding_model = module_factory.create_embedding()
    file_loader = module_factory.create_file_loader()
    web_crawler = module_factory.create_web_crawler()
    vector_db = module_factory.create_vector_db()
