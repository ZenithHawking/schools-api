from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

class RateLimits:
    """Các mức giới hạn cho từng loại endpoint"""
    
    SEARCH = "50/minute"    
    LIST = "100/minute"      
    DETAIL = "200/minute"     
    HEALTH = "500/minute"       