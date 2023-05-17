class CapturableObjectives:
    """
    Sharenian tower
    HORSE A, Junk, Horse B, ... to track Sharenian Footman, Activate Radiant Beam, Teleport to Temple of Despair, Tele to Golem's Temple
    bactrian camel, bear, camel, ARROW4 to track Sharenian Golem, Activate Radiant Beam, Tele to Sharenian Ruin, Tele to Temple of Despair
    Horse C, Horse D, Horse E, BOLTXF to track Sharenian Chariot, Activate Radiant Beam, Tele to Golem's Temple, Tele to Sharenian Ruin

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

    def __init__(self, coreUnitId, name, coreTargetUnitId, trainableUnits, trainableDescriptions, trainableIcon,
                 chargesCost, trainableUniqueUnit, uniqueUnit_Name):
        CapturableObjectives.__init__(self, coreUnitId, name)
        self.coreTargetUnitId = coreTargetUnitId
        self.trainableUnits = trainableUnits
        self.trainableDescriptions = trainableDescriptions
        self.trainableIcon = trainableIcon
        self.chargesCost = chargesCost
        self.trainableUniqueUnit = trainableUniqueUnit
        self.uniqueUnit_Name = uniqueUnit_Name

    def get_sharenian_tower():
        current_charge_str = "Current charge (in this tower): <hp>/40"
        radiant_beam_str = "Activate  <b>Radiant Beam<b> (cost 1 charge / shot)\n\n" \
                           "Heating up the core of this Tower's Magical Stone, " \
                           "unleash beam of destructive fire to destroy " \
                           "faraway targets (unable to fire upon close-ranged targets).\n\n" \
                           "Will deactivate immediately when out of charge. Will recharge over time.\n\n" \
                           + current_charge_str
        return [
            SharenianTower(32374, "Sharenian Excavation Site", 41959, [814, 15, 1356], [
                "Summon <b>Sharenian Footman<b> (cost 8 charges)\n\n"
                "Ancient Sharenian footmen, revived from the dead. "
                "A simple infantry footman that can occasionally block enemies' attacks.\n\n" + current_charge_str,
                radiant_beam_str,
                ""], [184, 26, 189],
                           [8, 0, 0, 0], 76, "Sharenian Footman"),
            SharenianTower(32399, "Golem Temple", 41990, [1237, 486, 897], [
                "Summon <b>Sharenian Golem<b> (cost 20 charges)\n\n"
                "Sharenian Ancient Artificial Golem made of metal and stones. "
                "Act as a slow, moving mobile tank that soaks up incoming ranged attacks. "
                "Deals trample damage over an area with their melee attacks.\n\n" + current_charge_str,
                radiant_beam_str,
                ""], [9, 26, 189], [20, 0, 0, 0], 25, "Sharenian Golem"),
            SharenianTower(33015, "Temple of Despair", 41998, [1602, 1604, 1606, 1564], [
                "Summon <b>Sharenian Chariot<b> (cost 12 charges)\n\n"
                "Ancient Sharenian cavalries, revived from the dead. "
                "A versatile unit that can change between melee or ranged mode. "
                "Deals trample damage over an area with their melee attacks.\n\n" + current_charge_str,
                radiant_beam_str,
                "", ""], [388, 26, 189, 189], [12, 0, 0, 0], 1738, "Sharenian Chariot"),
        ]
