from enum import Enum
from dataclasses import dataclass
from abc import ABC
import json
import inquirer


class Race(Enum):
    HUMAN = 1
    ELF = 2
    DWARF = 3
    HOBBIT = 4
    ORC = 5


class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class Weapons(Enum):
    BOW = 1
    SWORD = 2
    STAFF = 3
    HAMMER = 4
    BLADES = 5


class Defense(Enum):
    SHIELD = 1
    NO_SHIELD = 2


class Armor(Enum):
    HELMET = 1
    GAUNTLETS = 2
    CHEST = 3
    LEG = 4


@dataclass
class Equipment:
    weapon: Weapons
    defense: Defense
    armor: list[Armor]


class Champion(ABC):
    def __init__(self, name: str, race: Race, gender: Gender):
        if not isinstance(name, str):
            raise TypeError('Name must be a string')
        if len(name) > 10:
            raise ValueError('Name can only be 10 characters long')
        if not isinstance(race, Race):
            raise TypeError('Race must be one of the valid races')
        if not isinstance(gender, Gender):
            raise TypeError('Gender must be one of the valid genders')

        self.name = name
        self.race = race
        self.gender = gender
        self.level = 0
        self.exp_needed = 100
        self.current_exp = 0
        self.total_exp = 0
        self.stat_points = 0
        self.class_type = ''

        self.stats = {
            'health': 0,
            'attack': 0,
            'defense': 0,
            'magic': 0,
            'speed': 0,
        }

    def level_up(self):
        if self.level <= 100:
            self.level += 1
        else:
            print('You are in the max level')
            return

        self.stat_points += 3
        self.total_exp += self.current_exp
        self.current_exp = 0
        self.exp_needed *= 1.2

    def increase_exp(self, exp: int):
        self.current_exp += exp
        if self.current_exp >= self.exp_needed:
            self.level_up()

    def death(self):
        self.current_exp *= 0.5

    def attack(self, attack_type: str, other_champion):
        if not isinstance(other_champion, Champion):
            raise TypeError('champion must be other Champion class')

        attack_points = self.stats[attack_type]

        while attack_points > 0:
            if other_champion.stats['defense'] > 0:
                other_champion.stats['defense'] -= 1

            if other_champion.stats['defense'] == 0 and other_champion.stats['health'] > 0:
                other_champion.stats['health'] -= 1

            attack_points -= 1

        if other_champion.stats['health'] == 0:
            other_champion.death()
            self.increase_exp(15)

    def save_character(self):
        data_champ = {
            'name': self.name,
            'race': self.race.name,
            'gender': self.gender.name,
            'stats': self.stats,
            'class_type': self.class_type
        }

        with open(f'{self.name}-data.json', 'w') as f:
            f.write(json.dumps(data_champ))

    @staticmethod
    def load_character(char_name: str):
        with open(f'{char_name}-data.json', 'r') as f:
            data_champ = json.loads(f.read())

        load_champ = Game.create_champ_class(
            data_champ['class_type'], data_champ['name'], data_champ['race'], data_champ['gender'])

        load_champ.stats = data_champ['stats']

        return load_champ

    def increase_stats(self, health=0, attack=0, defense=0, magic=0, speed=0):
        total_points = health + attack + defense + magic + speed

        if total_points > self.stat_points:
            print(f'You only have {self.stat_points} points to spend')
            return

        self.stats['health'] += health
        self.stats['attack'] += attack
        self.stats['defense'] += defense
        self.stats['magic'] += magic
        self.stats['speed'] += speed
        self.stat_points -= total_points


class Cleric(Champion):
    def __init__(self, name: str, race: Race, gender: Gender):
        super().__init__(name, race, gender)
        self.class_type = 'CLERIC'
        self.stats = {
            'health': 5,
            'attack': 2,
            'defense': 5,
            'magic': 5,
            'speed': 5
        }
        self.equipment = Equipment(Weapons.STAFF, Defense.SHIELD, [
                                   Armor.HELMET, Armor.GAUNTLETS])


class Fighter(Champion):
    def __init__(self, name: str, race: Race, gender: Gender):
        super().__init__(name, race, gender)
        self.class_type = 'FIGHTER'
        self.stats = {
            'health': 8,
            'attack': 4,
            'defense': 10,
            'magic': 3,
            'speed': 8
        }
        self.equipment = Equipment(Weapons.SWORD, Defense.SHIELD, [
                                   Armor.HELMET, Armor.CHEST])


class Mage(Champion):
    def __init__(self, name: str, race: Race, gender: Gender):
        super().__init__(name, race, gender)
        self.class_type = 'MAGE'
        self.stats = {
            'health': 5,
            'attack': 7,
            'defense': 5,
            'magic': 10,
            'speed': 5
        }
        self.equipment = Equipment(
            Weapons.STAFF, Defense.NO_SHIELD, [Armor.HELMET])


class Paladin(Champion):
    def __init__(self, name: str, race: Race, gender: Gender):
        super().__init__(name, race, gender)
        self.class_type = 'PALADIN'
        self.stats = {
            'health': 5,
            'attack': 6,
            'defense': 6,
            'magic': 7,
            'speed': 6
        }
        self.equipment = Equipment(
            Weapons.HAMMER, Defense.NO_SHIELD, [Armor.CHEST])


class Ranger(Champion):
    def __init__(self, name: str, race: Race, gender: Gender):
        super().__init__(name, race, gender)
        self.class_type = 'RANGE'
        self.stats = {
            'health': 7,
            'attack': 4,
            'defense': 5,
            'magic': 8,
            'speed': 3
        }
        self.equipment = Equipment(
            Weapons.BOW, Defense.NO_SHIELD, [Armor.HELMET])


class Rogue(Champion):
    def __init__(self, name: str, race: Race, gender: Gender):
        super().__init__(name, race, gender)
        self.class_type = 'ROGUE'
        self.stats = {
            'health': 6,
            'attack': 4,
            'defense': 5,
            'magic': 5,
            'speed': 10
        }
        self.equipment = Equipment(
            Weapons.BLADES, Defense.NO_SHIELD, [Armor.HELMET])


class Game:
    @staticmethod
    def create_champ_class(class_name: str, champ_name: str, race: str, gender: str) -> Champion:
        classes_map: dict[str, Champion] = {
            'CLERIC': Cleric,
            'FIGHTER': Fighter,
            'MAGE': Mage,
            'PALADIN': Paladin,
            'RANGER': Ranger,
            'ROGUE': Rogue
        }

        return classes_map[class_name](champ_name, Race._member_map_[race], Gender._member_map_[gender])

    def run(self):
        print('Bienvenido al juego de los campeones')
        load_char = inquirer.confirm('¿Quieres cargar un jugador?')

        if load_char:
            load_name = inquirer.text(
                'Introduce el nombre del Campeón que quieres cargar')

            champ = Champion.load_character(load_name)

            return champ

        questions = [
            inquirer.Text('name', message='Introduce el nombre de tu Campeón'),
            inquirer.List('race', message='Selecciona una raza para tu Campeón', choices=[
                          'HUMAN', 'ELF', 'DWARF', 'HOBBIT', 'ORC']),
            inquirer.List('gender', message='Selecciona el género de tu Campeón', choices=[
                          'MALE', 'FEMALE', 'OTHER']),
            inquirer.List('champ_class', message='Selecciona la clase de tu Campeón', choices=[
                          'CLERIC', 'FIGHTER', 'MAGE', 'PALADIN', 'RANGER', 'ROGUE'])
        ]

        answers = inquirer.prompt(questions)

        champ = self.create_champ_class(
            answers['champ_class'], answers['name'], answers['race'], answers['gender'])

        return champ
