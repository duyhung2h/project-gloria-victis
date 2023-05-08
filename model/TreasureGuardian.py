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
                             "<GREEN>Hey stranger, think you can give me 2 sheeps? The monster of this forest took my magical ball of yarn, and their wools are guaranteed to be perfect materials for a replacement."),
            TreasureGuardian('Ronnie', 8244, 170, 6, 83, 1,
                             "<GREEN>I'm from Sleepywood, but I'm moving to Ellinia and I need your help. Bring me a builder (villager) to renovate this old house."),
            TreasureGuardian('Arwen the Fairy', 10343, 170, 20, 83, 1,
                             "<GREEN>"),
            TreasureGuardian('Betty the Researcher', 9415, 160, 13, 305, 1,
                             "<GREEN>I came to Ellinia for the hunt of exotic animals. Find a Golden Llama for me, then we'll talk."),
            TreasureGuardian('Wing the Fairy', 9411, 140, 10, 846, 1,
                             "<GREEN>My traveling donkey got lost somewhere in the woods, and I need you to find it. Don't get the wrong ideas though, I just want my magical artifacts back."),
            TreasureGuardian('Rowen the Fairy', 9417, 170, 6, 83, 1,
                             "<GREEN>"),
            TreasureGuardian('Manji the Slayer', 29925, 170, 6, 83, 1,
                             "<ORANGE>"),
        ]
