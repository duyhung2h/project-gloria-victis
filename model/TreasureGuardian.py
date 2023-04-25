class TreasureGuardian:
    """
    This is a_localArea Villages class

    A village can have different attributes, such as villageName, locationXY [x1, x2, y1, y2]
    each village is captureable by one of 6 warlords players (each player can only have 3 villages each),
    they are untargetable at first. You either have two option (which are clickable inside the hero unit),

    either you raze the village (to obtain resources (rewarded for each unit kill/building razed) but decrease your unit morale)
    or
    win the village's favor (by doing their errands)
    """

    def __init__(self, guardianName, coreUnitId, hp, atk, unitDemand, amountNeeded, missionText):
        self.guardianName = guardianName
        self.coreUnitId = coreUnitId
        self.hp = hp
        self.atk = atk

        self.unitDemand = unitDemand
        self.amountNeeded = amountNeeded
        self.missionText = missionText

    def get_treasure_guardians():
        return [
            TreasureGuardian('Fanzy, the Dream Eater', 8028, 200, 6, 594, 2,
                             "<GREEN>---Fanzy, the Dream Eater---\nHey stranger, think you can give me 2 sheep? The monster of this forest took my magical ball of yarn, and their wools are guaranteed to be perfect materials for a replacement.")
        ]
