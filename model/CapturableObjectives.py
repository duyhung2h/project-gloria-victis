class CapturableObjectives:
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

    def __init__(self, coreUnitId, name):
        self.coreUnitId = coreUnitId
        self.name = name

    def get_capturable_objectives():
        return [
            CapturableObjectives(10683, "Ellinia Airship Station"),
        ]


class SharenianTower(CapturableObjectives):

    def __init__(self, coreUnitId, name, coreTargetUnitId):
        CapturableObjectives.__init__(self, coreUnitId, name)
        self.coreTargetUnitId = coreTargetUnitId

    def get_sharenian_tower():
        return [
            SharenianTower(32374, "Sharenian Excavation Site", 41959),
            SharenianTower(32399, "Sharenian Golem Temple", 41990),
            SharenianTower(33015, "Sharenian Temple of Despair", 41998),
        ]
