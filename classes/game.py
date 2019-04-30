import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkh = atk + 10
        self.atkl = atk - 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp = self.hp - dmg

        if self.hp <= 0:
            self.hp = 0

        return self.hp

    def heal_hp(self, dmg):
        self.hp = self.hp + dmg

        if self.hp >= self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):

        if self.hp <= 0:
            self.hp = 0

        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def choose_action(self):
        i = 1
        print(bcolors.OKGREEN + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "    ACTION: " + bcolors.ENDC)

        for item in self.actions:
            print("          " + str(i) + "." + item)
            i += 1

    def choose_magic(self):
        i = 1
        print(bcolors.HEADER + bcolors.BOLD + "    MAGIC: " + bcolors.ENDC)

        for spell in self.magic:
            print("        " + str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_item(self):
        i = 1
        print(bcolors.HEADER + bcolors.BOLD + "    ITEMS: " + bcolors.ENDC)

        for items in self.items:
            print("        " + str(i) + "." + items["item"].name + " " + items["item"].description, "(x" + str(items["quantity"]) + ")")
            i += 1

    def get_player_stats(self):
        hp_bar = (self.hp / self.maxhp) * 100 / 4
        hp_bar_ticks = ""

        while hp_bar > 0:
            hp_bar_ticks += "█"
            hp_bar -= 1

        while len(hp_bar_ticks) < 25:
            hp_bar_ticks += "      "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += "  "
                decreased -= 1

            current_hp += hp_string

        else:
            current_hp = hp_string

        mp_bar = (self.mp / self.maxmp) * 100 / 10
        mp_bar_ticks = ""

        while mp_bar > 0:
            mp_bar_ticks += "█"
            mp_bar -= 1

        current_mp = str(self.mp) + "/" + str(self.maxmp)

        print("                      __________________________________________                 _______________")
        print(bcolors.BOLD + bcolors.OKBLUE + self.name + "  " + current_hp + " |" + hp_bar_ticks + "|       " +
              bcolors.OKGREEN + current_mp + " |" + mp_bar_ticks + "|" + bcolors.ENDC)

    def get_enemy_stats(self):
        hp_bar = (self.hp / self.maxhp) * 100 / 2
        bar_ticks = ""

        while hp_bar > 0:
            bar_ticks += "█"
            hp_bar -= 1

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 11:
            decreased = 11 - len(hp_string)

            while decreased > 0:
                current_hp += "  "
                decreased -= 1

            current_hp += hp_string

        else:
            current_hp = hp_string

        print("                   ___________________________________________________________________________________")
        print(bcolors.BOLD + bcolors.FAIL + self.name + " " + current_hp + " |" + bar_ticks + "|" + bcolors.ENDC)

    def player_choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.BOLD + bcolors.FAIL + "    TARGET: " + bcolors.ENDC)

        for enemy in enemies:

            if enemy.get_hp != 0:
                print("        " + str(i) + "." + enemy.name)
                i += 1

        choice = int(input("    Choose Target: ")) - 1
        return choice

    def enemy_choose_magic(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        if self.hp <= self.hp/2 and self.mp < spell.cost:
            self.enemy_choose_magic()

        else:
            return spell, magic_dmg