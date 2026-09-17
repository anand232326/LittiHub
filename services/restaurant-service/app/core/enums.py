from enum import Enum


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class RestaurantSortField(str, Enum):
    NAME = "name"
    CREATED_AT = "created_at"
    CITY = "city"