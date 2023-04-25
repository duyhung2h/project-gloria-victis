class SeasonalBushes:
    """
    Seasonal bushes which contains information for each bushes
    Bush B -> Bush B -> Bush B -> Bush C
    """

    def __init__(self, SpringVariant, SummerVariant, AutumnVariant, WinterVariant):
        self.SpringVariant = SpringVariant
        self.SummerVariant = SummerVariant
        self.AutumnVariant = AutumnVariant
        self.WinterVariant = WinterVariant

    def get_seasonal_bushes():
        return [
            SeasonalBushes(SpringVariant=27, SummerVariant=27, AutumnVariant=45, WinterVariant=21),
            SeasonalBushes(SpringVariant=0, SummerVariant=0, AutumnVariant=49, WinterVariant=22),
            SeasonalBushes(SpringVariant=14, SummerVariant=14, AutumnVariant=46, WinterVariant=23),
            SeasonalBushes(SpringVariant=12, SummerVariant=12, AutumnVariant=45, WinterVariant=24),
            SeasonalBushes(SpringVariant=28, SummerVariant=28, AutumnVariant=46, WinterVariant=25),
            SeasonalBushes(SpringVariant=20, SummerVariant=20, AutumnVariant=20, WinterVariant=26),
            SeasonalBushes(SpringVariant=42, SummerVariant=42, AutumnVariant=33, WinterVariant=0),
            SeasonalBushes(SpringVariant=44, SummerVariant=44, AutumnVariant=34, WinterVariant=1),
            SeasonalBushes(SpringVariant=41, SummerVariant=41, AutumnVariant=35, WinterVariant=2),
            SeasonalBushes(SpringVariant=30, SummerVariant=30, AutumnVariant=49, WinterVariant=3),
            SeasonalBushes(SpringVariant=23, SummerVariant=23, AutumnVariant=53, WinterVariant=4),
            SeasonalBushes(SpringVariant=19, SummerVariant=19, AutumnVariant=48, WinterVariant=5),
            SeasonalBushes(SpringVariant=40, SummerVariant=40, AutumnVariant=34, WinterVariant=6),
            SeasonalBushes(SpringVariant=39, SummerVariant=39, AutumnVariant=35, WinterVariant=7),
            SeasonalBushes(SpringVariant=21, SummerVariant=21, AutumnVariant=33, WinterVariant=8),
            SeasonalBushes(SpringVariant=11, SummerVariant=11, AutumnVariant=51, WinterVariant=9),
            SeasonalBushes(SpringVariant=31, SummerVariant=31, AutumnVariant=52, WinterVariant=10),
            SeasonalBushes(SpringVariant=10, SummerVariant=10, AutumnVariant=49, WinterVariant=11),
            SeasonalBushes(SpringVariant=2, SummerVariant=2, AutumnVariant=50, WinterVariant=12),
            SeasonalBushes(SpringVariant=32, SummerVariant=32, AutumnVariant=32, WinterVariant=13),
            SeasonalBushes(SpringVariant=13, SummerVariant=13, AutumnVariant=46, WinterVariant=14),
            SeasonalBushes(SpringVariant=39, SummerVariant=39, AutumnVariant=15, WinterVariant=15),
            SeasonalBushes(SpringVariant=38, SummerVariant=38, AutumnVariant=38, WinterVariant=16),
            SeasonalBushes(SpringVariant=36, SummerVariant=36, AutumnVariant=17, WinterVariant=17),
            SeasonalBushes(SpringVariant=18, SummerVariant=18, AutumnVariant=45, WinterVariant=18),
            SeasonalBushes(SpringVariant=9, SummerVariant=9, AutumnVariant=9, WinterVariant=19),
            SeasonalBushes(SpringVariant=4, SummerVariant=4, AutumnVariant=48, WinterVariant=20)

            # SeasonalBushes(SpringVariant=-1, SummerVariant=-1, FallVariant=-1, WinterVariant=-1),
        ]