class RebuildingTriggers:
    unitList = []

    def rebuild_trigger(self, source_trigger_manager, identification_name):
        # remove past triggers
        triggerStart = -1
        triggerEnd = -1
        triggerDisplayList = source_trigger_manager.trigger_display_order
        print("==================Old List=====================")
        print(source_trigger_manager.trigger_display_order)
        old_len = len(triggerDisplayList)
        # view  a specific trigger
        for triggerId in range(0, len(triggerDisplayList), 1):
            if source_trigger_manager.triggers[triggerDisplayList[triggerId]].name == "----Airship---------------":
                print(source_trigger_manager.triggers[triggerDisplayList[triggerId]])
        for triggerId in range(0, len(triggerDisplayList), 1):
            # Identicate remove points, start and end
            if source_trigger_manager.triggers[
                triggerDisplayList[triggerId]].name == "9===" + identification_name + " Start===":
                # print(source_trigger_manager.triggers[triggerDisplayList[triggerId]].name)
                triggerStart = triggerId
            if source_trigger_manager.triggers[
                triggerDisplayList[triggerId]].name == "9===" + identification_name + " End===":
                # print(source_trigger_manager.triggers[triggerDisplayList[triggerId]].name)
                triggerEnd = triggerId
        print(triggerStart, triggerEnd)
        # reordering after getting rid of old triggers
        if triggerStart != -1 and triggerEnd != -1:
            triggerDisplayList = triggerDisplayList[:triggerStart] \
                                 + triggerDisplayList[triggerEnd + 1:]
        print("==================New List=====================")
        # print(triggerDisplayList)

        # Push to a new list (in display order)
        newTriggerList = []
        for triggerDisplayId in range(0, old_len, 1):
            for triggerId in range(0, old_len, 1):
                for triggerDisplayId2 in range(0, len(triggerDisplayList), 1):
                    if triggerDisplayList[triggerDisplayId2] == triggerDisplayId and triggerDisplayList[triggerDisplayId2] == source_trigger_manager.triggers[triggerId].trigger_id:
                        newTrigger = source_trigger_manager.triggers[triggerId]
                        newTriggerList.append(newTrigger)
                        # print(newTrigger.name)
        print("new length: " + str(len(triggerDisplayList)) + " " + str(len(newTriggerList)))
        for triggerId in range(0, len(triggerDisplayList), 1):
            if triggerDisplayList[triggerId] > triggerEnd:
                triggerDisplayList[triggerId] = triggerDisplayList[triggerId] - (old_len - len(triggerDisplayList))
        # # view  a specific trigger
        # for trigger in newTriggerList:
        #     if trigger.name == "E_Ice Archmage":
        #         print(trigger)
        source_trigger_manager.triggers = newTriggerList
        source_trigger_manager.trigger_display_order = triggerDisplayList
        print(source_trigger_manager.trigger_display_order)
        return source_trigger_manager
