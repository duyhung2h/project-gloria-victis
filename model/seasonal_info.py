class SeasonalInfo:
    """
    """

    def get_season_name(self, season_id):
        if season_id == 1:
            return "Spring"
        if season_id == 2:
            return "Summer"
        if season_id == 3:
            return "Autumn"
        if season_id == 4:
            return "Winter"

    def get_season_bonuses_info(self, season_id):
        if season_id == 1:
            return "Unit heal +1 per 15 seconds \nTrade +50% profit"
        if season_id == 2:
            return "Gold gather rate +33% \nStone gather rate +33%"
        if season_id == 3:
            return "Wood gather rate +33% \nFood gather rate +33%"
        if season_id == 4:
            return "Attrition when in enemy's territory (-max hp) \nBuildings are more resilient"

    def get_seasonal_ground_obj_facets(self, season_id):
        if season_id == 1:
            return [1, 2, 3, 4, 5, 6, 7, 8]
        if season_id == 2:
            return [1, 2, 3, 4, 5, 6, 7, 8]
        if season_id == 3:
            return [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if season_id == 4:
            return [1, 2, 3, 4, 5, 6]

    def get_seasonal_ground_obj_id(self, season_id):
        if season_id == 1:
            return 1366  # Plant (Flowers)
        if season_id == 2:
            return 1351  # Plant (Jungle)
        if season_id == 3:
            return 1365  # Plant (Underbrush Rainforest)
        if season_id == 4:
            return 728  # Ice, Navigable

    def get_seasonal_tree_id(self, season_id):
        if season_id == 1:
            return 411  # Tree (Oak Forest)
        if season_id == 2:
            return 411  # Tree (Oak Forest)
        if season_id == 3:
            return 1248  # Tree (Oak Autumn)
        if season_id == 4:
            return 1249  # Tree (Oak Autumn Snow)

    def get_seasonal_bush_id(self, season_id):
        if season_id == 1:
            return 1053  # Bush B
        if season_id == 2:
            return 1053  # Bush B
        if season_id == 3:
            return 1053  # Bush B
        if season_id == 4:
            return 1054  # Bush C

    def get_allowed_terrains(self, season_id):
        allowed_terrains = []
        if season_id == 1:
            # Allowed terrain (ALL LANDS TERRAIN -roads -farm)
            allowed_terrains = [0, 3, 5, 6, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 26, 27, 32, 36,
                                40, 41, 42, 45, 46, 48, 49, 50, 56, 70, 71, 72, 76, 77, 83, 88, 89, 100, 101, 102, 104,
                                105, 106, 110, 111, 112]
        if season_id == 2:
            # Allowed terrain (ALL LANDS TERRAIN -roads -farm)
            allowed_terrains = [0, 3, 5, 6, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 26, 27, 32, 36,
                                40, 41, 42, 45, 46, 48, 49, 50, 56, 70, 71, 72, 76, 77, 83, 88, 89, 100, 101, 102, 104,
                                105, 106, 110, 111, 112]
        if season_id == 3:
            # Allowed terrain (ALL LANDS TERRAIN -roads -farm)
            allowed_terrains = [0, 3, 5, 6, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 26, 27, 32, 36,
                                40, 41, 42, 45, 46, 48, 49, 50, 56, 70, 71, 72, 76, 77, 83, 88, 89, 100, 101, 102, 104,
                                105, 106, 110, 111, 112]
        if season_id == 4:
            # Allowed terrain (ALL LANDS TERRAIN)
            allowed_terrains = [0, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 24, 25, 26, 27, 29, 30,
                                31, 32, 36, 40, 41, 42, 45, 46, 48, 49, 50, 56, 60, 63, 64, 65, 66, 67, 70, 71, 72, 75,
                                76, 77, 78,
                                83, 88, 89, 100, 101, 102, 104, 105, 106, 110, 111, 112]
        return allowed_terrains
