from enum import Enum


class FinishingStatus(Enum):
    """Finishing Status Enum class"""
    FINISHED = 'Finished'
    DISQUALIFIED = 'DSQ'
    DID_NOT_FINISH = 'DNF'
    PLUS_ONE_LAP = '+1 Lap'
    PLUS_TWO_LAPS = '+2 Laps'
    PLUS_THREE_LAPS = '+3 Laps'
    PLUS_FOUR_LAPS = '+4 Laps'
    PLUS_FIVE_LAPS = '+5 Laps'
    PLUS_SIX_LAPS = '+6 Laps'
    PLUS_SEVEN_LAPS = '+7 Laps'
    PLUS_EIGHT_LAPS = '+8 Laps'
    PLUS_NINE_LAPS = '+9 Laps'
    PLUS_TEN_LAPS = '+10 Laps'

    @classmethod
    def _missing_(cls, value):
        return FinishingStatus.DID_NOT_FINISH
