from AoE2ScenarioParser.objects.data_objects.trigger import Trigger
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

from functions.RebuildingTriggers import RebuildingTriggers

# File & Folder setup

scenario_folder = "C:/Users/Admin/Games/Age of Empires 2 DE/76561198148041091/resources/_common/scenario/"

# Source scenario to work with
scenario_name = "Gloria Victis v0v1v12"
input_path = scenario_folder + scenario_name + ".aoe2scenario"
output_path = scenario_folder + scenario_name + " ElliniaTrees" + ".aoe2scenario"

# declare scenario class
source_scenario = AoE2DEScenario.from_file(input_path)

# declare trigger manager to work with variables and triggers
source_trigger_manager = source_scenario.trigger_manager
unit_manager = source_scenario.unit_manager

# print num of triggers
print("Number of triggers: " + str(len(source_trigger_manager.triggers)))

# Rearrange trigger (push to a new list)
identification_name = "GVictis - ElliniaTrees.py"
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
declare variables
'''

baobab_id = 1052
oak_id = 349
oak_forest_id = 411
jungle_id = 414
rainforest_id = 1146

list_trunk_type = [baobab_id, oak_id, oak_forest_id, jungle_id, rainforest_id]

tree_locac_list = [[207, 150], [228, 136], [219, 156], [229, 150], [240, 134], [238, 146], [245, 145], [240, 161],
                   [227, 166], [228, 159], [219, 156], [239, 174], [245, 173], [186, 159], [229, 150]]

print(unit_manager.get_units_in_area(x1=207, x2=207, y1=150, y2=150, players=[0]))

'''
fetch all tree location -> check if there's baobab tree above -> mark that tree as a tree trunk
'''
triggerSeparator = source_trigger_manager.add_trigger("----ElliniaTree_DisableTargeting---------------")
for tree_locac in tree_locac_list:
    trigg_disable_targeting: Trigger = source_trigger_manager.add_trigger(
        enabled=True,
        looping=False,
        name="DisableTargeting" + str(tree_locac) + "ElliniaTree"
    )
    trigg_chop_down_tree: Trigger = source_trigger_manager.add_trigger(
        enabled=True,
        looping=False,
        name="ChopDown" + str(tree_locac) + "ElliniaTree"
    )
    x1 = tree_locac[0] - 1
    x2 = tree_locac[0] + 1
    y1 = tree_locac[1] - 2
    y2 = tree_locac[1] + 1
    # x1 = x1 + 3
    # x2 = x2 + 3
    # y1 = y1 - 3
    # y2 = y2 - 3
    for number_of_trunk in range(1, 99, 1):
        list_object = []
        list_object = unit_manager.get_units_in_area(x1=x1, x2=x2, y1=y1 + 1, y2=y2 - 1, players=[0])
        # print(len(list_object))
        if len(list_object) > 0:
            # print("pass len!")
            for object in list_object:
                # print(object.unit_const)
                if object.unit_const == 1052:
                    print("pass treetrunk!")
                    x1 = x1 + 3
                    x2 = x2 + 3
                    y1 = y1 - 3
                    y2 = y2 - 3
                    for tree_trunk in list_trunk_type:
                        trigg_disable_targeting.new_effect.disable_unit_targeting(source_player=0,
                                                                                  object_list_unit_id=tree_trunk,
                                                                                  area_x1=x1,
                                                                                  area_x2=x2,
                                                                                  area_y1=y1,
                                                                                  area_y2=y2)
                        trigg_disable_targeting.new_effect.disable_object_selection(source_player=0,
                                                                                    object_list_unit_id=tree_trunk,
                                                                                    area_x1=x1,
                                                                                    area_x2=x2,
                                                                                    area_y1=y1,
                                                                                    area_y2=y2)
                        trigg_chop_down_tree.new_effect.remove_object(source_player=0,
                                                                      object_list_unit_id=tree_trunk,
                                                                      area_x1=x1,
                                                                      area_x2=x2,
                                                                      area_y1=y1,
                                                                      area_y2=y2)
                    break
    print("pass treetop!")
    for tree_trunk in list_trunk_type:
        trigg_disable_targeting.new_effect.disable_unit_targeting(source_player=0,
                                                                  object_list_unit_id=tree_trunk,
                                                                  area_x1=x1 - 2,
                                                                  area_x2=x2,
                                                                  area_y1=y1,
                                                                  area_y2=y2 + 2)
        trigg_disable_targeting.new_effect.disable_object_selection(source_player=0,
                                                                    object_list_unit_id=tree_trunk,
                                                                    area_x1=x1 - 2,
                                                                    area_x2=x2,
                                                                    area_y1=y1,
                                                                    area_y2=y2 + 2)
        trigg_chop_down_tree.new_effect.remove_object(source_player=0,
                                                      object_list_unit_id=tree_trunk,
                                                      area_x1=x1 - 2,
                                                      area_x2=x2,
                                                      area_y1=y1,
                                                      area_y2=y2 + 2)
    x1 = tree_locac[0] - 1
    x2 = tree_locac[0] + 1
    y1 = tree_locac[1] - 1
    y2 = tree_locac[1] + 1
    trigg_disable_targeting.new_effect.enable_unit_targeting(source_player=0,
                                                             object_list_unit_id=jungle_id,
                                                             area_x1=x1,
                                                             area_x2=x2,
                                                             area_y1=y1,
                                                             area_y2=y2)
    trigg_chop_down_tree.new_condition.own_fewer_objects(source_player=0,
                                                         object_list=jungle_id,
                                                         quantity=0,
                                                         area_x1=x1,
                                                         area_x2=x2,
                                                         area_y1=y1,
                                                         area_y2=y2)

triggerEnd = source_trigger_manager.add_trigger("9===" + identification_name + " End===")

# Final step: write a_localArea modified scenario class to a_localArea new scenario file
source_scenario.write_to_file(output_path)
