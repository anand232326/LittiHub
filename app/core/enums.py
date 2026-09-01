
from enum import Enum

class UserRole(str,Enum):
    CUSTOMER="customer"
    RESTAURENT_OWNER="restaurent_owner"
    RESTAURENT_STAFF="restaurent_staff"
    RIDER="rider"
    ADMIN="admin"
    



class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class RestaurantSortField(str, Enum):
    NAME = "name"
    CITY = "city"
    CREATED_AT = "created_at"   