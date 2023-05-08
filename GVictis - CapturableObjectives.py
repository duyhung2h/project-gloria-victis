from AoE2ScenarioParser.datasets.trigger_lists import ObjectType
from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from functions.RebuildingTriggers import RebuildingTriggers

# File & Folder setup

scenario_folder = "C:/Users/Admin/Games/Age of Empires 2 DE/76561198148041091/resources/_common/scenario/"

# Source scenario to work with
scenario_name = "Gloria Victis v0v1v10"
input_path = scenario_folder + scenario_name + ".aoe2scenario"
output_path = scenario_folder + scenario_name + " CapturableObjectives" + ".aoe2scenario"

# declare scenario class
source_scenario = AoE2DEScenario.from_file(input_path)

# declare trigger manager to work with variables and triggers
source_trigger_manager = source_scenario.trigger_manager
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
core_units_id = [32374, 32399, 33015, 10683]

'''
capture trigger
'''
triggerSeparator = source_trigger_manager.add_trigger("----Capturable objectives---------------")
for core_unit_id in core_units_id:
    triggerSeparator = source_trigger_manager.add_trigger("----" + str(core_unit_id) + "---------------")
    for playerId in range(1, 9, 1):
        coreunit_capturable_obj = unit_manager.filter_units_by_reference_id(unit_reference_ids=[core_unit_id])[0]
        trigg_capture: Trigger = source_trigger_manager.add_trigger(
            enabled=True,
            looping=True,
            name="P" + str(playerId) + "Capture" + str(core_unit_id)
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
            unit_object=core_unit_id,
            source_player=playerId,
            inverted=True
        )
        for playerId2 in range(1, 9, 1):
            if playerId2 == playerId:
                continue
            else:
                trigg_capture.new_condition.own_fewer_objects(
                    source_player=playerId2,
                    quantity=0,
                    area_x1=int(coreunit_capturable_obj.x - 8),
                    area_x2=int(coreunit_capturable_obj.x + 8),
                    area_y1=int(coreunit_capturable_obj.y - 8),
                    area_y2=int(coreunit_capturable_obj.y + 8),
                    object_type=ObjectType.MILITARY
                )
        trigg_capture.new_effect.change_ownership(
            selected_object_ids=core_unit_id,
            source_player=playerId,
            target_player=playerId,
        )
'''
Makes all objective invulnerable
'''
triggerSeparator = source_trigger_manager.add_trigger("----invulnerable objectives---------------")
trigg_invulnerable = source_trigger_manager.add_trigger(
    enabled=True,
    looping=False,
    name="Invulnerable_Obj"
)
for core_unit_id in core_units_id:
    trigg_capture.new_effect.disable_unit_targeting(
        selected_object_ids=core_unit_id
    )
    trigg_capture.new_effect.disable_object_deletion(
        selected_object_ids=core_unit_id
    )
triggerEnd = source_trigger_manager.add_trigger("9===" + identification_name + " End===")

# Final step: write a_localArea modified scenario class to a_localArea new scenario file
source_scenario.write_to_file(output_path)
