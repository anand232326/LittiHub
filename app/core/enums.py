
from enum import Enum

class UserRole(str,Enum):
    CUSTOMER="customer"
    RESTAURENT_OWNER="restaurent_owner"
    RESTAURENT_STAFF="restaurent_staff"
    RIDER="rider"
    ADMIN="admin"
    
   