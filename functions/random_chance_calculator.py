import random


class RandomChanceCalculator:
    """
    Calculate chances to generate random seasonal object on the map
    Spring (1), Summer (2), Fall (3), Winter (4)
    """

    def get_tree_chance(self, elevation):
        random_chance = ((random.random() - 0.4) ** (1 - (elevation - 2) / 5)).real
        if float(random_chance) > float(0.40):  # chances depends on elevation bro
            return True

    '''
    random chances to create ground props for every tiles
    '''
    def get_ground_prop_chance(self, season, elevation):
        random_chance = 0
        x = random.random()
        '''
        for Fall, Spring, Summer:
        
        random chances would be higher depends on lower elevation:
        if it's 0 or 1 or 2, 0%
        > 0% chances start with ele 3
        
        wolfram alpha: 
        plot (<ele>^100 - 2^100)/<ele>^100*(x - 0.4)^(0 - (2-<ele>)/5)
        55% -> 32.5% -> 32.5% -> 7.5% -> 0%
        '''
        if 1 <= season <= 3:
            if elevation == 0:
                random_chance = 0
            else:
                random_chance = (((elevation ** 100) - (2 ** 100)) / (elevation ** 100)) * (
                            (x - 0.1) ** (0 - (2 - elevation) / 5)).real
            if float(random_chance) > float(0.96):
                return True
        '''
        for Winter:
        
        random chances would be higher depends on higher elevation:
        if it's 0 or 1 or 2, 0%
        > 4% chances start with ele 3
        
        wolfram alpha: 
        plot (x-0.4)^(1 - (<ele>-2)/5))
        8% -> 17.5% -> 32.5% -> 52.5% -> 100%
        '''
        if season == 4:
            random_chance = ((x - 0.4) ** (1 - (elevation - 2) / 5)).real
            if float(random_chance) > float(0.6):
                return True
