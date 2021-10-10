from enum import Enum


class UpdateStatus(Enum):
    """Update Status Enum class"""
    SUCCESS = 'Success'
    FAIL = 'Fail'
    API_ERROR = 'API Error'
    NETWORK_ERROR = 'Network Error'
