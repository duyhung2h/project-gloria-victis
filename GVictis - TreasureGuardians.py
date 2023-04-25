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
scenario_name = "Gloria Victis v0v1v1"
input_path = scenario_folder + scenario_name + ".aoe2scenario"
output_path = scenario_folder + scenario_name + " TreasureGuardians" + ".aoe2scenario"

# declare scenario class
source_scenario = AoE2DEScenario.from_file(input_path)

# declare trigger manager to work with variables and triggers
source_trigger_manager = source_scenario.trigger_manager
unit_manager = source_scenario.unit_manager

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
for treasure_guardian in TreasureGuardian.get_treasure_guardians():
    triggerSeparator = source_trigger_manager.add_trigger("----click on TG---------------")
    for playerId in range(1, 9, 1):
        trigg_click_on_TG = source_trigger_manager.add_trigger(
            enabled=True,
            looping=True,
            name="P" + str(playerId) + "ClickOnTG_" + treasure_guardian.guardianName
        )
        # trigg_click_on_TG.new_condition.objects_in_area(
        #     quantity=1,
        #     source_player=playerId,
        #     area_x1=treasure_guardian.locationXY[0],
        #     area_x2=treasure_guardian.locationXY[1],
        #     area_y1=treasure_guardian.locationXY[2],
        #     area_y2=treasure_guardian.locationXY[3],
        #     object_state=ObjectState.ALIVE,
        #     object_type=ObjectType.MILITARY
        # )
        trigg_click_on_TG.new_condition.object_selected_multiplayer(
            unit_object=treasure_guardian.coreUnitId,
            source_player=playerId,
        )
        trigg_click_on_TG.new_condition.capture_object(
            unit_object=treasure_guardian.coreUnitId,
            source_player=0,
        )
        trigg_click_on_TG.new_condition.timer(
            timer=20
        )
        trigg_click_on_TG.new_effect.send_chat(
            source_player=playerId,
            message=treasure_guardian.missionText
        )


'''
Loop heal treasure guardians
'''
trigg_heal_tg = source_trigger_manager.add_trigger(
    enabled=True,
    looping=True,
    name="Heal_TG"
)
for treasure_guardian in TreasureGuardian.get_treasure_guardians():
    trigg_heal_tg.new_condition.timer(timer=5)
    trigg_heal_tg.new_effect.heal_object(
        selected_object_ids=treasure_guardian.coreUnitId,
        source_player=8,
        quantity=int(treasure_guardian.hp / 100)
    )

'''
Loop treasure guardian HP < max (engage in battle)
'''
for treasure_guardian in TreasureGuardian.get_treasure_guardians():
    trigg_tg_engage = source_trigger_manager.add_trigger(
        enabled=True,
        looping=True,
        name="TG_Engage_" + treasure_guardian.guardianName
    )
    trigg_tg_engage.new_condition.capture_object(
        source_player=0,
        unit_object=treasure_guardian.coreUnitId
    )
    trigg_tg_engage.new_condition.object_hp(
        quantity=treasure_guardian.hp-1,
        comparison=Comparison.LESS,
        unit_object=treasure_guardian.coreUnitId
    )
    trigg_tg_engage.new_effect.change_ownership(
        selected_object_ids=treasure_guardian.coreUnitId,
        source_player=0,
        target_player=8,
    )

'''
Loop treasure guardian HP = max (disengage from battle)
'''
for treasure_guardian in TreasureGuardian.get_treasure_guardians():
    trigg_tg_disengage = source_trigger_manager.add_trigger(
        enabled=True,
        looping=True,
        name="TG_Disengage_" + treasure_guardian.guardianName
    )
    trigg_tg_disengage.new_condition.capture_object(
        source_player=8,
        unit_object=treasure_guardian.coreUnitId
    )
    trigg_tg_disengage.new_condition.object_hp(
        quantity=treasure_guardian.hp-1,
        comparison=Comparison.LARGER_OR_EQUAL,
        unit_object=treasure_guardian.coreUnitId
    )
    trigg_tg_disengage.new_effect.change_ownership(
        selected_object_ids=treasure_guardian.coreUnitId,
        source_player=8,
        target_player=0,
    )

'''
Loop attack_move treasure guardian back to location
'''
for treasure_guardian in TreasureGuardian.get_treasure_guardians():
    trigg_atk_move_to_origin_loc = source_trigger_manager.add_trigger(
        enabled=True,
        looping=True,
        name="ATKMove_ToOriginLoc_" + treasure_guardian.guardianName
    )
    coreunit_treasure_guardian = unit_manager.filter_units_by_reference_id(unit_reference_ids=[treasure_guardian.coreUnitId])[0]
    print(coreunit_treasure_guardian)
    trigg_atk_move_to_origin_loc.new_condition.timer(timer=2)
    trigg_atk_move_to_origin_loc.new_condition.bring_object_to_area(
        area_x1=int(coreunit_treasure_guardian.x - 5),
        area_x2=int(coreunit_treasure_guardian.x + 5),
        area_y1=int(coreunit_treasure_guardian.y - 5),
        area_y2=int(coreunit_treasure_guardian.y + 5),
        unit_object=treasure_guardian.coreUnitId,
        inverted=True
    )
    trigg_atk_move_to_origin_loc.new_effect.task_object(
        selected_object_ids=treasure_guardian.coreUnitId,
        location_x=int(coreunit_treasure_guardian.x),
        location_y=int(coreunit_treasure_guardian.y),
        source_player=8,
    )
    trigg_atk_move_to_origin_loc.new_effect.heal_object(
        selected_object_ids=treasure_guardian.coreUnitId,
        source_player=8,
        quantity=treasure_guardian.hp
    )

'''
modify treasure guardian stats
'''
triggerSeparator = source_trigger_manager.add_trigger("----modify TG stats---------------")
playerId = 8
trigg_modify_TC_icon = source_trigger_manager.add_trigger(
    name="TG_stats"
)
trigg_modify_TC_icon.new_condition.timer(timer=5)
for treasure_guardian in TreasureGuardian.get_treasure_guardians():
    trigg_modify_TC_icon.new_effect.none()
    trigg_modify_TC_icon.new_effect.change_object_name(
        source_player=playerId,
        selected_object_ids=treasure_guardian.coreUnitId,
        message=treasure_guardian.guardianName
    )
    trigg_modify_TC_icon.new_effect.change_object_attack(
        source_player=playerId,
        selected_object_ids=treasure_guardian.coreUnitId,
        operation=Operation.SET,
        armour_attack_class=3,
        armour_attack_quantity=treasure_guardian.atk
    )
    trigg_modify_TC_icon.new_effect.change_object_attack(
        source_player=playerId,
        selected_object_ids=treasure_guardian.coreUnitId,
        operation=Operation.SET,
        armour_attack_class=4,
        armour_attack_quantity=treasure_guardian.atk
    )
    trigg_modify_TC_icon.new_effect.change_object_hp(
        source_player=playerId,
        selected_object_ids=treasure_guardian.coreUnitId,
        operation=Operation.SET,
        quantity=treasure_guardian.hp
    )

triggerEnd = source_trigger_manager.add_trigger("9===" + identification_name + " End===")

# Final step: write a_localArea modified scenario class to a_localArea new scenario file
source_scenario.write_to_file(output_path)
