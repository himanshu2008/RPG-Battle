from classes.game import bcolors, Person
from classes.magic import Spell
from classes.inventory import Item
import random


# Creating Black Magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Creating White Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")

# Creating Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals for 1000 HP", 1000)

elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("Mege Elixer", "elixer", "Fully restores HP/MP of party", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, quake, cure, cura]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2},
                {"item": grenade, "quantity": 5}]
enemy_spells = [fire, quake, curaga]

# Instantiating People
player1 = Person("Valos:   ", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Himanshu:", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Jarvis:  ", 3089, 130, 288, 34, player_spells, player_items)

enemy1 = Person("Imp", 1250, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magus", 18200, 701, 525, 25, enemy_spells, [])
enemy3 = Person("Imp", 1250, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

print(bcolors.FAIL + "AN ENEMY ATTACKS!" + bcolors.ENDC)

running = True
i = 0

while running:
    print("\n")
    print("========================================================================================================")
    print("NAME               HP                                             MP")

    for player in players:
        player.get_player_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = int(input("Choose Action: "))

        # Player attack phase.
        if choice == 1:
            dmg = player.generate_damage()
            enemy = player.player_choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print(bcolors.BOLD + "You attacked", enemies[enemy].name + " for", dmg, "HP." + bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

        # Player magic choice.
        if choice == 2:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic: ")) - 1
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            if spell.cost > player.mp:
                print(bcolors.BOLD + "Not Enough MP!" + bcolors.ENDC)
                continue

            else:
                if spell.type == "black":
                    enemy = player.player_choose_target(enemies)
                    enemies[enemy].take_damage(magic_dmg)
                    print(bcolors.OKGREEN + player.name.replace(":", "") + " attacks", enemies[enemy].name + " for",
                          magic_dmg,
                          "HP." + bcolors.ENDC)

                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name + " has died.")
                        del enemies[enemy]

                if spell.type == "white":
                    player.heal_hp(magic_dmg)
                    print(bcolors.OKGREEN + bcolors.BOLD + player.name.replace(" ,:", "") + " cures for", magic_dmg,
                          "HP.")

            player.reduce_mp(spell.cost)

        # Player item choice.
        if choice == 3:
            player.choose_item()
            item_choice = int(input("    Choose Item: ")) - 1
            item = player.items[item_choice]["item"]

            if item_choice == -1:
                continue

            items = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left" + bcolors.ENDC)
                continue

            player.items[item_choice]['quantity'] -= 1

            if item.type == "potion":
                player.heal_hp(item.prop)
                print(bcolors.OKGREEN + bcolors.BOLD + player.name.replace(":", ""), "heals for ",
                      str(item.prop) + bcolors.ENDC)

            elif item.type == "elixer":

                if item.name == "Mega Elixer":

                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + bcolors.BOLD + item.name + " fully restores HP/MP." + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.player_choose_target(enemies)
                enemies[enemy].take_damage(500)
                print(bcolors.BOLD + bcolors.OKGREEN + item.name + " deals for 500 HP." + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]

    defeated_enemies = 0
    defeated_players = 0

    # Check whether battle is over.
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == 2:
        print(bcolors.BOLD + bcolors.HEADER + "You killed all enemies. Your REIGN is Safe!" + bcolors.ENDC)
        running = False

    if defeated_players == 2:
        print(bcolors.FAIL + bcolors.BOLD + "You Loose your REIGN!" + bcolors.ENDC)
        running = False

    # Enemy attack phase.
    for enemy in enemies:
        enemy_attack = random.randrange(0, 2)

        if enemy_attack == 0:
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()
            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + enemy.name.replace(" ", "") + " attacks", bcolors.ENDC + bcolors.BOLD +
                  players[target].name.replace(" ", "") + bcolors.ENDC + bcolors.FAIL + " for", enemy_dmg, "HP." + bcolors.ENDC)

        if enemy_attack == 1:
            spell, magic_dmg = enemy.enemy_choose_magic()
            enemy.reduce_mp(spell.cost)

            if spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.FAIL + enemy.name.replace(" ", "") + " attacks", bcolors.BOLD +
                      players[target].name.replace(" ", "") + bcolors.ENDC + bcolors.FAIL + " for", magic_dmg, "HP." + bcolors.ENDC)

            elif spell.type == "white":
                enemy.heal_hp(magic_dmg)
                print(bcolors.BOLD + enemy.name.replace(" ", "") + " heals!!" + bcolors.ENDC)