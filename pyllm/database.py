# Copyright (c) 2023, Haoxus Tech Corp. (15408440) and/or its affiliates,
# All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

import datetime
import hashlib
import json
import logging
import numbers
import traceback

import pymongo
from bson import json_util

from pyllm import enums
from pyllm.configuration import Configuration


class DbInstance:
    __instance_singleton = None

    @classmethod
    def get_instance(cls, new_instance=False):
        if cls.__instance_singleton is None or new_instance:
            cls.__instance_singleton = pymongo.MongoClient(
                Configuration.get_instance().mongodb__connection_string
            )[Configuration.get_instance().mongodb__database_name]
        return cls.__instance_singleton

    @classmethod
    def to_json(cls, cursor):
        return json_util.dumps(
            {item: value for item, value in cursor.items() if not item.startswith("_")},
            indent=2,
            default=str,
        )

    @classmethod
    def collection(cls, collection_name):
        return cls.get_instance()[collection_name]

    @classmethod
    def get_cache(cls, key):
        hashed_key = cls.get_hash(key)
        try:
            cached = cls.collection(enums.Common.cache_table).find_one(
                {enums.Common.hashed_key: hashed_key}
            )
            if cached is None:
                return None
            return cached[enums.Common.value]
        except IndexError:
            return None

    @staticmethod
    def get_hash(string: str):
        assert isinstance(string, str)
        hash_obj = hashlib.sha256(string.encode("utf-8"))
        hashed_key = hash_obj.hexdigest()
        return hashed_key

    @classmethod
    def set_cache(cls, key, value):
        hashed_key = cls.get_hash(key)

        cls.collection(enums.Common.cache_table).update_one(
            {enums.Common.hashed_key: hashed_key},
            {
                "$set": {
                    enums.Common.hashed_key: hashed_key,
                    enums.Common.key: key,
                    enums.Common.value: value,
                    enums.Common.updated_at: datetime.datetime.now(
                        datetime.timezone.utc
                    ),
                }
            },
            upsert=True,
        )

    @staticmethod
    def filter_private(json_like_or_cursor):
        # if CommandCursor
        if hasattr(json_like_or_cursor, "next"):
            return DbInstance.filter_private(list(json_like_or_cursor))
        if hasattr(json_like_or_cursor, "items"):
            return {
                key: DbInstance.filter_private(value)
                for key, value in json_like_or_cursor.items()
                if (not key.startswith("_") and not key.endswith("_embedding"))
            }
        elif isinstance(json_like_or_cursor, list):
            return [DbInstance.filter_private(item) for item in json_like_or_cursor]
        else:
            return json_like_or_cursor


ENABLE_CACHE = True


def cached_staticmethod(func):
    def wrapper(*args, **kwargs):
        try:
            Configuration.get_instance()
        except Exception as exc:
            logging.warning(
                f"Configuration.get_instance() failed: {exc}, will not perform caching. To enable, ensure mongodb__connection_string is set in .env"
            )
            return func(*args, **kwargs)

        cached = None
        key = json.dumps(args) + json.dumps(kwargs, sort_keys=True)
        if ENABLE_CACHE and kwargs.get("use_cache", True):
            try:
                cached = DbInstance.get_cache(key)
                if cached is not None:
                    return cached

            except Exception as exc:
                logging.warning(
                    f"function {func} cannot be cached, params are not hashable: {args} {kwargs}: {exc}, traceback: {traceback.format_exc()}"
                )
        logging.debug(f"cache missed for {func}")
        result = func(*args, **kwargs)
        DbInstance.set_cache(key, result)
        logging.debug(f"Set cache for {func}, result: {result}")
        return result

    return wrapper


def parse_date_string(date_string: str = "2024-10-04 14:52:22"):
    if date_string is None:
        return None
    if isinstance(date_string, datetime.datetime):
        return date_string.replace(tzinfo=datetime.timezone.utc)
    for date_format_python in ["%Y-%m-%d %H:%M:%S"] + list(
        enums.Common.date_formats_python
    ):
        try:

            datetime_value = datetime.datetime.strptime(
                date_string,
                date_format_python,
            )
            return datetime_value.replace(tzinfo=datetime.timezone.utc)
        except Exception:
            logging.debug(f"Failed to parse date_string=={date_string}")
    logging.warning(f"Failed to parse date_string=={date_string}")
    return None


def parse_float(value, digits=2, abs_value=False, default_value=None):
    if isinstance(value, str):
        # remove any non-numeric characters, except "." and "-"
        value = "".join([c for c in value if c.isdigit() or c == "." or c == "-"])
        # only keep the first "."
        value = value.replace(".", "", value.count(".") - 1)
        if value == "":
            return default_value
        try:
            value = float(value)
        except Exception as exception:
            logging.warning(f"Failed to parse float {value} due to: {exception}")
            value = 0
    elif isinstance(value, numbers.Number):
        pass
    else:
        return default_value
    if digits == 0:
        rounded_value = int(value)
    else:
        rounded_value = round(value, digits)
    if abs_value:
        rounded_value = abs(rounded_value)
    return rounded_value
