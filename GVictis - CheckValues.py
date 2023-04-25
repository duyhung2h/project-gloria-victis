from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from model.TreasureGuardian import TreasureGuardian

# File & Folder setup
scenario_folder = "C:/Users/Admin/Games/Age of Empires 2 DE/76561198148041091/resources/_common/scenario/"

# Source scenario to work with
scenario_name = "12warlords 0v1v31"
input_path = scenario_folder + scenario_name + ".aoe2scenario"

# declare scenario class
source_scenario = AoE2DEScenario.from_file(input_path)

# declare trigger manager to work with variables and triggers
source_trigger_manager = source_scenario.trigger_manager

# print num of triggers
print("Number of triggers: " + str(len(source_trigger_manager.triggers)))

# target_trigger_manager.triggers = []  # Uncomment this in order to wipe all triggers from the map at start
# target_trigger_manager.variables = []  # Uncomment this in order to wipe all variables from the map at start

# print("--------dict-------------------------------")
# print(source_trigger_manager.__dict__)

print("--------Variables-------------------------------")
unit_manager = source_scenario.unit_manager
for unit in unit_manager.units[0]:
    # print(unit)
    if unit.unit_const == 415:
        print(str(unit.reference_id) + " x: " + str(unit.x) + " y: " + str(unit.y))
        unit.unit_const = 809
variables = source_scenario.trigger_manager.variables
for variableNum in range(0, len(variables), 1):
    print("ID: " + str(variables[variableNum].variable_id) + " - " + variables[variableNum].name)
print("---------------------------------------")
# for a_localArea in range(0, len(UnitInfo), 1):
# print(UnitInfo[a_localArea].ID)
print("---------------------------------------")
print("trigger list with their id:")
for triggerId in range(0, len(source_trigger_manager.triggers), 1):
    print(source_trigger_manager.triggers[triggerId].name + ", ID: "
          + str(source_trigger_manager.triggers[triggerId].trigger_id))

# put triggers ranging from index position_start to position_end, to position position_transfer in the target file
test_position_start = 0
test_position_end = 0
for triggerId in range(0, len(source_trigger_manager.triggers), 1):
    if source_trigger_manager.triggers[triggerId].name == "------------------testStartCheckShit":
        print(source_trigger_manager.triggers[triggerId].name)
        test_position_start = source_trigger_manager.triggers[triggerId].trigger_id + 0
        test_position_end = test_position_start + 4

# working with triggers
testTriggers = source_trigger_manager.triggers[test_position_start:test_position_end]
villages = TreasureGuardian.get_villages()

# try:
print(testTriggers[0].trigger_id)
print("map size: " + str(testTriggers[0].conditions[1].area_x2))
print("teleSheep location: [x=" + str(testTriggers[0].effects[0].location_x) + ", y=" + str(
    testTriggers[0].effects[0].location_y) + "]")
print("------------Coreunit--------------")
print("TC Dai La Coreunit: " + str(testTriggers[1].effects[0].selected_object_ids))
print("TC Tam Đái Coreunit: " + str(testTriggers[1].effects[1].selected_object_ids))
print("TC Bắc Kạn Coreunit: " + str(testTriggers[1].effects[2].selected_object_ids))
print("TC Hoa Lư Coreunit: " + str(testTriggers[1].effects[3].selected_object_ids))
print("TC Thái Nguyên Coreunit: " + str(testTriggers[1].effects[4].selected_object_ids))
print("TC Chu Diên Coreunit: " + str(testTriggers[1].effects[5].selected_object_ids))
print("TC Hải Môn Coreunit: " + str(testTriggers[1].effects[6].selected_object_ids))
coreunit_DL = unit_manager.filter_units_by_reference_id(unit_reference_ids=[testTriggers[1].effects[0].selected_object_ids[0]])[0]
coreunit_TD = unit_manager.filter_units_by_reference_id(unit_reference_ids=[testTriggers[1].effects[1].selected_object_ids[0]])[0]
coreunit_BK = unit_manager.filter_units_by_reference_id(unit_reference_ids=[testTriggers[1].effects[2].selected_object_ids[0]])[0]
coreunit_HL = unit_manager.filter_units_by_reference_id(unit_reference_ids=[testTriggers[1].effects[3].selected_object_ids[0]])[0]
coreunit_TN = unit_manager.filter_units_by_reference_id(unit_reference_ids=[testTriggers[1].effects[4].selected_object_ids[0]])[0]
coreunit_CD = unit_manager.filter_units_by_reference_id(unit_reference_ids=[testTriggers[1].effects[5].selected_object_ids[0]])[0]
coreunit_HM = unit_manager.filter_units_by_reference_id(unit_reference_ids=[testTriggers[1].effects[6].selected_object_ids[0]])[0]
# print(coreunit_TD)
print("------------village area--------------")
print("area Đại La [x1 = " + str(testTriggers[0].conditions[3].area_x1) + ", x2 = " + str(
    testTriggers[0].conditions[3].area_x2) + ", y1 = " + str(
    testTriggers[0].conditions[3].area_y1) + ", y2 = " + str(testTriggers[0].conditions[3].area_y2) + "]")
print("area Tam Đái [x1 = " + str(testTriggers[1].effects[1].area_x1) + ", x2 = " + str(
    testTriggers[1].effects[1].area_x2) + ", y1 = " + str(
    testTriggers[1].effects[1].area_y1) + ", y2 = " + str(testTriggers[1].effects[1].area_y2) + "]")
print("area Bắc Kạn [x1 = " + str(testTriggers[0].conditions[2].area_x1) + ", x2 = " + str(
    testTriggers[0].conditions[2].area_x2) + ", y1 = " + str(
    testTriggers[0].conditions[2].area_y1) + ", y2 = " + str(testTriggers[0].conditions[2].area_y2) + "]")
print("area Hoa Lư [x1 = " + str(testTriggers[1].effects[3].area_x1) + ", x2 = " + str(
    testTriggers[1].effects[3].area_x2) + ", y1 = " + str(
    testTriggers[1].effects[3].area_y1) + ", y2 = " + str(testTriggers[1].effects[3].area_y2) + "]")
print("area Thái Nguyên [x1 = " + str(testTriggers[1].effects[4].area_x1) + ", x2 = " + str(
    testTriggers[1].effects[4].area_x2) + ", y1 = " + str(
    testTriggers[1].effects[4].area_y1) + ", y2 = " + str(testTriggers[1].effects[4].area_y2) + "]")
print("area Chu Diên [x1 = " + str(testTriggers[1].effects[5].area_x1) + ", x2 = " + str(
    testTriggers[1].effects[5].area_x2) + ", y1 = " + str(
    testTriggers[1].effects[5].area_y1) + ", y2 = " + str(testTriggers[1].effects[5].area_y2) + "]")
print("area Hải Môn [x1 = " + str(testTriggers[1].effects[6].area_x1) + ", x2 = " + str(
    testTriggers[1].effects[6].area_x2) + ", y1 = " + str(
    testTriggers[1].effects[6].area_y1) + ", y2 = " + str(testTriggers[1].effects[6].area_y2) + "]")
print("------------CheckTCLocation--------------")
print("TC Dai La location: [x=" + str(coreunit_DL.x) + ", y=" + str(coreunit_DL.y) + "]")
print("TC Tam Đái location: [x=" + str(coreunit_TD.x) + ", y=" + str(coreunit_TD.y) + "]")
print("TC Bắc Kạn location: [x=" + str(coreunit_BK.x) + ", y=" + str(coreunit_BK.y) + "]")
print("TC Hoa Lư location: [x=" + str(coreunit_HL.x) + ", y=" + str(coreunit_HL.y) + "]")
print("TC Thái Nguyên location: [x=" + str(coreunit_TN.x) + ", y=" + str(coreunit_TN.y) + "]")
print("TC Chu Diên location: [x=" + str(coreunit_CD.x) + ", y=" + str(coreunit_CD.y) + "]")
print("TC Hải Môn location: [x=" + str(coreunit_HM.x) + ", y=" + str(coreunit_HM.y) + "]")


# except Exception as ex:
#     print(ex)
