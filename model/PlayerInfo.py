class PlayerInfo:
    """
    Sharenian tower
    CATST1, CATST2, CATST3 to track Sharenian Knight, Teleport to Temple of Despair, Tele to Golem's Temple
    ARROW1, ARROW2, ARROW3 to track Sharenian Golem, Tele to Sharenian Ruin, Tele to Temple of Despair
    BOLTF, BOLTF1, BOLTX to track Sharenian Chariot, Tele to Golem's Temple, Tele to Sharenian Ruin

    32374, 32399, 33015
    Info:

    coreUnitId
    coreTargetUnitId
    """

    def __init__(self, coreTC, name, color):
        self.coreTC = coreTC
        self.name = name
        self.color = color
    def get_player_info():
        return [
            PlayerInfo(-1, "Ellinia", "<GREEN>"),
            PlayerInfo(-1, "Perion", "<ORANGE>"),
            PlayerInfo(-1, "Henesys", "<AQUA>"),
            PlayerInfo(-1, "Kerning City", "<PURPLE>"),
            PlayerInfo(-1, "Lith Harbor", "<BLUE>"),
            PlayerInfo(-1, "Nautilus", "<RED>"),
            PlayerInfo(-1, "Florina", "<YELLOW>"),
        ]
