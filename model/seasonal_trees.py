class SeasonalTrees:
    """
    Seasonal trees which contains information for each trees

    can also includes plants
    Oak -> Oak -> Oak Autumn -> Oak Autumn Snow

    """

    def __init__(self, SpringVariant, SummerVariant, AutumnVariant, WinterVariant):
        self.SpringVariant = SpringVariant
        self.SummerVariant = SummerVariant
        self.AutumnVariant = AutumnVariant
        self.WinterVariant = WinterVariant

    def get_seasonal_trees():
        return [
            SeasonalTrees(SpringVariant=4, SummerVariant=4, AutumnVariant=23, WinterVariant=23),
            SeasonalTrees(SpringVariant=5, SummerVariant=5, AutumnVariant=22, WinterVariant=22),
            SeasonalTrees(SpringVariant=6, SummerVariant=6, AutumnVariant=24, WinterVariant=24),
            SeasonalTrees(SpringVariant=7, SummerVariant=7, AutumnVariant=20, WinterVariant=20),
            SeasonalTrees(SpringVariant=8, SummerVariant=8, AutumnVariant=21, WinterVariant=21),
            SeasonalTrees(SpringVariant=9, SummerVariant=9, AutumnVariant=19, WinterVariant=19),
            # 10: dead tree
            # 11: dead tree
            # 12: dead tree
            SeasonalTrees(SpringVariant=13, SummerVariant=13, AutumnVariant=30, WinterVariant=30),
            SeasonalTrees(SpringVariant=14, SummerVariant=14, AutumnVariant=28, WinterVariant=28),
            SeasonalTrees(SpringVariant=15, SummerVariant=15, AutumnVariant=29, WinterVariant=29),
            # 16: dead tree
            # 17: dead tree
            # 18: dead tree
            # 19-24: orange leaf tree
            # 25-27: dead tree
            SeasonalTrees(SpringVariant=28, SummerVariant=28, AutumnVariant=26, WinterVariant=26),
            SeasonalTrees(SpringVariant=29, SummerVariant=29, AutumnVariant=25, WinterVariant=25),
            SeasonalTrees(SpringVariant=30, SummerVariant=30, AutumnVariant=24, WinterVariant=24),
            SeasonalTrees(SpringVariant=31, SummerVariant=31, AutumnVariant=0, WinterVariant=0),
            SeasonalTrees(SpringVariant=32, SummerVariant=32, AutumnVariant=1, WinterVariant=1),
            SeasonalTrees(SpringVariant=33, SummerVariant=33, AutumnVariant=0, WinterVariant=0),
            SeasonalTrees(SpringVariant=34, SummerVariant=34, AutumnVariant=1, WinterVariant=1),
            SeasonalTrees(SpringVariant=35, SummerVariant=35, AutumnVariant=2, WinterVariant=2),
            SeasonalTrees(SpringVariant=36, SummerVariant=36, AutumnVariant=3, WinterVariant=3),
            SeasonalTrees(SpringVariant=37, SummerVariant=37, AutumnVariant=11, WinterVariant=11),
            SeasonalTrees(SpringVariant=38, SummerVariant=38, AutumnVariant=10, WinterVariant=10),
            SeasonalTrees(SpringVariant=39, SummerVariant=39, AutumnVariant=41, WinterVariant=41),
            SeasonalTrees(SpringVariant=40, SummerVariant=40, AutumnVariant=40, WinterVariant=40),
            SeasonalTrees(SpringVariant=41, SummerVariant=41, AutumnVariant=7, WinterVariant=7),
            SeasonalTrees(SpringVariant=42, SummerVariant=42, AutumnVariant=12, WinterVariant=12),
            SeasonalTrees(SpringVariant=1, SummerVariant=1, AutumnVariant=3, WinterVariant=3),
            SeasonalTrees(SpringVariant=2, SummerVariant=2, AutumnVariant=1, WinterVariant=1),
            SeasonalTrees(SpringVariant=3, SummerVariant=3, AutumnVariant=2, WinterVariant=2),
        ]