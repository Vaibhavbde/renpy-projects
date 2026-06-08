#--------------------------------------------------------
#                   Gacha Basic Example                 #
#--------------------------------------------------------
default figurine = False
default money = 0.0
default machine1 = ["Toy 1", "Toy 1", "Toy 2", "Toy 2", "Toy 2", "Toy 3", "figurine"]

label gacha_loop:
    show screen money_display
    while money < 1:
        $ money += 0.25
        "You pick up one quarter"

    "Now that you have a dollar, you go to the gacha machine"

    while money > 0.0:
        $ money -= 0.25
        $ chosen_figurine = renpy.random.choice(machine1)
        $ machine1.remove(chosen_figurine)

        if chosen_figurine == "figurine":
            jump figurine_picked
        else:
            if chosen_figurine == "Toy 1":
                show toy 1 at truecenter        # NEED IMAGE
            elif chosen_figurine == "Toy 2":
                show toy 2 at truecenter        # NEED IMAGE
            elif chosen_figurine == "Toy 3":
                show toy 3 at truecenter        # NEED IMAGE
            "You got [chosen_figurine]"
            hide toy                            # NEED IMAGE
            if money == 0:
                "You're out of quarters"
                jump start
            else:
                pass

label figurine_picked:
    hide screen money_display
    show figurine at truecenter
    "You got the correct figurine!"
    return

screen money_display:
    frame:
        text "$[money]"

#--------------------------------------------------------
#                   Gacha Classes Example               #
#--------------------------------------------------------

init python:
    class toy:
        def __init__(self, name, image):
            self.name = name
            self.image = image

default machine2 = [toy("Toy 1", "toy 1"), toy("Toy 1", "toy 1"), toy("Toy 2", "toy 2"), toy("Toy 2", "toy 2"), toy("Toy 2", "toy 2"), toy("Toy 2", "toy 3"), toy("Toy 3", "toy 3"), toy("Toy 4", "toy 4"), toy("Figurine", "figurine")]

label gacha_class_loop:
    show screen money_display
    while money < 1:
        $ money += 0.25
        "You pick up one quarter"

    "Now that you have a dollar, you go to the gacha machine"

    while money > 0.0:
        $ money -= 0.25
        $ rand_number = renpy.random.randint(0, (len(machine2)-1))

        if machine2[rand_number].name == "Figurine":
            jump figurine_class_picked
        else:
            $ renpy.show(machine2[rand_number].image, at_list=[truecenter])     # NEED IMAGE
            "You got [machine2[rand_number].name]"
            $ renpy.hide(machine2[rand_number].image)                           # NEED IMAGE
            $ machine2.remove(machine2[rand_number])
            if money == 0:
                "You're out of quarters"
                jump gacha_class_loop
            else:
                pass

label figurine_class_picked:
    hide screen money_display
    $ renpy.show(machine2[rand_number].image, at_list=[truecenter])             # NEED IMAGE
    "You got the correct figurine!"

    return

#--------------------------------------------------------
#              Easy Inventory Example                   #
#--------------------------------------------------------
default item_list = []

label easy_inventory:
    show screen journal
    $ item_list.append("Daisy")
    "You got a [item_list[0]]!"
    $ item_list.append("Ribbon")
    "You got a [item_list[1]]!  You also have a [item_list[0]]!"

    if "Daisy" in item_list:
        "You have a Daisy!"
        if "Medal" not in item_list:
            "You don't have a medal"
            $ item_list.remove("Daisy")
            $ item_list.append("Medal")
            "You trade a Daisy for a Medal"
    
    show screen journal
    return

screen journal:
    vpgrid:
        cols 1
        for i in item_list:
            frame xsize 200:
                text "[i]"

##                  Alternative version of Screen Journal, in case you wanted to show more text
#screen journal:
#    vpgrid:
#        rows 3
#        if "Daisy" in item_list:
#            text "Daisy - You got it from the ground"
#        if "Ribbon" in item_list:
#            text "Ribbon - You also got it from the ground"
#        if "Medal" in item_list:
#            text "Medal - You traded a Daisy for it"

#--------------------------------------------------------
#              Quantity Items Example                   #
#--------------------------------------------------------
init python:
    class item_multiple:
        def __init__(self, name, quantity=0):
            self.name = name
            self.quantity = quantity

default hp = 50
default max_hp = 100
default utilityitems = [item_multiple("Healing Potion"), item_multiple("Mana Potion", 1)]

label quantity_items:
    show screen utility_belt
    show screen hpbar
    while hp > 0:
        $ utilityitems[0].quantity += 1
        "You found a Healing Potion"
        $ hp -= renpy.random.randint(1, 20)
        "Oh No, you just got hurt!"
    "You Died!"
    return

screen hpbar:
    frame align (0.5, 0.0) xsize 500:
        bar value AnimatedValue(hp, max_hp, 0.5)

screen utility_belt:
    vbox align (0.5, 0.5):
        frame:
            textbutton "Healing Potion - [utilityitems[0].quantity]" action [SetVariable("hp", hp+20), SetField(utilityitems[0], "quantity", utilityitems[0].quantity - 1)]
        frame:
            textbutton "Mana Potion - [utilityitems[1].quantity]" action NullAction()

#--------------------------------------------------------
#              Inventory Backpack Example               #
#--------------------------------------------------------

init python:
    class item:
        def __init__(self, name, effect, effect_value):
            self.name = name
            self.effect = effect
            self.effect_value = effect_value

default rand_items = [item("Healing Potion", "heal", 10), item("Greater Healing Potion", "heal", 20)]
default rand_colors = ["Yellow Potion", "Red Potion", "Orange Potion", "Purple Potion", "Green Potion", "Blue Potion"]
default rand_effects = ["damage", "heal", "none"]
default backpack = []

label inventory_backpack:
    show screen backpack_display
    show screen hpbar
    while len(backpack) < 60:
        $ d3 = renpy.random.randint(0, 2)
        if d3 <=1:
            $ backpack.append(rand_items[d3])
        elif d3 == 2 and len(rand_colors) > 0:
            $ d20 = renpy.random.randint(1, 20)
            $ random_effect = renpy.random.choice(rand_effects)
            $ color = renpy.random.choice(rand_colors)
            $ rand_colors.remove(color)
            $ rand_items.append(item(color, random_effect, d20))
            $ backpack.append(item(color, random_effect, d20))
        else: 
            $ d6 = renpy.random.randint(2, 7)
            $ backpack.append(rand_items[d6])
        "You got a new item"
    "You've filled up your inventory."
    return

screen backpack_display:
    vpgrid:
        cols 2
        spacing 5
        rows 30
        mousewheel True
        for item in backpack:
            frame:
                if item.effect == "heal":
                    textbutton "[item.name]" action [SetVariable("hp", hp+item.effect_value), RemoveFromSet(backpack, item)]
                elif item.effect == "damage":
                    textbutton "[item.name]" action [SetVariable("hp", hp-item.effect_value), RemoveFromSet(backpack, item)]
                else:
                    textbutton "[item.name]" action RemoveFromSet(backpack, item)

#--------------------------------------------------------
#              Drag and Drop Inventory Example          #
#--------------------------------------------------------

# Define an inventory list
default inventory = ["Right Half of\nan Amulet", "Left Half of\nan Amulet", "Book", "Locket"]

label dnd_inventory:
    while "Full Amulet" not in inventory:
        show screen inventory_combine
        "You need a full amulet to continue"

    "You got the full amulet!"

    while "The Grimoire" not in inventory:
        "You need The Grimoire to continue"

    "You did it!  You got The Grimoire!"
    return

screen inventory_combine():
    vbox:
        xpos 100
        ypos 200
        spacing 10
        draggroup:
            if len(inventory)>=1:
                drag:
                    drag_name inventory[0]
                    text "[inventory[0]]"
                    draggable True
                    droppable True
                    dragged combine_check
                    xpos 100
                    ypos 100
            if len(inventory)>=2:
                drag:
                    drag_name inventory[1]
                    text "[inventory[1]]"
                    draggable True
                    droppable True
                    dragged combine_check
                    xpos 400
                    ypos 100
            if len(inventory)>=3:
                drag:
                    drag_name inventory[2]
                    text "[inventory[2]]"
                    draggable True
                    droppable True
                    dragged combine_check
                    xpos 100
                    ypos 200
            if len(inventory)>=4:
                drag:
                    drag_name inventory[3]
                    text "[inventory[3]]"
                    draggable True
                    droppable True
                    dragged combine_check
                    xpos 400
                    ypos 200

init python:
    def combine_check(drag, drop):
        if not drop:
            if drag[0].drag_name == inventory[0]:
                drag[0].snap(100, 100)
            elif drag[0].drag_name == inventory[1]:
                drag[0].snap(400, 100)
            elif drag[0].drag_name == inventory[2]:
                drag[0].snap(100, 200)
            else:
                drag[0].snap(400, 200)
            return
        if (drag[0].drag_name == "Right Half of\nan Amulet" and drop.drag_name == "Left Half of\nan Amulet") or (drag[0].drag_name == "Left Half of\nan Amulet" and drop.drag_name == "Right Half of\nan Amulet"):
            inventory.remove("Right Half of\nan Amulet")
            inventory.remove("Left Half of\nan Amulet")
            inventory.append("Full Amulet")
            renpy.hide_screen("inventory_combine")
            renpy.show_screen("inventory_combine")
            return True
        elif (drag[0].drag_name == "Book" and drop.drag_name == "Locket") or (drag[0].drag_name == "Locket" and drop.drag_name == "Book"):
            inventory.remove("Book")
            inventory.remove("Locket")
            inventory.append("The Grimoire")
            renpy.hide_screen("inventory_combine")
            renpy.show_screen("inventory_combine")
            return True
        else:
            if drag[0].drag_name == inventory[0]:
                drag[0].snap(100, 100)
            elif drag[0].drag_name == inventory[1]:
                drag[0].snap(400, 100)
            elif drag[0].drag_name == inventory[2]:
                drag[0].snap(100, 200)
            else:
                drag[0].snap(400, 200)
            return