from enum import Enum


class GrandPrixStatus(Enum):
    """Grand Prix Status Enum class"""
    UPCOMING = 'Upcoming'
    IN_PROGRESS = 'In Progress'
    DELAYED = 'Delayed'
    CANCELED = 'Canceled'
    FINISHED = 'Finished'
