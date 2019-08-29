
import os
os.chdir(os.path.dirname(__file__))

import sys

import time

import random

SPACING = 20

MODIFIER = [4,3.5,3,2.5,2,1.5,1,.66,.5,.4,.33,.28,.25]

STATS_LIST = ['HP','ATT','DEF','SPA','SPD','SPE','ACC']

STATS_PRINT = ['HP','Attack','Defense','Special Attack','Special Defense','Speed','Accuracy']

EFFECTIVE_DICT = {'Normal': [], 'Fire': ['Grass','Ice','Steel','Bug'], 'Water': ['Fire','Ground','Rock'],'Grass': ['Water','Ground','Rock'], 'Fighting': ['Normal','Ice','Rock','Dark','Steel']\
,'Psychic': ['Fighting','Poison'],'Poison': ['Grass','Fairy'], 'Ground': ['Poison','Fire','Electric','Rock','Steel'], 'Dark': ['Ghost','Psychic'],'Electric': ['Water','Flying']\
,'Flying': ['Grass','Fighting','Bug'],'Rock': ['Fire','Ice','Flying','Bug'],'Ice': ['Grass','Ground','Flying','Dragon']\
,'Bug': ['Grass','Psychic','Dark'], 'Ghost': ['Psychic', 'Ghost'], 'Steel': ['Ice','Rock','Fairy'], 'Dragon': ['Dragon']}

NOT_EFFECTIVE_DICT = {'Normal': ['Rock','Steel'], 'Fire': ['Water','Fire','Rock','Dragon'], 'Water': ['Water','Grass','Dragon'],'Grass': ['Fire','Grass','Poison','Flying','Bug','Steel']\
,'Fighting': ['Poison','Flying','Psychic','Fairy','Bug'], 'Psychic': ['Psychic','Steel'], 'Poison': ['Poison','Ground','Rock','Ghost'], 'Ground': ['Grass','Bug']\
,'Dark': ['Fighting','Dark','Fairy'], 'Electric': ['Electric','Grass','Dragon'], 'Ghost': ['Dark'], 'Ice': ['Fire','Water','Ice','Steel'], 'Dragon': ['Steel']\
,'Bug': ['Fire','Fighting','Poison','Flying','Ghost','Steel','Fairy'], 'Flying': ['Electric','Rock','Steel'], 'Rock': ['Fighting','Ground','Steel'], 'Steel': ['Fire','Water','Electric','Steel']}

ZERO_EFFECT_DICT = {'Normal': ['Ghost'], 'Fire': [], 'Water': [],'Grass': [], 'Fighting': ['Ghost'], 'Psychic': []\
, 'Poison': ['Steel'], 'Ground': ['Flying'], 'Dark': ['Psychic'],'Electric': ['Ground'],'Flying': [],'Rock': []\
,'Bug': [], 'Ghost': ['Normal'], 'Fairy': [], 'Ice': [], 'Dragon': [], 'Steel': [],'Psychic': []}

BADGE_PACK = []

USER_BAG = []

BAG = {'heal': {},'pokeballs': {}}

REVIVES = {'Max Revive': 'all', 'Revive': 'half'}

HEALS = {'Hyper Potion': 100, 'Super Potion': 50}

POKEBALLS = {'Master Ball': 15,'Ultra Ball': 3,'Great Ball': 2, 'Pokeball': 1}

CATCH_OPPS = [[1,2,2,3,3,4],[3,4,4,5,5,5],[4,5,5,5,5,5]]

CATCH_DIF = {1:80,2:42,3:30,4:20,5:14}

FILENAME = 'pokemon_list_1.txt'

GYM = ['None','evolution','add','evolution','add','item','item','item','catch opp','evolvedeck','item','catch opp','item','item','catch opp']

POKEMON_DICTIONARY = {}

RIVAL_DECK = {}

def main():
    user_deck = {}
    rival_deck = {}
    file = open(FILENAME, 'r')
    file.readline()
    first_selection_dictionary, pokemon_choice_list = creat_first_selection_dictionary(file,9)
    pokemon = 'N'
    while pokemon == 'N':
        pokemon = pokemon_choice(pokemon_choice_list)
    print('\nYou selected {}.\n'.format(pokemon))
    time.sleep(1.2)
    user_deck[pokemon] = first_selection_dictionary.get(pokemon)
    i = pokemon_choice_list.index(pokemon)
    if i % 3 == 2:
        i -= 2
    else:
        i += 1
    rival_deck[pokemon_choice_list[i]] = first_selection_dictionary.get(pokemon_choice_list[i])
    gym = gym_battle(user_deck,'Rival', rival_deck)
    rival = gym.battle(15,14,0,0)

    gyms_completed = battle_sequence(user_deck,rival_deck,file,15,14,1,1,9,0)

    rival_deck = evolve_rival(rival_deck)
    selection_dict, choice_list = creat_first_selection_dictionary(file,3)
    for pokemon,att in selection_dict.items():
        rival_deck[pokemon] = att
    gym = gym_battle(user_deck,'Rival',rival_deck)
    rival = gym.battle(64,65,0,0)

    user_deck = choose_item(file,3,user_deck)

    index = 0
    gym = gym_battle(user_deck,'Final',None)
    gym.build_gym_deck(file)
    while advance == 'NO':
        final = gym.battle(64,65,index,0)
        if final == 'YES':
            time.sleep(3)
            advance = 'YES'
        else:
            print('Would you like to try the gym battle again Yes/No?\n')
            answer = input()
            if answer.lower() != 'yes':
                exit(0)
            index += 1
    print('Congratulations You have defeated the Champion!\nYou are now the Pokemon Champion.')

def evolve_rival(rival_deck):
    new_deck = {}
    for pokemon in rival_deck:
        if rival_deck[pokemon][4] != None:
            new_deck[rival_deck[pokemon][4]] = POKEMON_DICTIONARY[rival_deck[pokemon][4]]
        else:
            new_deck[pokemon] = POKEMON_DICTIONARY[pokemon]
    rival_deck = new_deck
    return rival_deck

def pokemon_choice(pokemon_choice_list):
    print('Choose a pokemon from the list to add to your deck:\n')
    for i in range(0,len(pokemon_choice_list)-2,3):
        print(pokemon_choice_list[i], end='')
        print(' ' * (SPACING - len(pokemon_choice_list[i])) + pokemon_choice_list[i+1], end='')
        print(' ' * (SPACING - len(pokemon_choice_list[i+1])) + pokemon_choice_list[i+2])
    pokemon = input('\n')
    pokemon = pokemon[0].upper() + pokemon[1:]
    if pokemon not in pokemon_choice_list:
        print('\nThat Pokemon is not in the list.')
        return 'N'
    return pokemon

def creat_first_selection_dictionary(file,num):
    first_selection_dictionary = {}
    pokemon_choice_list = []
    index = 0
    while index < num:
        line = file.readline()
        pokemon = line.strip().split(',')
        pok_attributes = creat_values(pokemon)
        first_selection_dictionary[pokemon[1]] = pok_attributes
        POKEMON_DICTIONARY[pokemon[1]] = pok_attributes
        pokemon_choice_list.append(pokemon[1])
        index += 1
    return first_selection_dictionary, pokemon_choice_list

def creat_values(pokemon):
    if pokemon[3] == 'None':
        pok_type = [pokemon[2]]
    else:
        pok_type = [pokemon[2],pokemon[3]]
    pok_stats = [int(pokemon[index]) for index in range(5,11)]
    pok_moves = [pokemon[11:16],pokemon[16:21],pokemon[21:26],pokemon[26:31]]
    evolution = pokemon[31]
    return [pok_type,pok_stats,pok_moves,None,evolution]

def battle_sequence(user_deck,rival_deck,file,u_level,g_level,gym_num,index,evolution_count,num):
    while gym_num <= 8:
        if gym_num == 3 or gym_num == 5:
            gym = gym_battle(user_deck,'Rival',rival_deck)
            rival = gym.battle(u_level,g_level,0,0)
        gym = gym_battle(user_deck,None,None)
        battles(gym,gym_num,file,u_level,g_level)

        if gym_num >= 7:
            count = 3
        elif gym_num >= 5:
            count = 2
        else:
            count = 1

        while count > 0:
            if GYM[index] == 'evolution':
                user_deck,rival_deck = get_evolution(user_deck,rival_deck,file,evolution_count)
                evolution_count += 3
            elif GYM[index] == 'add':
                add,att = add_pokemon(file)
                user_deck[add] = att
            elif GYM[index] == 'item':
                user_deck = choose_item(file,3,user_deck)
            elif GYM[index] == 'evolvedeck':
                evolve, n_a = creat_first_selection_dictionary(file,18)
            else:
                add,att = catch_opp(file,num)
                if add != None:
                    user_deck[add] = att
                num += 1
            count -= 1
            index += 1
        if gym_num == 1:
            u_level = 30
            g_level = 28
        elif gym_num == 3:
            u_level = 64
            g_level = 65
        gym_num += 1


def battles(gym,gym_number,file,user_level,gym_level):
    gym.build_gym_deck(file)
    advance = 'NO'
    index = 0
    while advance == 'NO':
        badge = gym.battle(user_level,gym_level,index,gym_number)
        if badge == 'YES':
            time.sleep(3)
            advance = 'YES'
        else:
            print('Would you like to try the gym battle again Yes/No?\n')
            answer = input()
            if answer.lower() != 'yes':
                exit(0)
            index += 1
    BADGE_PACK.append(gym_number)

def add_pokemon(file):
    selection_dict, choice_list = creat_first_selection_dictionary(file,3)
    pokemon = pokemon_choice(choice_list)
    i = choice_list.index(pokemon)
    att = selection_dict.get(pokemon)
    if i == 2:
        RIVAL_DECK[choice_list[0]] = selection_dict.get(choice_list[0])
    else:
        RIVAL_DECK[choice_list[i+1]] = selection_dict.get(choice_list[i+1])
    return pokemon, att

def get_evolution(user_deck,rival_deck,file,num):
    new_user_deck = {}
    new_rival_deck = {}
    evolve, n_a = creat_first_selection_dictionary(file,num)
    for pokemon in rival_deck:
        new_rival_deck[rival_deck[pokemon][4]] = POKEMON_DICTIONARY[rival_deck[pokemon][4]]
    rival_deck = new_rival_deck
    word = ' .....'
    for pokemon in user_deck:
        print('Whoa your {} is evolving! '.format(pokemon),end='')
        for l in word:
            sys.stdout.write(l)
            sys.stdout.flush()
            time.sleep(0.8)
        print()
        new_user_deck[user_deck[pokemon][4]] = evolve[user_deck[pokemon][4]]
        print('\nYour {} has evolved into a {}!\n'.format(pokemon,user_deck[pokemon][4]))
        time.sleep(1.5)
    return new_user_deck, rival_deck

def choose_item(file,number,user_deck):
    item_list = {}
    while number > 0:
        line = file.readline()
        line = line.strip().split(',')
        item_list[line[0]] = [line[1],line[2]]
        number -= 1
    print('Please select an item from the list to add to your bag.\n')
    time.sleep(1)
    print('Item', ' ' * (SPACING - 6), 'Amount')
    for item in item_list:
        print(item +  ' ' * (SPACING - len(item)), item_list[item][1])
    while True:
        pick = input('\nWhich item do you want?\n')
        pick = pick.split(' ')
        for i in range(len(pick)):
            pick[i] = pick[i][0].upper() + pick[i][1:].lower()
        pick = ' '.join(pick)
        time.sleep(1)
        if pick in item_list:
            if item_list[pick][0] == 'item':
                user_deck = evolution_stone(user_deck)
                time.sleep(1.5)
                return user_deck
            print('\nYou picked {} as your item, it has been added to your bag.\n'.format(pick))
            time.sleep(1.5)
            if item_list[pick][0] == 'heal':
                if pick in BAG['heal']:
                    BAG['heal'][pick] += item_list[pick][1]
                else:
                    BAG['heal'][pick] = int(item_list[pick][1])
                    USER_BAG.append(pick)
            else:
                if pick in BAG['pokeballs']:
                    BAG['pokeballs'][pick] += item_list[pick][1]
                else:
                    BAG['pokeballs'][pick] = int(item_list[pick][1])
            break
        else:
            print('Pick an item in the list\n')
            time.sleep(1)
    return user_deck

def evolution_stone(user_deck):
    while True:
        print('\nWhich pokemon do you want to evolve.\n')
        for pokemon in user_deck:
            if user_deck[pokemon][-1] == None:
                print(pokemon, 'can\'t evolve')
            else:
                print(pokemon)
        p = input('\n')
        p = p.split(' ')
        for i in range(len(p)):
            p[i] = p[i][0].upper() + p[i][1:].lower()
        p = ' '.join(p)
        if p in user_deck:
            break
        else:
            print('That Pokemon is not in your deck, or does not have an evolution.\n')
    new_user_deck = {}
    word = ' .....'
    for pok in user_deck:
        if pok == p:
            new_user_deck[user_deck[pok][4]] = POKEMON_DICTIONARY[user_deck[pok][4]]
            print('Whoa your {} is evolving! '.format(pok),end='')
            for l in word:
                sys.stdout.write(l)
                sys.stdout.flush()
                time.sleep(0.8)
            print()
            print('\nYour {} has evolved into a {}!\n'.format(pok,user_deck[pokemon][4]))
        else:
            new_user_deck[pok] = POKEMON_DICTIONARY[pok]
    return new_user_deck

def catch_opp(file,num):
    selection_dict, choice_list = creat_first_selection_dictionary(file,6)
    print('This is a catch opportunity! you have the opportunity to catch any of the 6 pokemon.')
    time.sleep(2.5)
    print('The number next to the pokemon is the difficutly to catch. You can continue to try')
    time.sleep(2.5)
    print('and catch a pokemon until you say Stop, a pokemon is caught, or you run out of pokeballs.')
    time.sleep(2.5)
    print('Good Luck!\n\n')
    time.sleep(1.5)
    while True:
        for i in range(len(choice_list)):
            test = choice_list[i] + ' ' * (SPACING - len(choice_list[i])) + str(CATCH_OPPS[num][i])
            sys.stdout.write(test)
            print()
            sys.stdout.flush()
            time.sleep(0.8)
        time.sleep(0.8)
        print('\nStop')
        time.sleep(1.5)
        pokemon = input('\nWhich one do you want to try and catch?\n')
        time.sleep(1)
        pokemon = pokemon[0].upper() + pokemon[1:]
        if pokemon == 'Stop':
            break
        elif pokemon not in choice_list:
            print('\nThat Pokemon is not in the list.')
        elif len(BAG['pokeballs']) == 0:
            print('Sorry you are out of pokeballs.\n')
            break
        else:
            balls = []
            print('\nWhat pokeball would you like to use?\n')
            time.sleep(1)
            for ball in BAG['pokeballs']:
                print(ball + ' ' * SPACING + str(BAG['pokeballs'][ball]))
                balls.append(ball)
            while True:
                b = input('\n')
                b = b.split(' ')
                for i in range(len(b)):
                    b[i] = b[i][0].upper() + b[i][1:].lower()
                b = ' '.join(b)
                if b not in balls:
                    print('\nThat pokeball is not in the list.')
                    time.sleep(1)
                else:
                    if BAG['pokeballs'][b] == 1:
                        BAG['pokeballs'].pop(b)
                    else:
                        BAG['pokeballs'][b] -= 1
                    catch = catch_attempt(pokemon,b,num,choice_list)
                    if catch == 'YES':
                        att = selection_dict.get(pokemon)
                        return pokemon, att
                    else:
                        print('Try again.\n')
                        break
    time.sleep(1)
    return None, None

def catch_attempt(pokemon,ball,num,choice_list):
    print('You threw a {} at {}!'.format(ball,pokemon))
    word = '.....'
    for l in word:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(0.8)
    print()
    time.sleep(1)
    dif = CATCH_DIF[CATCH_OPPS[num][choice_list.index(pokemon)]]
    percent = dif * POKEBALLS[ball]
    number = random.randint(1,101)
    if number <= percent:
        print('Congratulations! You caught {}.\n'.format(pokemon))
        time.sleep(1.5)
        return 'YES'
    else:
        print('AWH! You almost had it.\n')
        time.sleep(1.5)
        return 'NO'

class gym_battle:

    def __init__(self, user_deck,trainer,deck):
        self._u_deck = user_deck
        self._u_cond = [6,6,6,6,6,6,6]
        self._u_faint = 0
        self._gym_deck = {}
        self._gym_cond = [6,6,6,6,6,6,6]
        self._gym_faint = 0
        self._poke_hp = {}
        self._user_skip = None
        self._gym_skip = None
        self._u_value = None
        self._gym_value = None
        self._u_set_move = None
        self._gym_set_move = None
        self._trainer = trainer
        self._deck = deck
        if self._deck != None:
            self._gym_deck = self._deck

    def build_gym_deck(self,file):
        nums = file.readline()
        pok = []
        deck = 0
        index = 0
        while deck < int(nums[0]):
            num = random.randint(0,int(nums[2])-1)
            while index < int(nums[2]):
                pok.append(file.readline())
                index += 1
            line = pok[num]
            pokemon = line.strip().split(',')
            self._gym_deck[pokemon[1]] = creat_values(pokemon)
            pok = []
            index = 0
            deck += 1

    def choose_user_starter(self):
        print('We will now move on to the next battle.\n')
        time.sleep(1.6)
        print('Please select a Pokemon from your deck to start the battle:\n')
        time.sleep(1.4)
        for pokemon in self._u_deck:
            print(pokemon, '\n', end='')
            time.sleep(0.8)
        while True:
            pokemon = input('\nWhich Pokemon do you want to start the battle?\n')
            pokemon = pokemon.split(' ')
            for i in range(len(pokemon)):
                pokemon[i] = pokemon[i][0].upper() + pokemon[i][1:].lower()
            pokemon = ' '.join(pokemon)
            if pokemon in self._u_deck:
                break
            else:
                print('That Pokemon is not in your deck, pick a pokemon in your deck.\n')
        time.sleep(1)
        return pokemon

    def get_gym_starter(self):
        for pokemon in self._gym_deck:
            return pokemon

    def u_move(self,user_move,u_start,gym_start,level):
        skip = None
        acc = self.check_accuracy(user_move,'U')
        for d in self._gym_deck[gym_start][0]:
            if d in ZERO_EFFECT_DICT[user_move[1]]:
                skip = 'YES'
        if acc == 'YES':
            print('{} used {},'.format(u_start,user_move[0]), end='')
            if user_move[2][0] == 'L':
                damage = self.lower_move(gym_start,user_move,'U')

            elif user_move[2][0] == 'I':
                damage = self.increase_move(u_start,user_move,'U')

            elif user_move[2][0] == 'C':
                S = user_move[2][1:6]
                A = user_move[2][7:]
                if skip != None:
                    print('{} is not effective against {}.\n'.format(user_move[0],gym_start))
                else:
                    user_move[2] = A
                    damage = self.attack_move(user_move,u_start,gym_start,'U',level)
                user_move[2] = S
                if S[0] == 'L':
                    damage = self.lower_move(gym_start,user_move,'U')
                elif S[0] == 'D':
                    damage = self.lower_move(u_start,user_move,'G')
                else:
                    damage = self.increase_move(u_start,user_move,'U')
                user_move[2] = 'C' + S + '.' + A

            elif user_move[2][0] == 'G':
                if skip != None:
                    print('{} is not effective against {}.\n'.format(user_move[0],gym_start))
                    damage = 0
                else:
                    user_move[2] = user_move[2][1:]
                    damage = self.attack_move(user_move,u_start,gym_start,'U',level)
                    self._u_deck[u_start][1][0] += int(damage // 2)
                    if self._u_deck[u_start][1][0] > self._poke_hp[u_start]:
                        self._u_deck[u_start][1][0] = self._poke_hp[u_start]

            elif user_move[2][0] == 'D':
                one = user_move[2][1:6]
                two = user_move[2][7:]
                user_move[2] = one
                damage = self.increase_move(u_start,user_move,'U')
                user_move[2] = two
                damage = self.increase_move(u_start,user_move,'U')
                user_move[2] = 'D' + one + '.' + two

            elif user_move[2][0] == 'M':
                damage = self.modifier_move(user_move,u_start,gym_start,'U')
                if user_move[2][1] == 'A':
                    if skip != None:
                        print('{} is not effective against {}.\n'.format(user_move[0],gym_start))
                        damage = 0
                    else:
                        temp = user_move[2]
                        att = user_move[2].split('.')
                        user_move[2] = att[1]
                        damage = self.attack_move(user_move,u_start,gym_start,'U',level)
                        user_move[2] = temp

            elif user_move[2][0] == 'P':
                temp = user_move[2]
                split = user_move[2].split('.')
                check_percent = self.check_per(split[2])
                if skip != None:
                    print('{} is not effective against {}.\n'.format(user_move[0],gym_start))
                else:
                    user_move[2] = split[1]
                    damage = self.attack_move(user_move,u_start,gym_start,'U',level)
                    if check_percent == 'YES':
                        if split[0][1:] == 'skip':
                            damage = self.skip_move(user_move,u_start,gym_start,'U')
                            if damage != 0:
                                time.sleep(1.5)
                                print(' the opponents {} is frozen solid.\n'.format(gym_start))
                        elif split[0][1] == 'L':
                            user_move[2] = 'L' + split[3]
                            damage = self.lower_move(gym_start,user_move,'U')
                        elif split[0][1] == 'M':
                            user_move[2] = 'MN'
                            damage = self.modifier_move(user_move,u_start,gym_start,'U')
                            time.sleep(1.5)
                            print(' the opponents was effected by the move.\n'.format(gym_start))
                user_move[2] = temp

            elif user_move[2][0] == 'T':
                if self._u_value == None:
                    self._u_value = 'in air/sky'
                    self._gym_skip = 1
                    damage = 0
                    print()
                    print()
                if self._u_value == 0:
                    if skip != None:
                        print('{} is not effective against {}.\n'.format(user_move[0],gym_start))
                        damage = 0
                    else:
                        temp = user_move[2]
                        user_move[2] = user_move[2][1:]
                        damage = self.attack_move(user_move,u_start,gym_start,'U',level)
                        user_move[2] = temp
                    self._u_value = None
                    self._u_set_move = None
                else:
                    self._u_value = 0
                    self._u_set_move = user_move

            elif user_move[2][0:3] == 'set':
                if skip != None:
                    print('{} is not effective against {}.\n'.format(user_move[0],gym_start))
                    damage = 0
                else:
                    damage = int(user_move[2][3:])
                    self._gym_deck[gym_start][1][0] -= damage

            elif user_move[2][0:5] == 'reach':
                if skip != None:
                    print('{} is not effective against {}.\n'.format(user_move[0],gym_start))
                else:
                    temp = user_move[2]
                    user_move[2] = user_move[2][5:]
                    damage = self.attack_move(user_move,u_start,gym_start,'U',level)
                    user_move[2] = temp
                    self._user_skip = 'r'
                    self._u_set_move = 'reach'

            elif user_move[2] == 'protect':
                self._gym_skip = 1
                user_move[3] = user_move[3] * 0.66667
                print(' and protected its self.\n')
                damage = 0

            elif user_move[2] == 'heal':
                hp = self._poke_hp[u_start] // 2
                if (self._u_deck[u_start][1][0] + hp) > self._poke_hp[u_start]:
                    hp = self._poke_hp[u_start] - self._u_deck[u_start][1][0]
                self._u_deck[u_start][1][0] += hp
                print(' it healed {} hp.\n'.format(hp))
                damage = 0

            elif user_move[2] == 'skip':
                damage = self.skip_move(user_move,u_start,gym_start,'U')
                if damage != 0:
                    print(' and {} started to fall asleep.\n'.format(gym_start))
                    damge = 0

            else:
                if skip != None:
                    print('{} is not effective against {}.\n'.format(user_move[0],gym_start))
                    damage = 0
                else:
                    damage = self.attack_move(user_move,u_start,gym_start,'U',level)
            time.sleep(2)
        else:
            print('{} used {}, and it missed.\n'.format(u_start,user_move[0]))
            time.sleep(2)

    def opp_move(self,gym_move,u_start,gym_start,level):
        skip = None
        acc = self.check_accuracy(gym_move,'G')
        for d in self._u_deck[u_start][0]:
            if d in ZERO_EFFECT_DICT[gym_move[1]]:
                skip = 'YES'
        if acc == 'YES':
            print('{} used {},'.format(gym_start,gym_move[0]), end='')
            if gym_move[2][0] == 'L':
                damage = self.lower_move(u_start,gym_move,'G')

            elif gym_move[2][0] == 'I':
                damage = self.increase_move(gym_start,gym_move,'G')

            elif gym_move[2][0] == 'C':
                S = gym_move[2][1:6]
                A = gym_move[2][7:]
                if skip != None:
                    print('{} is not effective against {}.\n'.format(gym_move[0],u_start))
                else:
                    gym_move[2] = A
                    damage = self.attack_move(gym_move,u_start,gym_start,'G',level)
                gym_move[2] = S
                if S[0] == 'L':
                    damage = self.lower_move(u_start,gym_move,'G')
                elif S[0] == 'D':
                    damage = self.lower_move(gym_start,gym_move,'U')
                else:
                    damage = self.increase_move(gym_start,gym_move,'G')
                gym_move[2] = 'C' + S + '.' + A

            elif gym_move[2][0] == 'G':
                if skip != None:
                    print('{} is not effective against {}.\n'.format(gym_move[0],u_start))
                    damage = 0
                else:
                    gym_move[2] = gym_move[2][1:]
                    damage = self.attack_move(gym_move,u_start,gym_start,'G',level)
                    self._gym_deck[gym_start][1][0] += damage
                    if self._gym_deck[gym_start][1][0] > self._poke_hp[gym_start]:
                        self._gym_deck[gym_start][1][0] = self._poke_hp[gym_start]

            elif gym_move[2][0] == 'D':
                one = gym_move[2][1:6]
                two = gym_move[2][7:]
                gym_move[2] = one
                damage = self.increase_move(gym_start,gym_move,'G')
                gym_move[2] = two
                damage = self.increase_move(gym_start,gym_move,'G')
                gym_move[2] = 'D' + one + '.' + two

            elif gym_move[2][0] == 'M':
                damage = self.modifier_move(gym_move,u_start,gym_start,'G')
                if gym_move[2][1] == 'A':
                    if skip != None:
                        print('{} is not effective against {}.\n'.format(gym_move[0],u_start))
                    else:
                        temp = gym_move[2]
                        att = gym_move[2].split('.')
                        gym_move[2] = att[1]
                        damage = self.attack_move(gym_move,u_start,gym_start,'G',level)
                        gym_move[2] = temp

            elif gym_move[2][0] == 'P':
                temp = gym_move[2]
                split = gym_move[2].split('.')
                check_percent = self.check_per(split[2])
                if skip != None:
                    print('{} is not effective against {}.\n'.format(gym_move[0],u_start))
                else:
                    gym_move[2] = split[1]
                    damage = self.attack_move(gym_move,u_start,gym_start,'G',level)
                    if chek_percent == 'YES':
                        if split[0][1:] == 'skip':
                            damage = self.skip_move(gym_move,u_start,gym_start,'G')
                            if damage != 0:
                                time.sleep(1.5)
                                print(' the opponents {} is frozen solid.\n'.format(u_start))
                        elif gym_move[2][1] == 'L':
                            gym_move[2] = 'L' + split[3]
                            damage = self.lower_move(u_start,gym_move,'G')
                        elif gym_move[2][1] == 'M':
                            gym_move[2] = 'MN'
                            damage = self.modifier_move(gym_move,u_start,gym_start,'G')
                            time.sleep(1.5)
                            print(' the opponents was effected by the move.\n'.format(u_start))
                gym_move[2] = temp
                print(gym_move[2])

            elif gym_move[2][0] == 'T':
                if self._gym_value == None:
                    self._gym_value = 'in air/sky'
                    self._user_skip = 1
                    damage = 0
                    print()
                    print()
                if self._gym_value == 0:
                    if skip != None:
                        print('{} is not effective against {}.\n'.format(gym_move[0],u_start))
                        damage = 0
                    else:
                        temp = gym_move[2]
                        gym_move[2] = gym_move[2][1:]
                        damage = self.attack_move(gym_move,u_start,gym_start,'G',level)
                        gym_move[2] = temp
                    self._gym_value = None
                    self._gym_set_move = None
                else:
                    self._gym_value = 0
                    self._gym_set_move = gym_move

            elif gym_move[2][0:3] == 'set':
                if skip != None:
                    print('{} is not effective against {}.\n'.format(gym_move[0],u_start))
                    damage = 0
                else:
                    damage = int(user_move[2][3:])
                    self._u_deck[u_start][1][0] -= damage

            elif gym_move[2][0:5] == 'reach':
                if skip != None:
                    print('{} is not effective against {}.\n'.format(gym_move[0],u_start))
                else:
                    temp = gym_move[2]
                    gym_move[2] = gym_move[2][5:]
                    damage = self.attack_move(gym_move,u_start,gym_start,'G',level)
                    gym_move[2] = temp
                    self._gym_skip = 'r'
                    self._gym_set_move = 'reach'

            elif gym_move[2] == 'protect':
                self._user_skip = 1
                gym_move[3] = gym_move[3] * 0.66667
                print(' and protected its self.\n')
                damage = 0

            elif gym_move[2] == 'heal':
                hp = self._poke_hp[gym_start] // 2
                if (self._gym_deck[gym_start][1][0] + hp) > self._poke_hp[gym_start]:
                    hp = self._poke_hp[gym_start] - self._gym_deck[gym_start][1][0]
                self._gym_deck[gym_start][1][0] += hp
                print(' it healed {} hp.\n'.format(hp))
                damage = 0

            elif gym_move[2] == 'skip':
                damage = self.skip_move(gym_move,u_start,gym_start,'G')
                if damage != 0:
                    print(' and {} started to fall asleep.\n'.format(u_start))
                    damge = 0

            else:
                if skip != None:
                    print('{} is not effective against {}.\n'.format(gym_move[0],u_start))
                    damage = 0
                else:
                    damage = self.attack_move(gym_move,u_start,gym_start,'G',level)
            time.sleep(2)
        else:
            print('{} used {}, and it missed.\n'.format(gym_start,gym_move[0]))
            time.sleep(2)

    def base_hp(self):
        for pokemon in self._u_deck:
            self._poke_hp[pokemon] = self._u_deck[pokemon][1][0]
        for pokemon in self._gym_deck:
            self._poke_hp[pokemon] = self._gym_deck[pokemon][1][0]

    def reset_deck(self):
        for pokemon in self._u_deck:
            self._u_deck[pokemon][1][0] = self._poke_hp[pokemon]
            self._u_deck[pokemon][3] = None
        for pokemon in self._gym_deck:
            self._gym_deck[pokemon][1][0] = self._poke_hp[pokemon]
            self._gym_deck[pokemon][3] = None
        self._u_cond = [6,6,6,6,6,6,6]
        self._gym_cond = [6,6,6,6,6,6,6]

    def battle(self,ulevel,gymlevel,index,g_num):

        if index > 0:
            self.reset_deck()

        self.base_hp()

        u_start = self.choose_user_starter()
        gym_start = self.get_gym_starter()

        if self._trainer == 'Rival':
            print('\nRival Duel Gary: {} vs. {}\n'.format(gym_start,u_start))
        elif self._trainer == 'Final':
            print('\nFinal Battle Champion: {} vs. {}\n'.format(gym_start,u_start))
        else:
            print('\nGYM BATTLE {}: {} vs. {}\n'.format(str(g_num),gym_start,u_start))
        time.sleep(2.5)

        while True:
            print('{}\'s HP is {}, {}\'s HP is {}\n'.format(gym_start,self._gym_deck[gym_start][1][0],u_start,self._u_deck[u_start][1][0]))
            time.sleep(2.2)
            if self._u_set_move == None:
                d, pok = self.decision(u_start)
            else:
                d = self._u_set_move
            if self._gym_set_move == None:
                gym_move = self.gym_pokemon_move(gym_start)
            else:
                gym_move = self._gym_set_move
            gym_turn = ''
            if d == 'skip':
                u_start = pok
                if self.check_skip(u_start,gym_start,'G') != 'skip'and gym_turn != 'skip':
                    if self._gym_skip == 1 or self._gym_skip == 'r':
                        if self._gym_skip == 1:
                            print('{} used {}, and it missed.\n'.format(gym_start,gym_move[0]))
                        else:
                            self._gym_set_move = None
                            print('{} must recharge.\n'.format(gym_start))
                        self._gym_skip = None
                        time.sleep(2)
                    else:
                        self.opp_move(gym_move,u_start,gym_start,gymlevel)
                    if self._u_deck[u_start][1][0] <= 0:
                        faint = self.user_faint(u_start)
                        if faint != 'NO':
                            u_start = faint
                            u_turn = 'skip'
                        else:
                            badge = 'NO'
                            break
            else:
                user_move = d
                speed = self.check_speed(u_start,user_move,gym_start,gym_move)
                u_turn = ''
                if speed == 'U':
                    if self.check_skip(u_start,gym_start,'U') != 'skip':
                        if self._user_skip == 1 or self._user_skip == 'r':
                            if self._user_skip == 1:
                                print('{} used {}, and it missed.\n'.format(u_start,user_move[0]))
                            else:
                                self._u_set_move = None
                                print('{} must recharge.\n'.format(u_start))
                            self._user_skip = None
                            time.sleep(2)
                        else:
                            self.u_move(user_move,u_start,gym_start,ulevel)
                        if self._gym_deck[gym_start][1][0] <= 0:
                            faint = self.gym_faint(gym_start)
                            if faint == 'YES':
                                badge = 'YES'
                                break
                            else:
                                gym_start = faint
                                gym_turn = 'skip'
                    if self.check_skip(u_start,gym_start,'G') != 'skip' and gym_turn != 'skip':
                        if self._gym_skip == 1 or self._gym_skip == 'r':
                            if self._gym_skip == 1:
                                print('{} used {}, and it missed.\n'.format(gym_start,gym_move[0]))
                            else:
                                self._gym_set_move = None
                                print('{} must recharge.\n'.format(gym_start))
                            self._gym_skip = None
                            time.sleep(2)
                        else:
                            self.opp_move(gym_move,u_start,gym_start,gymlevel)
                        if self._u_deck[u_start][1][0] <= 0:
                            faint = self.user_faint(u_start)
                            if faint != 'NO':
                                u_start = faint
                                u_turn = 'skip'
                            else:
                                badge = 'NO'
                                break
                else:
                    if gym_turn != 'skip':
                        if self.check_skip(u_start,gym_start,'G') != 'skip':
                            if self._gym_skip == 1 or self._gym_skip == 'r':
                                if self._gym_skip == 1:
                                    print('{} used {}, and it missed.\n'.format(gym_start,gym_move[0]))
                                else:
                                    self._gym_set_move = None
                                    print('{} must recharge.\n'.format(gym_start))
                                self._gym_skip = None
                                time.sleep(2)
                            else:
                                self.opp_move(gym_move,u_start,gym_start,gymlevel)
                            if self._u_deck[u_start][1][0] <= 0:
                                faint = self.user_faint(u_start)
                                if faint != 'NO':
                                    u_start = faint
                                else:
                                    badge = 'NO'
                                    break
                    if u_turn != 'skip':
                        if self.check_skip(u_start,gym_start,'U') != 'skip':
                            if self._user_skip == 1 or self._user_skip == 'r':
                                if self._user_skip == 1:
                                    print('{} used {}, and it missed.\n'.format(u_start,user_move[0]))
                                else:
                                    self._u_set_move = None
                                    print('{} must recharge.\n'.format(u_start))
                                self._user_skip = None
                                time.sleep(2)
                            else:
                                self.u_move(user_move,u_start,gym_start,ulevel)
                            if self._gym_deck[gym_start][1][0] <= 0:
                                faint = self.gym_faint(gym_start)
                                if faint == 'YES':
                                    badge = 'YES'
                                    break
                                else:
                                    gym_start = faint
            badge, u, g = self.check_modifier(u_start,gym_start)
            if badge != '':
                break
            else:
                u_start = u
                gym_start = g
        return badge

    def check_accuracy(self,move,L):
        if move[3] == 'I':
            return 'YES'
        if L == 'U':
            acc = int(float(move[3]) * float(MODIFIER[self._u_cond[6]]))
        else:
            acc = int(float(move[3]) * float(MODIFIER[self._gym_cond[6]]))
        num = random.randint(1,100)
        if num <= acc:
            return 'YES'
        return 'NO'

    def check_skip(self,u_start,gym_start,L):
        if L == 'U':
            if type(self._u_deck[u_start][3]) == list:
                if self._u_deck[u_start][3][0] == 0:
                    self._u_deck[u_start][3] = None
                    return 'YES'
                self._u_deck[u_start][3][0] -= 1
                print('{} turn was skipped do to sleep or frozen.\n'.format(u_start))
                time.sleep(2)
                return 'skip'
        else:
            if type(self._gym_deck[gym_start][3]) == list:
                if self._gym_deck[gym_start][3][0] == 0:
                    self._gym_deck[gym_start][3] = None
                    return 'YES'
                self._gym_deck[gym_start][3][0] -= 1
                print('{} turn was skipped do to sleep or frozen.\n'.format(gym_start))
                time.sleep(2)
                return 'skip'
        return 'YES'


    def check_modifier(self,u_start,gym_start):
        if self._gym_deck[gym_start][3] != None and type(self._gym_deck[gym_start][3]) != list:
            self._gym_deck[gym_start][1][0] += self._gym_deck[gym_start][3]
            if self._gym_deck[gym_start][3] > 0:
                print('The opponents {} gained {} hp.\n'.format(gym_start,self._gym_deck[gym_start][3]))
            else:
                print('The opponents {} lost {} hp.\n'.format(gym_start,self._gym_deck[gym_start][3]))
            if self._gym_deck[gym_start][1][0] > self._poke_hp[gym_start]:
                    self._gym_deck[gym_start][1][0] = self._poke_hp[gym_start]
            if self._gym_deck[gym_start][1][0] <= 0:
                faint = self.gym_faint(gym_start)
                if faint == 'YES':
                    return 'YES', None, None
                else:
                    g = faint
            else:
                g = gym_start
        else:
                g = gym_start
        if self._u_deck[u_start][3] != None and type(self._u_deck[u_start][3]) != list:
            self._u_deck[u_start][1][0] += self._u_deck[u_start][3]
            if self._u_deck[u_start][3] > 0:
                print('Your {} gained {} hp.\n'.format(u_start,self._u_deck[u_start][3]))
            else:
                print('Your {} lost {} hp.\n'.format(u_start,self._u_deck[u_start][3]))
            if self._u_deck[u_start][1][0] > self._poke_hp[u_start]:
                    self._u_deck[u_start][1][0] = self._poke_hp[u_start]
            if self._u_deck[u_start][1][0] <= 0:
                faint = self.user_faint(u_start)
                if faint != 'NO':
                    u = faint
                else:
                    return 'NO', None, None
            else:
                u = u_start
        else:
                u = u_start
        return '', u, g

    def check_speed(self,user,user_move,gym,gym_move):
        user_speed = self._u_deck[user][1][-1] * (MODIFIER[self._u_cond[5]])
        gym_speed = self._gym_deck[gym][1][-1] * (MODIFIER[self._gym_cond[5]])
        if (user_speed >= gym_speed and gym_move[0][-2] != 'W') or user_move[0][-2] == 'W':
            speed = 'U'
        else:
            speed = 'G'
        return speed

    def gym_faint(self,pokemon):
        if self._trainer == 'Rival':
            print('The Rival\'s {} has fainted.\n'.format(pokemon))
        elif self._trainer == 'Final':
            print('The Champion\'s {} has fainted.\n'.format(pokemon))
        else:
            print('The gym leaders {} has fainted.\n'.format(pokemon))
        time.sleep(1.5)
        self._gym_deck[pokemon][1][0] = 'faint'
        self._gym_faint += 1
        if self._gym_faint == len(self._gym_deck):
            if self._trainer == 'Rival':
                print('All of the Rival\'s pokemon have fainted!\n')
                time.sleep(1)
                print('Congratulations you defeated Gary!\n')
            elif self._trainer == 'Final':
                print('All of the Champion\'s pokemon have fainted!\n')
                time.sleep(1)
                print('Congratulations you defeated the Champion!\n')
            else:
                print('All of the gym leaders pokemon have fainted!\n')
                time.sleep(1)
                print('Congratulations you defeated the gym!\n')
            self.reset_user_deck()
            return 'YES'
        else:
            for pok in self._gym_deck:
                if self._gym_deck[pok][1][0] != 'faint':
                    self._gym_cond = [6,6,6,6,6,6,6]
                    return pok

    def user_faint(self,pokemon):
        print('Your {} has fainted.\n'.format(pokemon))
        time.sleep(1.5)
        self._u_deck[pokemon][1][0] = 'faint'
        self._u_faint += 1
        if self._u_faint == len(self._u_deck):
            print('All of your pokemon have fainted, you lost the gym battle.\n')
            return 'NO'
        else:
            for pok in self._u_deck:
                if self._u_deck[pok][1][0] == 'faint':
                    print(pok, 'faint')
                else:
                    print(pok)
        print()
        time.sleep(1.5)
        while True:
            choice = input('Which pokemon do you want to put in?\n')
            choice = choice[0].upper() + choice[1:].lower()
            if choice in self._u_deck:
                if self._u_deck[choice][1][0] == 'faint':
                    print('That Pokemon is fainted, pick another pokemon.\n')
                    time.sleep(1.5)
                else:
                    self._u_cond = [6,6,6,6,6,6,6]
                    return choice
            else:
                print('That Pokemon is not in your deck, pick a pokemon in your deck.\n')
                time.sleep(1.5)

    def reset_user_deck(self):
        for pokemon in self._u_deck:
            self._u_deck[pokemon][1][0] = self._poke_hp[pokemon]
            self._u_deck[pokemon][3] = None

    def decision(self,pokemon):
        while True:
            print('What do you want to do?\n')
            time.sleep(0.8)
            print('Pick a move' + ' ' * 5 + 'Pick an item from bag' + ' ' * 5 + 'Swap Pokemon\n')
            pick = input()
            time.sleep(1)
            if pick.lower() == 'pick a move':
                d = self.user_pokemon_move(pokemon)
                pok = None
                break
            elif pick.lower() == 'pick an item from bag':
                time.sleep(1)
                if len(USER_BAG) == 0:
                    print('\nYou do not have any items in your bag.\n')
                else:
                    choice = self.open_bag()
                    if choice == 'YES':
                        d = 'skip'
                        pok = pokemon
                        break
            elif pick.lower() == 'swap pokemon':
                choice = self.swap_pokemon(pokemon)
                if choice != 'NO':
                    d = 'skip'
                    pok = choice
                    self._u_cond = [6,6,6,6,6,6,6]
                    break
            else:
                print('Pick one of the three options.\n')
                time.sleep(1.5)
        time.sleep(0.8)
        return d, pok

    def open_bag(self):
        print('\nUser BAG:\n')
        for item in USER_BAG:
            print(item)
        print('Exit')
        print()
        while True:
            pick = input('What Item do you want to use from your bag?\n')
            pick = pick.split(' ')
            time.sleep(1)
            for i in range(len(pick)):
                pick[i] = pick[i][0].upper() + pick[i][1:].lower()
            pick = ' '.join(pick)
            if pick in USER_BAG:
                time.sleep(1)
                if pick == 'Max Revive' or pick == 'Revive':
                    b = self.revive(pick)
                    if b == 'YES':
                        break
                else:
                    self.hp_boost(pick)
                    break
            elif pick == 'Exit':
                return 'NO'
            else:
                print('Pick a valid item.\n')
                time.sleep(1)
        return 'YES'

    def hp_boost(self,pick):
        print('\nwhich pokemon do you want to use {} on?\n'.format(pick))
        for pokemon in self._u_deck:
            if self._u_deck[pokemon][1][0] == 'faint':
                print(pokemon, 'faint')
            else:
                print(pokemon)
        while True:
            choice = input('\n')
            choice = choice[0].upper() + choice[1:].lower()
            if choice in self._u_deck:
                if self._u_deck[choice][1][0] == 'faint':
                    print('That Pokemon\'s HP is 0, that item has no effect on it.\n')
                    time.sleep(1.5)
                else:
                    hp = HEALS[pick]
                    self._u_deck[choice][1][0] += hp
                    if self._u_deck[choice][1][0] > self._poke_hp[choice]:
                        self._u_deck[choice][1][0] = self._poke_hp[choice]
                    time.sleep(1.5)
                    break
            else:
                print('That Pokemon is not in your deck, pick a pokemon in your deck.\n')
                time.sleep(1.5)
        print(BAG['heal'][pick])
        if BAG['heal'][pick] == 1:
            BAG['heal'].pop(pick)
            USER_BAG.remove(pick)
        else:
            BAG['heal'][pick] -= 1

    def revive(self,pick):
        print('which pokemon do you want to use {} on?\n'.format(pick))
        for pokemon in self._u_deck:
            if self._u_deck[pokemon][1][0] == 'faint':
                print(pokemon, 'faint')
            else:
                print(pokemon)
        while True:
            choice = input('\n')
            choice = choice[0].upper() + choice[1:].lower()
            if choice in self._u_deck:
                if self._u_deck[choice][1][0] == 'faint':
                    if pick == 'Max Revive':
                        self._u_deck[choice][1][0] = self._poke_hp[choice]
                    else:
                        hp = self._poke_hp[choice] // 2
                        self._u_deck[choice][1][0] = hp
                    print('That Pokemon\'s HP has been restored!\n')
                    time.sleep(1.5)
                    break
                else:
                    print()
                    return 'NO'
            else:
                print('That Pokemon is not in your deck, pick a pokemon in your deck.\n')
                time.sleep(1.5)
        if BAG['heal'][pick] == 1:
            BAG['heal'].pop(pick)
            USER_BAG.remove(pick)
        else:
            BAG['heal'][pick] -= 1
        return 'YES'


    def gym_pokemon_move(self,pokemon):
        num = random.randint(1,101)
        if num >= 1 and num <= 25:
            move = self._gym_deck[pokemon][2][0]
        elif num <= 50:
            move = self._gym_deck[pokemon][2][1]
        elif num <= 75:
            move = self._gym_deck[pokemon][2][2]
        else:
            move = self._gym_deck[pokemon][2][3]
        return move

    def user_pokemon_move(self,pokemon):
        user_moves = [item[0] for item in self._u_deck[pokemon][2]]
        print('\nWhich move do you want to pick?\n' + user_moves[0] + ' ' * (SPACING - len(user_moves[0])) + user_moves[1] + '\n' + user_moves[2] + ' ' * (SPACING - len(user_moves[2])) + user_moves[3] + '\n')
        time.sleep(1)
        while True:
            pick = input()
            pick = pick.split(' ')
            try:
                for i in range(len(pick)):
                    pick[i] = pick[i][0].upper() + pick[i][1:].lower()
                pick = ' '.join(pick)
            except:
                pick = 'nlnsl'
            if pick[-2:] == 'w)':
                pick = pick[0:-3] + '(W)'
            if pick in user_moves:
                break
            else:
                print('Pick a valid move.\n')
        print()
        time.sleep(1)
        index = user_moves.index(pick)
        move = self._u_deck[pokemon][2][index]
        return move

    def swap_pokemon(self,pok):
        print('\n' + pok)
        for pokemon in self._u_deck:
            if pokemon != pok:
                if self._u_deck[pokemon][1][0] == 'faint':
                    print(pokemon, 'faint')
                else:
                    print(pokemon)
        print()
        time.sleep(1.5)
        while True:
            choice = input('Which pokemon do you want to choose?\n')
            choice = choice[0].upper() + choice[1:].lower()
            if choice in self._u_deck:
                if choice == pok:
                    print()
                    return 'NO'
                elif self._u_deck[choice][1][0] == 'faint':
                    print('That Pokemon is fainted, pick another pokemon.\n')
                    time.sleep(1.5)
                else:
                    print()
                    return choice
            else:
                print('That Pokemon is not in your deck, pick a pokemon in your deck.\n')
                time.sleep(1.5)

    def check_per(self,percent):
        num = random.randint(1,101)
        print(percent, 'percent')
        print(num)
        if num <= int(percent):
            return 'YES'
        else:
            return 'NO'

    def skip_move(self,move,user,gym,L):
        if L == 'U':
            if self._gym_deck[gym][3] == None:
                num = random.randint(1,3)
                self._gym_deck[gym][3] = [num]
                damage = 'YES'
            else:
                print(' and it had no effect on {}.\n'.format(gym))
                damage = 0
        else:
            if self._u_deck[user][3] == None:
                num = random.randint(1,3)
                self._u_deck[user][3] = [num]
                damage = 'YES'
            else:
                print(' and it had no effect on {}.\n'.format(user))
                damage = 0
        return damage

    def modifier_move(self,move,user,gym,L):
        if L == 'U':
            if self._gym_deck[gym][3] == None:
                if move[2][1] == 'N':
                    self._gym_deck[gym][3] = int((self._poke_hp[gym] * 0.125) * -1)
                elif move[2][1] == 'S':
                    self._gym_deck[gym][3] = int((self._poke_hp[gym] * 0.125) * -1)
                    self._u_deck[user][3] = int((self._poke_hp[user] * 0.125))
                elif move[2][1] == 'A':
                    self._gym_deck[gym][3] = int((self._poke_hp[gym] * 0.125) * -1)
            else:
                print(' and it missed.\n')
        else:
            if self._u_deck[user][3] == None:
                if move[2][1] == 'N':
                    self._u_deck[user][3] = int((self._poke_hp[user] * 0.125) * -1)
                elif move[2][1] == 'S':
                    self._u_deck[user][3] = int((self._poke_hp[user] * 0.125) * -1)
                    self._gym_deck[gym][3] = int((self._poke_hp[gym] * 0.125))
                elif move[2][1] == 'A':
                    self._u_deck[user][3] = int((self._poke_hp[user] * 0.125) * -1)
            else:
                print(' and it missed.\n')
        return 0

    def attack_move(self,move,user,gym,L,level):
        modifier = 1
        if L == 'U':
            for d in self._gym_deck[gym][0]:
                if d in EFFECTIVE_DICT[move[1]]:
                    modifier *= 2
                if d in NOT_EFFECTIVE_DICT[move[1]]:
                    modifier *= 0.5
            if move[4] == 'SPE':
                attack = self._u_deck[user][1][3] * (MODIFIER[self._u_cond[3]])
                defense = self._gym_deck[gym][1][4] * (MODIFIER[self._gym_cond[4]])
            else:
                attack = self._u_deck[user][1][1] * (MODIFIER[self._u_cond[1]])
                defense = self._gym_deck[gym][1][2] * (MODIFIER[self._gym_cond[2]])
            damage = int(((((((2*level/5) + 2) * int(move[2][0:]) * (attack/defense))/50)+2) * modifier))
            self._gym_deck[gym][1][0] -= damage
        else:
            for d in self._u_deck[user][0]:
                if d in EFFECTIVE_DICT[move[1]]:
                    modifier *= 2
                if d in NOT_EFFECTIVE_DICT[move[1]]:
                    modifier *= 0.5
            if move[4] == 'SPE':
                attack = self._gym_deck[gym][1][3] * (MODIFIER[self._gym_cond[3]])
                defense = self._u_deck[user][1][4] * (MODIFIER[self._u_cond[4]])
            else:
                attack = self._gym_deck[gym][1][1] * (MODIFIER[self._gym_cond[1]])
                defense = self._u_deck[user][1][2] * (MODIFIER[self._u_cond[2]])
            damage = int(((((((2*level/5) + 2) * int(move[2][0:]) * (attack/defense))/50)+2) * modifier))
            self._u_deck[user][1][0] -= damage
        print(' it did {} damage.\n'.format(damage))
        return damage

    def lower_move(self,pokemon,move,L):
        index = STATS_LIST.index(move[2][1:4])
        amount = int(move[2][-1])
        if L == 'U':
            if self._gym_cond[index] != 0 and self._gym_cond[index] != 12:
                self._gym_cond[index] += amount
        else:
            if self._u_cond[index] != 0 and self._u_cond[index] != 12:
                self._u_cond[index] += amount
        print(' and it decreased {}\'s {} by {} stages.\n'.format(pokemon,STATS_PRINT[index],amount))
        damage = 0
        return damage

    def increase_move(self,pokemon,move,L):
        index = STATS_LIST.index(move[2][1:4])
        amount = int(move[2][-1])
        if L == 'U':
            if self._u_cond[index] != 0 and self._u_cond[index] != 12:
                self._u_cond[index] -= amount
        else:
            if self._gym_cond[index] != 0 and self._gym_cond[index] != 12:
                self._gym_cond[index] -= amount
        print(' and increased its {} by {} stages.\n'.format(STATS_PRINT[index],amount))
        damage = 0
        return damage

    def __str__():
        return 'Gym 1'

main()