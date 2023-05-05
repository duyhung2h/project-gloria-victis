from AoE2ScenarioParser.datasets.trigger_lists import *
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from functions.RebuildingTriggers import RebuildingTriggers
# File & Folder setup
from model.buildings import BuildingInfo

scenario_folder = "C:/Users/Admin/Games/Age of Empires 2 DE/76561198148041091/resources/_common/scenario/"

# Source scenario to work with
scenario_name = "Gloria Victis v0v1v6"
input_path = scenario_folder + scenario_name + ".aoe2scenario"
output_path = scenario_folder + scenario_name + " GlobalUnits" + ".aoe2scenario"

# declare scenario class
source_scenario = AoE2DEScenario.from_file(input_path)

# declare trigger manager to work with variables and triggers
source_trigger_manager = source_scenario.trigger_manager
unit_manager = source_scenario.unit_manager

# print num of triggers
print("Number of triggers: " + str(len(source_trigger_manager.triggers)))

# Rearrange trigger (push to a new list)
identification_name = "GVictis - GlobalUnits.py"
source_trigger_manager.triggers = RebuildingTriggers.rebuild_trigger(self="",
                                                                     source_trigger_manager=source_trigger_manager,
                                                                     identification_name=identification_name)

# refresh (choose whether or not you just want to delete old triggers or not)
# refresh = True
refresh = False

if refresh:
    source_scenario.write_to_file(output_path)
    exit()

# start adding triggers
triggerStart = source_trigger_manager.add_trigger("9===" + identification_name + " Start===")

'''
modify airship when reached age 4
'''
triggerSeparator = source_trigger_manager.add_trigger("----Airship---------------")
airship_unit = UnitInfo.CARAVEL.ID
for playerId in range(1, 9, 1):
    trigg_modify_airship = source_trigger_manager.add_trigger(
        enabled=True,
        looping=False,
        name="P" + str(playerId) + "Airship_Modify"
    )
    trigg_modify_airship.new_condition.technology_state(
        source_player=playerId,
        technology=103,  # Imp age
        quantity=TechnologyState.DONE
    )
    trigg_modify_airship.new_effect.enable_disable_object(
        source_player=playerId,
        enabled=True,
        object_list_unit_id=airship_unit
    )
    trigg_modify_airship.new_effect.change_object_cost(
        source_player=playerId,
        object_list_unit_id=airship_unit,
        wood=1000,
        gold=500,
        food=-1,
        stone=-1
    )
    trigg_modify_airship.new_effect.change_train_location(
        object_list_unit_id=airship_unit,
        source_player=playerId,
        object_list_unit_id_2=BuildingInfo.HARBOR.ID,
        button_location=0,
    )
    trigg_modify_airship.new_effect.change_object_description(
        object_list_unit_id=airship_unit,
        source_player=playerId,
        message="Create <b>Airship<b> (<cost>)\n"
                "Airships that can float in the sky, can hold and paradrop troops for surprise assaults. "
                "Exclusive only to Ellinia's Airship Station.\n"
                "<hp> <attack> <armor> <piercearmor> <range>"
    )
    trigg_modify_airship.new_effect.modify_attribute(
        quantity=0,
        object_list_unit_id=airship_unit,
        source_player=playerId,
        operation=Operation.SET,
        object_attributes=ObjectAttribute.TERRAIN_RESTRICTION_ID,
        message="Airship"
    )
    trigg_modify_airship.new_effect.modify_attribute(
        quantity=20,
        object_list_unit_id=airship_unit,
        source_player=playerId,
        operation=Operation.SET,
        object_attributes=ObjectAttribute.GARRISON_CAPACITY,
        message="Airship"
    )
    trigg_change_airship_name = source_trigger_manager.add_trigger(
        enabled=True,
        looping=True,
        name="P" + str(playerId) + "Airship_CName"
    )
    trigg_change_airship_name.new_condition.timer(
        timer=5
    )
    trigg_change_airship_name.new_effect.replace_object(
        source_player=playerId,
        object_list_unit_id=airship_unit,
        object_list_unit_id_2=airship_unit,
        target_player=playerId
    )
    trigg_change_airship_name.new_effect.change_object_name(
        source_player=playerId,
        object_list_unit_id=airship_unit,
        message="Airship"
    )
triggerEnd = source_trigger_manager.add_trigger("9===" + identification_name + " End===")

# Final step: write a_localArea modified scenario class to a_localArea new scenario file
source_scenario.write_to_file(output_path)
