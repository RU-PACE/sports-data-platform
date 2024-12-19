from enum import Enum

# Enums for selection options
class SportEnum(str, Enum):
    cricket = "Cricket"
    football = "Football"
    basketball = "Basketball"
    hockey = "Hockey"
    cric = "Footb"

class GenderEnum(str, Enum):
    men = "Men"
    women = "Women"
    mixed = "Mixed"

class FormatEnum(str, Enum):
    t20 = "T20"
    oneday = "OneDay"
    test = "Test"
    worldcup = "WorldCup"