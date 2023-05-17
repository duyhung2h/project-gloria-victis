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
scenario_name = "Gloria Victis v0v1v12"
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
    trigg_invulnerable.new_condition.timer(timer=2)
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
    trigg_change_hp.new_condition.timer(timer=2)
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
# supporting_beam_unit = 1614
# supporting_beam_unit = 1120
# supporting_beam_unit = 438
supporting_beam_unit = 850
charge_count_unit = 9
overcharged_count = 40
unique_unit_check_location = [1, 9]  # x, y

'''
modify tower stuffs, and change ownership in start
'''
triggerSeparator = source_trigger_manager.add_trigger("-----modify in start---------")
for index, core_unit in enumerate(sharenian_sites):
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    trigg_sharenian_change_owner = source_trigger_manager.add_trigger(
        name="Modify_Sharen_" + str(core_unit.name),
        enabled=True,
        looping=False
    )
    trigg_sharenian_change_owner.new_condition.timer(timer=0)
    # modify tower specifically
    for playerId in range(1, 9, 1):
        trigg_sharenian_change_owner.new_effect.modify_attribute(object_attributes=ObjectAttribute.MAX_RANGE,
                                                                 object_list_unit_id=190,
                                                                 source_player=playerId,
                                                                 operation=Operation.SET,
                                                                 quantity=0)
        trigg_sharenian_change_owner.new_effect.modify_attribute(object_attributes=ObjectAttribute.MINIMUM_RANGE,
                                                                 object_list_unit_id=190,
                                                                 source_player=playerId,
                                                                 operation=Operation.SET,
                                                                 quantity=4)
        trigg_sharenian_change_owner.new_effect.modify_attribute(object_attributes=ObjectAttribute.HIT_POINTS,
                                                                 object_list_unit_id=190,
                                                                 source_player=playerId,
                                                                 operation=Operation.SET,
                                                                 quantity=30000)
    # modify trainables hp
    for playerId in range(1, 8, 1):
        trigg_sharenian_change_owner.new_effect.modify_attribute(quantity=core_unit.trainableIcon[0],
                                                                 operation=Operation.SET,
                                                                 object_attributes=ObjectAttribute.ICON_ID,
                                                                 source_player=playerId,
                                                                 object_list_unit_id=core_unit.trainableUniqueUnit)
        for index2, trainable_unit in enumerate(core_unit.trainableUnits):
            trigg_sharenian_change_owner.new_effect.modify_attribute(quantity=1,
                                                                     operation=Operation.SET,
                                                                     object_attributes=ObjectAttribute.HIT_POINTS,
                                                                     source_player=playerId,
                                                                     object_list_unit_id=trainable_unit)
            trigg_sharenian_change_owner.new_effect.modify_attribute(quantity=core_unit.trainableIcon[index2],
                                                                     operation=Operation.SET,
                                                                     object_attributes=ObjectAttribute.ICON_ID,
                                                                     source_player=playerId,
                                                                     object_list_unit_id=trainable_unit)
            trigg_sharenian_change_owner.new_effect.change_object_cost(food=0,
                                                                       wood=0,
                                                                       gold=0,
                                                                       stone=0,
                                                                       source_player=playerId,
                                                                       object_list_unit_id=trainable_unit)
            trigg_sharenian_change_owner.new_effect.change_variable(quantity=1,
                                                                    operation=Operation.SET,
                                                                    variable=index * 8 + playerId,
                                                                    message="ChargesCount_" + core_unit.name + "P" + str(
                                                                        playerId))
    # modify berserk first
    trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=8,
                                                             operation=Operation.SET,
                                                             object_attributes=ObjectAttribute.HIT_POINTS,
                                                             quantity=30000,
                                                             object_list_unit_id=94)
    trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=8,
                                                             operation=Operation.SET,
                                                             object_attributes=ObjectAttribute.MOVEMENT_SPEED,
                                                             quantity=0,
                                                             object_list_unit_id=94)
    # modify Beacon
    trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=8,
                                                             operation=Operation.SET,
                                                             object_attributes=ObjectAttribute.OCCLUSION_MODE,
                                                             quantity=0,
                                                             object_list_unit_id=supporting_beam_unit)
    trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=8,
                                                             operation=Operation.SET,
                                                             object_attributes=ObjectAttribute.MOVEMENT_SPEED,
                                                             quantity=0,
                                                             object_list_unit_id=supporting_beam_unit)
    trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=8,
                                                             operation=Operation.SET,
                                                             object_attributes=ObjectAttribute.MAX_RANGE,
                                                             quantity=10,
                                                             object_list_unit_id=supporting_beam_unit)
    trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=8,
                                                             operation=Operation.SET,
                                                             object_attributes=ObjectAttribute.ATTACK_RELOAD_TIME,
                                                             quantity=5,
                                                             object_list_unit_id=supporting_beam_unit)
    trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=8,
                                                             operation=Operation.SET,
                                                             object_attributes=ObjectAttribute.HIT_POINTS,
                                                             quantity=30000,
                                                             object_list_unit_id=supporting_beam_unit)
    trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=8,
                                                             operation=Operation.SET,
                                                             object_attributes=ObjectAttribute.DEAD_UNIT_ID,
                                                             quantity=supporting_beam_unit,
                                                             object_list_unit_id=supporting_beam_unit)
    trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=8,
                                                             operation=Operation.SET,
                                                             object_attributes=ObjectAttribute.PROJECTILE_UNIT,
                                                             quantity=676,
                                                             object_list_unit_id=supporting_beam_unit)
    # Modify fire ship projectiles
    for playerId in range(1, 8, 1):
        trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=playerId,
                                                                 operation=Operation.SET,
                                                                 object_attributes=ObjectAttribute.DEAD_UNIT_ID,
                                                                 quantity=charge_count_unit,
                                                                 object_list_unit_id=676)
        trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=playerId,
                                                                 operation=Operation.SET,
                                                                 object_attributes=ObjectAttribute.PROJECTILE_ARC,
                                                                 quantity=0,
                                                                 object_list_unit_id=676)
        trigg_sharenian_change_owner.new_effect.modify_attribute(source_player=playerId,
                                                                 operation=Operation.SET,
                                                                 object_attributes=ObjectAttribute.MOVEMENT_SPEED,
                                                                 quantity=19,
                                                                 object_list_unit_id=676)
    # Change name
    trigg_sharenian_change_owner.new_effect.change_object_name(area_x1=int(coreunit_capturable_obj.x - 2),
                                                               area_x2=int(coreunit_capturable_obj.x + 2),
                                                               area_y1=int(coreunit_capturable_obj.y - 2),
                                                               area_y2=int(coreunit_capturable_obj.y + 2),
                                                               source_player=8,
                                                               object_list_unit_id=155,
                                                               message="Support Beam")
    trigg_sharenian_change_owner.new_effect.change_object_name(selected_object_ids=core_unit.coreUnitId,
                                                               source_player=8,
                                                               message=core_unit.name)
    # now start replacing object
    trigg_sharenian_change_owner.new_effect.change_ownership(selected_object_ids=core_unit.coreUnitId,
                                                             target_player=0)
    trigg_sharenian_change_owner.new_effect.change_object_hp(object_group=ObjectClass.WALL,
                                                             source_player=8,
                                                             area_x1=int(coreunit_capturable_obj.x - 2),
                                                             area_x2=int(coreunit_capturable_obj.x + 2),
                                                             area_y1=int(coreunit_capturable_obj.y - 2),
                                                             area_y2=int(coreunit_capturable_obj.y + 2),
                                                             quantity=30000,
                                                             operation=Operation.SET)
    trigg_sharenian_change_owner.new_effect.change_object_hp(object_list_unit_id=94,
                                                             source_player=8,
                                                             area_x1=int(coreunit_capturable_obj.x - 2),
                                                             area_x2=int(coreunit_capturable_obj.x + 2),
                                                             area_y1=int(coreunit_capturable_obj.y - 2),
                                                             area_y2=int(coreunit_capturable_obj.y + 2),
                                                             quantity=30000,
                                                             operation=Operation.SET)
    trigg_sharenian_change_owner.new_effect.change_object_hp(object_list_unit_id=supporting_beam_unit,
                                                             source_player=8,
                                                             area_x1=int(coreunit_capturable_obj.x - 2),
                                                             area_x2=int(coreunit_capturable_obj.x + 2),
                                                             area_y1=int(coreunit_capturable_obj.y - 2),
                                                             area_y2=int(coreunit_capturable_obj.y + 2),
                                                             quantity=30000,
                                                             operation=Operation.SET)
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
                                                             object_list_unit_id=94, )
    trigg_sharenian_change_owner.new_effect.change_ownership(area_x1=int(coreunit_capturable_obj.x - 2),
                                                             area_x2=int(coreunit_capturable_obj.x + 2),
                                                             area_y1=int(coreunit_capturable_obj.y - 2),
                                                             area_y2=int(coreunit_capturable_obj.y + 2),
                                                             target_player=0,
                                                             source_player=8,
                                                             object_list_unit_id=supporting_beam_unit, )
    trigg_sharenian_change_owner.new_effect.change_object_hp(object_group=ObjectClass.WALL,
                                                             source_player=0,
                                                             area_x1=int(coreunit_capturable_obj.x - 2),
                                                             area_x2=int(coreunit_capturable_obj.x + 2),
                                                             area_y1=int(coreunit_capturable_obj.y - 2),
                                                             area_y2=int(coreunit_capturable_obj.y + 2),
                                                             quantity=30000,
                                                             operation=Operation.SET)
    # disable deletion, targetign and selection
    trigg_sharenian_change_owner.new_effect.disable_object_deletion(area_x1=int(coreunit_capturable_obj.x - 2),
                                                                    area_x2=int(coreunit_capturable_obj.x + 2),
                                                                    area_y1=int(coreunit_capturable_obj.y - 2),
                                                                    area_y2=int(coreunit_capturable_obj.y + 2),
                                                                    source_player=0,
                                                                    object_list_unit_id=supporting_beam_unit, )
    trigg_sharenian_change_owner.new_effect.disable_unit_targeting(area_x1=int(coreunit_capturable_obj.x - 2),
                                                                   area_x2=int(coreunit_capturable_obj.x + 2),
                                                                   area_y1=int(coreunit_capturable_obj.y - 2),
                                                                   area_y2=int(coreunit_capturable_obj.y + 2),
                                                                   source_player=0,
                                                                   object_list_unit_id=supporting_beam_unit, )
    trigg_sharenian_change_owner.new_effect.disable_unit_targeting(area_x1=int(coreunit_capturable_obj.x - 2),
                                                                   area_x2=int(coreunit_capturable_obj.x + 2),
                                                                   area_y1=int(coreunit_capturable_obj.y - 2),
                                                                   area_y2=int(coreunit_capturable_obj.y + 2),
                                                                   source_player=0,
                                                                   object_list_unit_id=155)
    trigg_sharenian_change_owner.new_effect.disable_object_selection(area_x1=int(coreunit_capturable_obj.x - 2),
                                                                     area_x2=int(coreunit_capturable_obj.x + 2),
                                                                     area_y1=int(coreunit_capturable_obj.y - 2),
                                                                     area_y2=int(coreunit_capturable_obj.y + 2),
                                                                     source_player=0,
                                                                     object_list_unit_id=supporting_beam_unit)

'''
After capturing tower, beacons start shooting!
'''
triggerSeparator = source_trigger_manager.add_trigger("--------beacon---------")
for core_unit in sharenian_sites:
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    for playerId in range(1, 8, 1):
        trigg_sharenian_captured = source_trigger_manager.add_trigger(
            name="P" + str(playerId) + "Tower_Capped_" + str(core_unit.name),
            enabled=True,
            looping=True
        )
        trigg_sharenian_captured.new_condition.timer(timer=5)
        trigg_sharenian_captured.new_condition.capture_object(unit_object=core_unit.coreUnitId,
                                                              source_player=playerId)
        trigg_sharenian_captured.new_condition.own_fewer_objects(area_x1=int(coreunit_capturable_obj.x - 2),
                                                                 area_x2=int(coreunit_capturable_obj.x + 2),
                                                                 area_y1=int(coreunit_capturable_obj.y - 2),
                                                                 area_y2=int(coreunit_capturable_obj.y + 2),
                                                                 source_player=playerId,
                                                                 quantity=3,
                                                                 object_list=supporting_beam_unit, )
        for playerId2 in range(0, 9, 1):
            trigg_sharenian_captured.new_effect.change_ownership(area_x1=int(coreunit_capturable_obj.x - 2),
                                                                 area_x2=int(coreunit_capturable_obj.x + 2),
                                                                 area_y1=int(coreunit_capturable_obj.y - 2),
                                                                 area_y2=int(coreunit_capturable_obj.y + 2),
                                                                 source_player=playerId2,
                                                                 object_list_unit_id=supporting_beam_unit,
                                                                 target_player=playerId)
        trigg_sharenian_captured.new_effect.task_object(area_x1=int(coreunit_capturable_obj.x - 2),
                                                        area_x2=int(coreunit_capturable_obj.x + 2),
                                                        area_y1=int(coreunit_capturable_obj.y - 2),
                                                        area_y2=int(coreunit_capturable_obj.y + 2),
                                                        source_player=playerId,
                                                        object_list_unit_id=supporting_beam_unit,
                                                        location_object_reference=core_unit.coreTargetUnitId)

'''
Gathering charges (using ARROW)
'''
triggerSeparator = source_trigger_manager.add_trigger("----gather charges---------")
for index, core_unit in enumerate(sharenian_sites):
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    for playerId in range(1, 8, 1):
        trigg_gathering_charges = source_trigger_manager.add_trigger(
            name="P" + str(playerId) + "GatherCharges_" + str(core_unit.name),
            enabled=True,
            looping=True
        )
        trigg_gathering_charges.new_condition.timer(timer=1)
        trigg_gathering_charges.new_condition.objects_in_area(object_list=charge_count_unit,
                                                              source_player=playerId,
                                                              quantity=4,
                                                              area_x1=int(coreunit_capturable_obj.x - 2),
                                                              area_x2=int(coreunit_capturable_obj.x + 2),
                                                              area_y1=int(coreunit_capturable_obj.y - 2),
                                                              area_y2=int(coreunit_capturable_obj.y + 2), )
        trigg_gathering_charges.new_effect.remove_object(object_list_unit_id=charge_count_unit,
                                                         source_player=playerId,
                                                         area_x1=int(coreunit_capturable_obj.x - 2),
                                                         area_x2=int(coreunit_capturable_obj.x + 2),
                                                         area_y1=int(coreunit_capturable_obj.y - 2),
                                                         area_y2=int(coreunit_capturable_obj.y + 2), )
        for trainable_unit in core_unit.trainableUnits:
            trigg_gathering_charges.new_effect.modify_attribute(quantity=1,
                                                                operation=Operation.ADD,
                                                                object_attributes=ObjectAttribute.HIT_POINTS,
                                                                source_player=playerId,
                                                                object_list_unit_id=trainable_unit)
        trigg_gathering_charges.new_effect.change_variable(quantity=1,
                                                           operation=Operation.ADD,
                                                           variable=index * 8 + playerId,
                                                           message="ChargesCount_" + core_unit.name + "P" + str(
                                                               playerId))

'''
charges overcharged
'''
triggerSeparator = source_trigger_manager.add_trigger("----overcharged---------")
for index, core_unit in enumerate(sharenian_sites):
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    for playerId in range(1, 8, 1):
        trigg_overcharged = source_trigger_manager.add_trigger(
            name="P" + str(playerId) + "Overcharged_" + str(core_unit.name),
            enabled=True,
            looping=True
        )
        trigg_overcharged.new_condition.variable_value(quantity=overcharged_count,
                                                       comparison=Comparison.LARGER,
                                                       variable=index * 8 + playerId)
        for trainable_unit in core_unit.trainableUnits:
            trigg_overcharged.new_effect.modify_attribute(quantity=overcharged_count,
                                                          operation=Operation.SET,
                                                          object_attributes=ObjectAttribute.HIT_POINTS,
                                                          source_player=playerId,
                                                          object_list_unit_id=trainable_unit)
        trigg_overcharged.new_effect.change_variable(quantity=overcharged_count,
                                                     operation=Operation.SET,
                                                     variable=index * 8 + playerId,
                                                     message="ChargesCount_" + core_unit.name + "P" + str(playerId))

'''
Enable Tower trainables
'''
triggerSeparator = source_trigger_manager.add_trigger("----enable Trainables---------")
for index, core_unit in enumerate(sharenian_sites):
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    for playerId in range(1, 8, 1):
        trigg_enable_trainables = source_trigger_manager.add_trigger(
            name="P" + str(playerId) + "EnableTrainables_" + str(core_unit.name),
            enabled=True,
            looping=True
        )
        trigg_enable_trainables.new_condition.timer(timer=3)
        for index2, trainable_unit in enumerate(core_unit.trainableUnits):
            trigg_enable_trainables.new_effect.enable_disable_object(object_list_unit_id=trainable_unit,
                                                                     source_player=playerId,
                                                                     enabled=True)
            trigg_enable_trainables.new_effect.change_object_description(object_list_unit_id=trainable_unit,
                                                                         source_player=playerId,
                                                                         message=core_unit.trainableDescriptions[
                                                                             index2])

'''
Select and display Tower trainables
'''
triggerSeparator = source_trigger_manager.add_trigger("----display Trainables---------")
for index, core_unit in enumerate(sharenian_sites):
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    for playerId in range(1, 8, 1):
        trigg_trainables = source_trigger_manager.add_trigger(
            name="P" + str(playerId) + "DisplayTrainables_" + str(core_unit.name),
            enabled=True,
            looping=True
        )
        trigg_trainables.new_condition.object_selected_multiplayer(unit_object=core_unit.coreUnitId,
                                                                   source_player=playerId)
        # unassign different site units out
        for index2, core_unit2 in enumerate(sharenian_sites):
            for index3, trainable_unit in enumerate(core_unit2.trainableUnits):
                trigg_trainables.new_effect.change_train_location(object_list_unit_id=trainable_unit,
                                                                  object_list_unit_id_2=1622,  # aachen cathedral
                                                                  source_player=playerId,
                                                                  button_location=index3 + 1)

        for index2, trainable_unit in enumerate(core_unit.trainableUnits):
            trigg_trainables.new_effect.change_train_location(object_list_unit_id=trainable_unit,
                                                              object_list_unit_id_2=190,  # Fire Tower
                                                              source_player=playerId,
                                                              button_location=index2 + 1)

'''
enough charges for something -> make them cost 0
'''
triggerSeparator = source_trigger_manager.add_trigger("----Enough charges: Trainable---------")
for index, core_unit in enumerate(sharenian_sites):
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    for playerId in range(1, 8, 1):
        for index2, trainable_unit in enumerate(core_unit.trainableUnits):
            trigg_enough_charges = source_trigger_manager.add_trigger(
                name="P" + str(playerId) + "EnoughChrg_" + str(core_unit.name) + "_" + str(index2),
                enabled=True,
                looping=True
            )
            trigg_enough_charges.new_condition.variable_value(quantity=core_unit.chargesCost[index2],
                                                              comparison=Comparison.LARGER,
                                                              variable=index * 8 + playerId)
            trigg_enough_charges.new_effect.modify_attribute(source_player=playerId,
                                                             operation=Operation.SET,
                                                             object_attributes=ObjectAttribute.POPULATION,
                                                             object_list_unit_id=trainable_unit,
                                                             quantity=0)
            # trigg_enough_charges.new_effect.change_object_cost(object_list_unit_id=trainable_unit,
            #                                                    source_player=playerId,
            #                                                    stone=0,
            #                                                    gold=0,
            #                                                    food=0,
            #                                                    wood=0)
            # trigg_enough_charges.new_effect.enable_disable_object(object_list_unit_id=trainable_unit,
            #                                                       source_player=playerId,
            #                                                       enabled=True)

'''
Not enough charges for something -> make them cost 999999
'''
triggerSeparator = source_trigger_manager.add_trigger("----Not Enough charges: Untrainable---------")
for index, core_unit in enumerate(sharenian_sites):
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    for playerId in range(1, 8, 1):
        for index2, trainable_unit in enumerate(core_unit.trainableUnits):
            trigg_not_enough_charges = source_trigger_manager.add_trigger(
                name="P" + str(playerId) + "NotEnoughChrg_" + str(core_unit.name) + "_" + str(index2),
                enabled=True,
                looping=True
            )
            trigg_not_enough_charges.new_condition.variable_value(quantity=core_unit.chargesCost[index2],
                                                                  comparison=Comparison.LESS_OR_EQUAL,
                                                                  variable=index * 8 + playerId)
            trigg_not_enough_charges.new_effect.modify_attribute(source_player=playerId,
                                                                 operation=Operation.SET,
                                                                 object_attributes=ObjectAttribute.POPULATION,
                                                                 object_list_unit_id=trainable_unit,
                                                                 quantity=200)
            # trigg_not_enough_charges.new_effect.change_object_cost(object_list_unit_id=trainable_unit,
            #                                                        source_player=playerId,
            #                                                        stone=99999,
            #                                                        gold=99999,
            #                                                        food=99999,
            #                                                        wood=99999)
            # trigg_not_enough_charges.new_effect.enable_disable_object(object_list_unit_id=trainable_unit,
            #                                                           source_player=playerId,
            #                                                           enabled=False)
'''
train something -> lower charge down
'''
triggerSeparator = source_trigger_manager.add_trigger("----Not Enough charges: Untrainable---------")
for index, core_unit in enumerate(sharenian_sites):
    coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit.coreUnitId])[0]
    for playerId in range(1, 8, 1):
        for index2, trainable_unit in enumerate(core_unit.trainableUnits):
            trigg_train_unique_unit = source_trigger_manager.add_trigger(
                name="P" + str(playerId) + "trainUnique_" + str(core_unit.name),
                enabled=True,
                looping=True
            )
            trigg_train_unique_unit_not_enough = source_trigger_manager.add_trigger(
                name="P" + str(playerId) + "trainUnique_NEnough_" + str(core_unit.name),
                enabled=True,
                looping=True
            )
            trigg_tele_unique_unit_back = source_trigger_manager.add_trigger(
                name="P" + str(playerId) + "teleUniqueBack_" + str(core_unit.name),
                enabled=True,
                looping=True
            )
            # check if training something and enough charges
            trigg_train_unique_unit.new_condition.objects_in_area(quantity=1,
                                                                  object_list=trainable_unit,
                                                                  source_player=playerId,
                                                                  area_x1=int(coreunit_capturable_obj.x - 20),
                                                                  area_x2=int(coreunit_capturable_obj.x + 20),
                                                                  area_y1=int(coreunit_capturable_obj.y - 20),
                                                                  area_y2=int(coreunit_capturable_obj.y + 20), )
            trigg_train_unique_unit.new_condition.variable_value(quantity=core_unit.chargesCost[index2],
                                                                 comparison=Comparison.LARGER,
                                                                 variable=index * 8 + playerId)
            trigg_train_unique_unit.new_effect.teleport_object(object_list_unit_id=trainable_unit,
                                                               source_player=playerId,
                                                               area_x1=int(coreunit_capturable_obj.x - 20),
                                                               area_x2=int(coreunit_capturable_obj.x + 20),
                                                               area_y1=int(coreunit_capturable_obj.y - 20),
                                                               area_y2=int(coreunit_capturable_obj.y + 20),
                                                               location_x=unique_unit_check_location[0],
                                                               location_y=unique_unit_check_location[1] + index2 * 2)
            # check if training something and NOT enough charges
            trigg_train_unique_unit_not_enough.new_condition.objects_in_area(quantity=1,
                                                                             object_list=trainable_unit,
                                                                             source_player=playerId,
                                                                             area_x1=int(
                                                                                 coreunit_capturable_obj.x - 20),
                                                                             area_x2=int(
                                                                                 coreunit_capturable_obj.x + 20),
                                                                             area_y1=int(
                                                                                 coreunit_capturable_obj.y - 20),
                                                                             area_y2=int(
                                                                                 coreunit_capturable_obj.y + 20), )
            trigg_train_unique_unit_not_enough.new_condition.variable_value(quantity=core_unit.chargesCost[index2],
                                                                            comparison=Comparison.LESS_OR_EQUAL,
                                                                            variable=index * 8 + playerId)
            trigg_train_unique_unit_not_enough.new_effect.remove_object(object_list_unit_id=trainable_unit,
                                                                        source_player=playerId,
                                                                        area_x1=int(coreunit_capturable_obj.x - 20),
                                                                        area_x2=int(coreunit_capturable_obj.x + 20),
                                                                        area_y1=int(coreunit_capturable_obj.y - 20),
                                                                        area_y2=int(coreunit_capturable_obj.y + 20), )
            # tele unit back
            trigg_tele_unique_unit_back.new_condition.variable_value(quantity=core_unit.chargesCost[index2],
                                                                     comparison=Comparison.LARGER,
                                                                     variable=index * 8 + playerId)
            trigg_tele_unique_unit_back.new_condition.objects_in_area(quantity=1,
                                                                      object_list=trainable_unit,
                                                                      source_player=playerId,
                                                                      area_x1=unique_unit_check_location[0],
                                                                      area_x2=unique_unit_check_location[0],
                                                                      area_y1=unique_unit_check_location[
                                                                                  1] + index2 * 2,
                                                                      area_y2=unique_unit_check_location[
                                                                                  1] + index2 * 2, )
            trigg_tele_unique_unit_back.new_effect.replace_object(object_list_unit_id=trainable_unit,
                                                                  source_player=playerId,
                                                                  target_player=playerId,
                                                                  area_x1=unique_unit_check_location[0],
                                                                  area_x2=unique_unit_check_location[0],
                                                                  area_y1=unique_unit_check_location[1] + index2 * 2,
                                                                  area_y2=unique_unit_check_location[1] + index2 * 2,
                                                                  object_list_unit_id_2=600 + index2)
            trigg_tele_unique_unit_back.new_effect.teleport_object(object_list_unit_id=600 + index2,
                                                                   source_player=playerId,
                                                                   area_x1=unique_unit_check_location[0],
                                                                   area_x2=unique_unit_check_location[0],
                                                                   area_y1=unique_unit_check_location[1] + index2 * 2,
                                                                   area_y2=unique_unit_check_location[1] + index2 * 2,
                                                                   location_x=int(coreunit_capturable_obj.x - 1),
                                                                   location_y=int(coreunit_capturable_obj.y + 1))
            trigg_tele_unique_unit_back.new_effect.replace_object(object_list_unit_id=600 + index2,
                                                                  source_player=playerId,
                                                                  target_player=playerId,
                                                                  area_x1=int(coreunit_capturable_obj.x - 1),
                                                                  area_x2=int(coreunit_capturable_obj.x - 1),
                                                                  area_y1=int(coreunit_capturable_obj.y + 1),
                                                                  area_y2=int(coreunit_capturable_obj.y + 1),
                                                                  object_list_unit_id_2=core_unit.trainableUniqueUnit)
            for index3, trainable_unit2 in enumerate(core_unit.trainableUnits):
                trigg_tele_unique_unit_back.new_effect.modify_attribute(quantity=core_unit.chargesCost[index2],
                                                                        object_list_unit_id=trainable_unit2,
                                                                        object_attributes=ObjectAttribute.HIT_POINTS,
                                                                        operation=Operation.SUBTRACT,
                                                                        source_player=playerId)
            trigg_tele_unique_unit_back.new_effect.change_variable(quantity=core_unit.chargesCost[index2],
                                                                   operation=Operation.SUBTRACT,
                                                                   variable=index * 8 + playerId,
                                                                   message="ChargesCount_" + core_unit.name + "P" + str(
                                                                       playerId))

triggerEnd = source_trigger_manager.add_trigger("9===" + identification_name + " End===")

# Final step: write a_localArea modified scenario class to a_localArea new scenario file
source_scenario.write_to_file(output_path)
