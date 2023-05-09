from AoE2ScenarioParser.datasets.trigger_lists import *
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.objects.managers.trigger_manager import TriggerManager
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from functions.RebuildingTriggers import RebuildingTriggers
from model.CapturableObjectives import CapturableObjectives
from model.CapturableObjectives import SharenianTower
from model.PlayerInfo import PlayerInfo
from model.buildings import BuildingInfo

# File & Folder setup

scenario_folder = "C:/Users/Admin/Games/Age of Empires 2 DE/76561198148041091/resources/_common/scenario/"

# Source scenario to work with
scenario_name = "Gloria Victis v0v1v11"
input_path = scenario_folder + scenario_name + ".aoe2scenario"
output_path = scenario_folder + scenario_name + " CapturableObjectives" + ".aoe2scenario"

# declare scenario class
source_scenario: AoE2DEScenario = AoE2DEScenario.from_file(input_path)

# declare trigger manager to work with variables and triggers
source_trigger_manager: TriggerManager = source_scenario.trigger_manager
unit_manager = source_scenario.unit_manager

# print num of triggers
print("Number of triggers: " + str(len(source_trigger_manager.triggers)))

# print(source_trigger_manager.triggers)
# Rearrange trigger (push to a new list)
identification_name = "GVictis - CapturableObjectives.py"
source_trigger_manager = RebuildingTriggers.rebuild_trigger(self="",
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
core units declaration
'''
# core_units_id = [32374, 32399, 33015, 10683]
core_units = CapturableObjectives.get_capturable_objectives() + SharenianTower.get_sharenian_tower()
players_info = PlayerInfo.get_player_info()

'''
capture trigger
'''
triggerSeparator = source_trigger_manager.add_trigger("----Capturable objectives---------------")
for core_unit in core_units:
    triggerSeparator = source_trigger_manager.add_trigger("----" + str(core_unit.name) + "---------------")
    for playerId in range(1, 8, 1):
        coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[
            0]
        trigg_capture: Trigger = source_trigger_manager.add_trigger(
            enabled=True,
            looping=True,
            name="P" + str(playerId) + "Capture" + str(core_unit.coreUnitId)
        )
        trigg_capture.new_condition.timer(timer=5)
        trigg_capture.new_condition.objects_in_area(
            source_player=playerId,
            quantity=1,
            area_x1=int(coreunit_capturable_obj.x - 8),
            area_x2=int(coreunit_capturable_obj.x + 8),
            area_y1=int(coreunit_capturable_obj.y - 8),
            area_y2=int(coreunit_capturable_obj.y + 8),
            object_type=ObjectType.MILITARY
        )
        trigg_capture.new_condition.capture_object(
            unit_object=core_unit.coreUnitId,
            source_player=playerId,
            inverted=True
        )
        for playerId2 in range(1, 9, 1):
            if playerId2 == playerId:
                continue
            else:
                trigg_capture.new_condition.own_fewer_objects(source_player=playerId2,
                                                              quantity=0,
                                                              area_x1=int(coreunit_capturable_obj.x - 8),
                                                              area_x2=int(coreunit_capturable_obj.x + 8),
                                                              area_y1=int(coreunit_capturable_obj.y - 8),
                                                              area_y2=int(coreunit_capturable_obj.y + 8),
                                                              object_type=ObjectType.MILITARY)
        trigg_capture.new_effect.change_ownership(selected_object_ids=core_unit.coreUnitId,
                                                  source_player=playerId,
                                                  target_player=playerId, )
        # print(coreunit_capturable_obj)
        trigg_capture.new_effect.display_instructions(source_player=playerId,
                                                      sound_name="PLAY_WONDER_DESTROYED",
                                                      object_list_unit_id=coreunit_capturable_obj.unit_const,
                                                      message=str(players_info[playerId - 1].color) + str(
                                                          players_info[playerId - 1].name) + " has captured " + str(
                                                          core_unit.name) + "!")
'''
Makes all objective invulnerable
'''
triggerSeparator = source_trigger_manager.add_trigger("----invulnerable objectives---------------")
trigg_invulnerable = source_trigger_manager.add_trigger(
    enabled=True,
    looping=False,
    name="Invulnerable_Obj"
)
for core_unit in core_units:
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    trigg_invulnerable.new_effect.disable_unit_targeting(
        selected_object_ids=core_unit.coreUnitId
    )
    trigg_invulnerable.new_effect.disable_object_deletion(
        selected_object_ids=core_unit.coreUnitId
    )
    # if it's sheranian tower, also apply to the surrounding beacon (walls)
    trigg_invulnerable.new_effect.change_ownership(source_player=8,
                                                   target_player=0,
                                                   object_group=ObjectClass.WALL,
                                                   area_x1=int(coreunit_capturable_obj.x - 2),
                                                   area_x2=int(coreunit_capturable_obj.x + 2),
                                                   area_y1=int(coreunit_capturable_obj.y - 2),
                                                   area_y2=int(coreunit_capturable_obj.y + 2), )
    trigg_invulnerable.new_effect.disable_unit_targeting(object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
                                                         area_x1=int(coreunit_capturable_obj.x - 2),
                                                         area_x2=int(coreunit_capturable_obj.x + 2),
                                                         area_y1=int(coreunit_capturable_obj.y - 2),
                                                         area_y2=int(coreunit_capturable_obj.y + 2), )

'''
modify hp
'''
triggerSeparator = source_trigger_manager.add_trigger("----heal obj loop---------------")
trigg_change_hp = source_trigger_manager.add_trigger(
    name="ChangeHPCapObj",
    enabled=True,
    looping=False
)
for core_unit in core_units:
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    trigg_change_hp.new_effect.change_object_hp(selected_object_ids=core_unit.coreUnitId,
                                                quantity=30000,
                                                operation=Operation.SET)
    trigg_change_hp.new_effect.change_object_hp(object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
                                                quantity=30000,
                                                area_x1=int(coreunit_capturable_obj.x - 2),
                                                area_x2=int(coreunit_capturable_obj.x + 2),
                                                area_y1=int(coreunit_capturable_obj.y - 2),
                                                area_y2=int(coreunit_capturable_obj.y + 2),
                                                operation=Operation.SET)

'''
heal objectives loop
'''
triggerSeparator = source_trigger_manager.add_trigger("----heal obj loop---------------")
for core_unit in core_units:
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    trigg_heal_obj: Trigger = source_trigger_manager.add_trigger(
        name="HealObj_" + str(core_unit.name),
        enabled=True,
        looping=True
    )
    trigg_heal_obj.new_condition.timer(timer=1)
    trigg_heal_obj.new_condition.object_hp(quantity=30000,
                                           unit_object=core_unit.coreUnitId,
                                           inverted=False,
                                           comparison=Comparison.LESS)
    trigg_heal_obj.new_effect.heal_object(quantity=30000,
                                          selected_object_ids=core_unit.coreUnitId)
    trigg_heal_obj.new_effect.heal_object(object_list_unit_id=BuildingInfo.FORTIFIED_WALL.ID,
                                          quantity=30000,
                                          area_x1=int(coreunit_capturable_obj.x - 2),
                                          area_x2=int(coreunit_capturable_obj.x + 2),
                                          area_y1=int(coreunit_capturable_obj.y - 2),
                                          area_y2=int(coreunit_capturable_obj.y + 2), )

'''
Sharenian Tower stuffs
'''
triggerSeparator = source_trigger_manager.add_trigger("======Sharenian Tower stuffs=======")
sharenian_sites = SharenianTower.get_sharenian_tower()

'''
change ownership in start
'''
for core_unit in sharenian_sites:
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    trigg_sharenian_change_owner = source_trigger_manager.add_trigger(
        name="ChangeOwn_Sharen_" + str(core_unit.name),
        enabled=True,
        looping=False
    )
    trigg_sharenian_change_owner.new_condition.timer(timer=2)
    trigg_sharenian_change_owner.new_effect.change_ownership(selected_object_ids=core_unit.coreUnitId,
                                                             target_player=0)
    trigg_sharenian_change_owner.new_effect.change_ownership(area_x1=int(coreunit_capturable_obj.x - 2),
                                                             area_x2=int(coreunit_capturable_obj.x + 2),
                                                             area_y1=int(coreunit_capturable_obj.y - 2),
                                                             area_y2=int(coreunit_capturable_obj.y + 2),
                                                             target_player=0,
                                                             source_player=8,
                                                             object_group=ObjectClass.WALL)
    trigg_sharenian_change_owner.new_effect.change_ownership(area_x1=int(coreunit_capturable_obj.x - 2),
                                                             area_x2=int(coreunit_capturable_obj.x + 2),
                                                             area_y1=int(coreunit_capturable_obj.y - 2),
                                                             area_y2=int(coreunit_capturable_obj.y + 2),
                                                             target_player=0,
                                                             source_player=8,
                                                             object_list_unit_id=94)

triggerEnd = source_trigger_manager.add_trigger("9===" + identification_name + " End===")

# Final step: write a_localArea modified scenario class to a_localArea new scenario file
source_scenario.write_to_file(output_path)
