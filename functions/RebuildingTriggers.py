class RebuildingTriggers:
    unitList = []

    def rebuild_trigger(self, source_trigger_manager, identification_name):
        # remove past triggers
        triggerStart = -1
        triggerEnd = -1
        triggerDisplayList = source_trigger_manager.trigger_display_order
        for triggerId in range(0, len(triggerDisplayList), 1):
            if source_trigger_manager.triggers[
                triggerDisplayList[triggerId]].name == "9===" + identification_name + " Start===":
                print(source_trigger_manager.triggers[triggerDisplayList[triggerId]].name)
                triggerStart = triggerId
            if source_trigger_manager.triggers[
                triggerDisplayList[triggerId]].name == "9===" + identification_name + " End===":
                print(source_trigger_manager.triggers[triggerDisplayList[triggerId]].name)
                triggerEnd = triggerId
        print(triggerStart, triggerEnd)
        print(source_trigger_manager.triggers[triggerDisplayList[triggerStart]])
        print(source_trigger_manager.triggers[triggerDisplayList[triggerEnd]])
        if triggerStart != -1 and triggerEnd != -1:
            triggerDisplayList = triggerDisplayList[:triggerStart] \
                                 + triggerDisplayList[triggerEnd + 1:]
        print("=======================================")
        print(triggerDisplayList)

        # Push to a new list (in display order)
        newTriggerList = []
        for triggerId in range(0, len(triggerDisplayList), 1):
            # print(triggerDisplayList[triggerId])
            print(source_trigger_manager.triggers[triggerDisplayList[triggerId]].trigger_id, end='')
            print(source_trigger_manager.triggers[triggerDisplayList[triggerId]].name)
            newTriggerList.append(source_trigger_manager.triggers[triggerDisplayList[triggerId]])

        return newTriggerList
