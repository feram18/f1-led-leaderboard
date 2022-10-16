from enum import Enum


class SessionStatus(Enum):
    """Session Status Enum class"""
    UPCOMING = 'Upcoming'
    IN_PROGRESS = 'In Progress'
    DELAYED = 'Delayed'
    CANCELED = 'Canceled'
    FINISHED = 'Finished'
