import logging
import os
from io import StringIO

import boto3
from dotenv import dotenv_values


class Configuration:
    __config_singleton: dict = None
    __mode: str = os.getenv("ENV")

    def __init__(self, configs: dict = None):
        if configs is None:
            current_folder = os.path.dirname(os.path.abspath(__file__))
            env_file = os.path.join(current_folder, "..", ".env")
            if not os.path.exists(env_file):
                config_stream = StringIO(Configuration.get_from_aws_secret_manager())
                configs = dotenv_values(stream=config_stream)
            else:
                logging.debug(f"Loading configs from {env_file}")
                configs = dotenv_values(os.path.join(current_folder, "..", ".env"))
        self.__configs = configs

    @classmethod
    def get_instance(cls):
        if cls.__config_singleton is None:
            cls.__config_singleton = Configuration()
        return cls.__config_singleton

    def get(self, key: str):
        assert (
            key in self.__configs
        ), f'Key {key} not found {self.__configs if self.in_development_mode() else ""}'
        return self.__configs[key]

    @classmethod
    def in_development_mode(cls):
        return cls.__mode == "development"

    @staticmethod
    def get_aws_iam_credentials():
        if os.path.exists(
            os.path.join(os.path.dirname(__file__), "..", ".credentials.env")
        ):
            dotenv_path = os.path.join(
                os.path.dirname(__file__), "..", ".credentials.env"
            )
        elif Configuration.__mode == "development":
            dotenv_path = os.path.join(
                os.path.dirname(__file__), "..", ".credentials.env.development"
            )
        elif Configuration.__mode == "production":
            dotenv_path = os.path.join(
                os.path.dirname(__file__), "..", ".credentials.env.production"
            )
        else:
            raise Exception("ENV not set, expecting: development or production")
        credentials = dotenv_values(dotenv_path)
        return credentials

    @staticmethod
    def get_from_aws_secret_manager():
        credentials = Configuration.get_aws_iam_credentials()
        session = boto3.session.Session(
            aws_access_key_id=credentials["accessKeyId"],
            aws_secret_access_key=credentials["secretAccessKey"],
            region_name=credentials["region"],
        )
        session.client("sts").get_caller_identity()

        client = session.client(
            service_name="secretsmanager", region_name=credentials["region"]
        )

        get_secret_value_response = client.get_secret_value(
            SecretId=credentials["secreteName"]
        )
        secret = get_secret_value_response["SecretString"]
        return secret

    @property
    def mongodb__connection_string(self):
        return self.get("mongodb__connection_string")

    @property
    def mongodb__database_name(self):
        return self.get("mongodb__database_name")
