import re

from AoE2ScenarioParser.datasets.trigger_lists import *
from AoE2ScenarioParser.datasets.units import UnitInfo
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from functions.RebuildingTriggers import RebuildingTriggers
from model.TreasureGuardian import TreasureGuardian
# File & Folder setup
from model.buildings import BuildingInfo

scenario_folder = "C:/Users/Admin/Games/Age of Empires 2 DE/76561198148041091/resources/_common/scenario/"

# Source scenario to work with
scenario_name = "12warlords 0v1v34"
input_path = scenario_folder + scenario_name + ".aoe2scenario"
output_path = scenario_folder + scenario_name + " Adding Villages" + ".aoe2scenario"

# declare scenario class
source_scenario = AoE2DEScenario.from_file(input_path)

# declare trigger manager to work with variables and triggers
source_trigger_manager = source_scenario.trigger_manager

# print num of triggers
print("Number of triggers: " + str(len(source_trigger_manager.triggers)))

# Rearrange trigger (push to a new list)
identification_name = "GVictis - TreasureGuardians.py"
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
When you get close to a guardian / clicked on them
'''
nearVilTriggerlist = []
vilID = -1
for village in TreasureGuardian.get_villages():
    nearVilTriggerlist.append([])
    vilID = vilID + 1
    triggerSeparator = source_trigger_manager.add_trigger("----UnitNearVillage---------------")
    for playerId in range(1, 9, 1):
        trigg_unit_near_village = source_trigger_manager.add_trigger(
            enabled=True,
            looping=False,
            name="P" + str(playerId) + "UnitNearVillage"
        )
        nearVilTriggerlist[vilID].append(trigg_unit_near_village.trigger_id)
        trigg_unit_outof_village = source_trigger_manager.add_trigger(
            enabled=False,
            looping=False,
            name="P" + str(playerId) + "UnitOutOfVillage"
        )
        nearVilTriggerlist[vilID].append(trigg_unit_outof_village.trigger_id)
        # UnitNearVillage
        trigg_unit_near_village.new_condition.objects_in_area(
            quantity=1,
            source_player=playerId,
            area_x1=village.locationXY[0],
            area_x2=village.locationXY[1],
            area_y1=village.locationXY[2],
            area_y2=village.locationXY[3],
            object_state=ObjectState.ALIVE,
            object_type=ObjectType.MILITARY
        )
        trigg_unit_near_village.new_effect.activate_trigger(
            trigger_id=trigg_unit_outof_village.trigger_id
        )
        trigg_unit_near_village.new_effect.create_object(
            source_player=playerId,
            location_x=village.TClocation[0],
            location_y=village.TClocation[1],
            object_list_unit_id=1689,
        )
        for req_text in req_texts:
            trigg_unit_near_village.new_effect.send_chat(
                source_player=playerId,
                message=req_text
            )
        # UnitOutOfVillage
        trigg_unit_outof_village.new_condition.objects_in_area(
            quantity=1,
            source_player=playerId,
            area_x1=village.locationXY[0],
            area_x2=village.locationXY[1],
            area_y1=village.locationXY[2],
            area_y2=village.locationXY[3],
            object_state=ObjectState.ALIVE,
            object_type=ObjectType.MILITARY,
            inverted=True
        )
        trigg_unit_outof_village.new_effect.activate_trigger(
            trigger_id=trigg_unit_near_village.trigger_id
        )
        trigg_unit_outof_village.new_effect.remove_object(
            source_player=playerId,
            area_x1=village.TClocation[0],
            area_x2=village.TClocation[0],
            area_y1=village.TClocation[1],
            area_y2=village.TClocation[1],
            object_list_unit_id=1689,
        )
        trigg_unit_outof_village.new_effect.change_ownership(
            source_player=playerId,
            target_player=0,
            area_x1=village.locationXY[0],
            area_x2=village.locationXY[1],
            area_y1=village.locationXY[2],
            area_y2=village.locationXY[3],
            object_list_unit_id=BuildingInfo.HARBOR.ID
        )
        # print(village.villageName)
        # print(VillageInfo[village.typeOfMission].REQ_TEXT)

'''
Loop change ownership harbor...............................
'''
triggerSeparator = source_trigger_manager.add_trigger("----nearVilTCchangeOWLOOP---------------")
for village in TreasureGuardian.get_villages():
    for playerId in range(1, 9, 1):
        trigg_near_village_change_ow_loop = source_trigger_manager.add_trigger(
            name="P" + str(playerId) + "nearVilTC_CO_LOOP",
            enabled=True,
            looping=True
        )
        trigg_near_village_change_ow_loop.new_condition.timer(
            timer=2
        )
        trigg_near_village_change_ow_loop.new_condition.objects_in_area(
            quantity=1,
            source_player=playerId,
            area_x1=village.locationXY[0],
            area_x2=village.locationXY[1],
            area_y1=village.locationXY[2],
            area_y2=village.locationXY[3],
            object_state=ObjectState.ALIVE,
            object_type=ObjectType.MILITARY
        )
        trigg_near_village_change_ow_loop.new_condition.object_selected_multiplayer(
            source_player=playerId,
            unit_object=village.coreTC
        )
        trigg_near_village_change_ow_loop.new_condition.objects_in_area(
            quantity=1,
            source_player=playerId,
            area_x1=village.locationXY[0],
            area_x2=village.locationXY[1],
            area_y1=village.locationXY[2],
            area_y2=village.locationXY[3],
            object_state=ObjectState.ALIVE,
            object_list=BuildingInfo.HARBOR.ID,
            inverted=True
        )
        for playerId2 in range(0, 9, 1):
            if playerId2 == playerId:
                continue
            trigg_near_village_change_ow_loop.new_effect.change_ownership(
                source_player=playerId2,
                target_player=playerId,
                area_x1=village.locationXY[0],
                area_x2=village.locationXY[1],
                area_y1=village.locationXY[2],
                area_y2=village.locationXY[3],
                object_list_unit_id=BuildingInfo.HARBOR.ID
            )

'''
modify appease | defy icon inside TC
'''
triggerSeparator = source_trigger_manager.add_trigger("----TC Icon---------------")
for playerId in range(1, 9, 1):
    trigg_modify_TC_icon = source_trigger_manager.add_trigger(
        name="P" + str(playerId) + "_TCIcon"
    )
    trigg_modify_TC_icon.new_condition.timer(timer=5)
    trigg_modify_TC_icon.new_effect.enable_disable_object(
        source_player=playerId,
        enabled=True,
        object_list_unit_id=UnitInfo.COW_A.ID,
    )
    trigg_modify_TC_icon.new_effect.enable_disable_object(
        source_player=playerId,
        enabled=True,
        object_list_unit_id=UnitInfo.COW_B.ID,
    )
    trigg_modify_TC_icon.new_effect.change_train_location(
        source_player=playerId,
        button_location=1,
        object_list_unit_id=UnitInfo.COW_A.ID,
        object_list_unit_id_2=1189,
    )
    trigg_modify_TC_icon.new_effect.change_train_location(
        source_player=playerId,
        button_location=2,
        object_list_unit_id=UnitInfo.COW_B.ID,
        object_list_unit_id_2=1189,
    )
    trigg_modify_TC_icon.new_effect.change_object_cost(
        source_player=playerId,
        object_list_unit_id=UnitInfo.COW_A.ID,
        stone=0,
        gold=0,
        wood=0,
        food=0
    )
    trigg_modify_TC_icon.new_effect.change_object_cost(
        source_player=playerId,
        object_list_unit_id=UnitInfo.COW_B.ID,
        stone=0,
        gold=0,
        wood=0,
        food=0
    )
    trigg_modify_TC_icon.new_effect.change_object_description(
        source_player=playerId,
        object_list_unit_id=UnitInfo.COW_A.ID,
        message="Click this icon to appease this village. You'd need to fulfill any request this settlement may have, "
                "to earn their trust and pull them to your side. Each warlord can only have up to 3 villages."
    )
    trigg_modify_TC_icon.new_effect.change_object_description(
        source_player=playerId,
        object_list_unit_id=UnitInfo.COW_B.ID,
        message="Click this icon to defy this village. "
                "This means you'll declare war against this village and cannot appease them again. "
                "All of their territories are ripe to take, even for other players."
    )
    trigg_modify_TC_icon.new_effect.modify_attribute(
        source_player=playerId,
        object_list_unit_id=UnitInfo.COW_A.ID,
        operation=Operation.SET,
        object_attributes=ObjectAttribute.ICON_ID,
        quantity=34
    )
    trigg_modify_TC_icon.new_effect.modify_attribute(
        source_player=playerId,
        object_list_unit_id=UnitInfo.COW_B.ID,
        operation=Operation.SET,
        object_attributes=ObjectAttribute.ICON_ID,
        quantity=183
    )
    trigg_modify_TC_icon.new_effect.modify_attribute(
        source_player=playerId,
        object_list_unit_id=UnitInfo.COW_A.ID,
        operation=Operation.SET,
        object_attributes=ObjectAttribute.TRAIN_TIME,
        quantity=0
    )
    trigg_modify_TC_icon.new_effect.modify_attribute(
        source_player=playerId,
        object_list_unit_id=UnitInfo.COW_B.ID,
        operation=Operation.SET,
        object_attributes=ObjectAttribute.TRAIN_TIME,
        quantity=0
    )
    trigg_modify_TC_icon.new_effect.modify_attribute(
        source_player=playerId,
        object_list_unit_id=UnitInfo.COW_B.ID,
        operation=Operation.SET,
        object_attributes=ObjectAttribute.POPULATION,
        quantity=0
    )
    trigg_modify_TC_icon.new_effect.modify_attribute(
        source_player=playerId,
        object_list_unit_id=UnitInfo.COW_A.ID,
        operation=Operation.SET,
        object_attributes=ObjectAttribute.POPULATION,
        quantity=0
    )



triggerSeparator = source_trigger_manager.add_trigger("--ATTRITION IN WINTER---------------")

triggerEnd = source_trigger_manager.add_trigger("9===" + identification_name + " End===")

# Final step: write a_localArea modified scenario class to a_localArea new scenario file
source_scenario.write_to_file(output_path)
