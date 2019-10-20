from scenes.scene import GameObject


def setup_starting_inventory(inventory):
    screwdriver = GameObject()
    screwdriver.pick_upable = True
    screwdriver.name = "screwdriver"
    screwdriver.detailed_description = ("One of those modern screwdrivers with a dynamic head that can adapt "
                                        "to any fixing. You got it in a cracker.")
    screwdriver.activate_description = ("You strike a pose like the Doctor and point the screwdriver firmly "
                                        "in front of you."
                                        "<br><br>"
                                        "Nothing much happens.")
    inventory.append(screwdriver)

    return inventory
