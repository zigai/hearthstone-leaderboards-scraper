import enum


class GameMode(str, enum.Enum):
    BATTLEGROUNDS = "battlegrounds"
    BATTLEGROUNDS_DUO = "battlegroundsduo"
    STANDARD = "standard"
    WILD = "wild"
    CLASSIC = "classic"
    MERCEANARY = "mercenaries"
    ARENA = "arena"
    TWIST = "twist"
