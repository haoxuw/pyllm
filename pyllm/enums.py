from dataclasses import dataclass


@dataclass
class Common:
    hashed_key: str = "hashed_key"
    key: str = "key"
    value: str = "value"
    cache_table: str = "cache_table"
    updated_at: str = "updated_at"
    created_at: str = "created_at"
    date_formats_python: tuple[str] = ("%Y/%m/%d", "%Y-%m-%d", "%Y%m%d")
