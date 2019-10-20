def show_inventory(inventory):
    inventory_desc = ("<b><u>Inventory</u></b>"
                      "<br><br>")
    for item in inventory:
        inventory_desc += "- "
        inventory_desc += item.name
        inventory_desc += "<br>"

    return inventory_desc


def get_scene_from_id(idf, scenes):
    for scene in scenes:
        if idf == scene.id:
            return scene


def try_scene_change(active_scene, scenes, direction, player):
    changed_scene = False
    if direction == "north":
        if active_scene.exit_north is not None:
            active_scene.set_leave_scene()
            active_scene = get_scene_from_id(active_scene.exit_north, scenes)
            changed_scene = True
    elif direction == "south":
        if active_scene.exit_south is not None:
            active_scene.set_leave_scene()
            active_scene = get_scene_from_id(active_scene.exit_south, scenes)
            changed_scene = True
    elif direction == "east":
        if active_scene.exit_east is not None:
            active_scene.set_leave_scene()
            active_scene = get_scene_from_id(active_scene.exit_east, scenes)
            changed_scene = True
    elif direction == "west":
        if active_scene.exit_west is not None:
            active_scene.set_leave_scene()
            active_scene = get_scene_from_id(active_scene.exit_west, scenes)
            changed_scene = True

    if changed_scene:
        description = active_scene.get_description(player)
    else:
        description = "You can't travel in that direction"
    return active_scene, description


def activate_object(scene, inventory, object_name, player):
    description = "I can't activate that"
    for scene_object in scene.objects:
        if object_name == scene_object.name:
            result = scene.activate_object(scene_object, player)
            scene = result[0]
            description = result[1]
            player = result[2]
        else:
            for alias in scene_object.aliases:
                if object_name == alias:
                    result = scene.activate_object(scene_object, player)
                    scene = result[0]
                    description = result[1]
                    player = result[2]

    for inv_object in inventory:
        if object_name == inv_object.name:
            description = inv_object.activate_description
            player = inv_object.set_player_flag_on_activate(player)
            if inv_object.change_on_activate_object is not None:
                new_object = inv_object.change_on_activate_object
                inventory[:] = [x for x in inventory if not (x.name == inv_object.name)]
                inventory.append(new_object)
            elif inv_object.should_remove_on_activate:
                inventory[:] = [x for x in inventory if not (x.name == inv_object.name)]

        else:
            for alias in inv_object.aliases:
                if object_name == alias:
                    description = inv_object.activate_description
                    player = inv_object.set_player_flag_on_activate(player)
                    if inv_object.change_on_activate_object is not None:
                        new_object = inv_object.change_on_activate_object
                        inventory[:] = [x for x in inventory if not (x.name == inv_object.name)]
                        inventory.append(new_object)
                    elif inv_object.should_remove_on_activate:
                        inventory[:] = [x for x in inventory if not (x.name == inv_object.name)]

    return scene, inventory, player, description


def combine_objects(scene, inventory, object_1_name, object_2_name):
    description = "combination failure"
    object1 = None
    object2 = None
    # check if both objects exist
    for scene_object in scene.objects:
        if object_1_name == scene_object.name:
            object1 = scene_object
        else:
            for alias in scene_object.aliases:
                if object_1_name == alias:
                    object1 = scene_object

        if object_2_name == scene_object.name:
            object2 = scene_object
        else:
            for alias in scene_object.aliases:
                if object_2_name == alias:
                    object2 = scene_object

    for inv_object in inventory:
        if object_1_name == inv_object.name:
            object1 = inv_object
        else:
            for alias in inv_object.aliases:
                if object_1_name == alias:
                    object1 = inv_object

        if object_2_name == inv_object.name:
            object2 = inv_object
        else:
            for alias in inv_object.aliases:
                if object_2_name == alias:
                    object2 = inv_object

    if object1 is not None and object2 is not None:
        result1 = object2.combine(object1, scene, inventory)
        scene = result1[1]
        inventory = result1[2]
        description = result1[3]
        if not result1[0]:
            result2 = object1.combine(object2, scene, inventory)
            scene = result2[1]
            inventory = result2[2]
            description = result2[3]

    return scene, inventory, description


def take_object(scene, inventory, object_name):
    description = "I can't take that"
    for scene_object in scene.objects:
        if object_name == scene_object.name:
            if scene_object.pick_upable:
                inventory.append(scene_object)
                scene.objects[:] = [x for x in scene.objects if not (x.name == scene_object.name)]
                description = "You take the "
                description += scene_object.name
        else:
            for alias in scene_object.aliases:
                if object_name == alias:
                    if scene_object.pick_upable:
                        inventory.append(scene_object)
                        scene.objects[:] = [x for x in scene.objects if not (x.name == scene_object.name)]
                        description = "You take the "
                        description += scene_object.name

    return scene, inventory, description


def examine_object(scene, inventory, object_name):
    description = "You're not sure what that is"
    for inv_object in inventory:
        if object_name == inv_object.name:
            description = inv_object.detailed_description
        else:
            for alias in inv_object.aliases:
                if object_name == alias:
                    description = inv_object.detailed_description

    for scene_object in scene.objects:
        if object_name == scene_object.name:
            description = scene_object.detailed_description
            scene.examine_object(scene_object.name)
        else:
            for alias in scene_object.aliases:
                if object_name == alias:
                    description = scene_object.detailed_description
                    scene.examine_object(scene_object.name)

    return description
