from __future__ import annotations
import random
import skills
from skills import Skill
import effects


class Pokemon:
    name: str
    type: str

    def __init__(self, hp: int, attack: int, defense: int, evasion: int) -> None:
        # 初始化 Pokemon 的属性
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.evasion = evasion
        self.skills = self.initialize_skills()
        self.damage_taken_multiplier = 1.0
        self.damage_dealt_multiplier = 1.0
        self.moveable = True
        self.alive = True
        self.bonusTurn = False
        self.statuses = []

    def initialize_skills(self):
        # 抽象方法，子类应实现具体技能初始化
        raise NotImplementedError

    def use_skill(self, skill: Skill, opponent: Pokemon):
        # 使用技能
        print(f"{self.name} uses {skill.name}")
        skill.execute(self, opponent)

    def heal_self(self, amount):
        # 为自身恢复生命值
        if not isinstance(amount, int):
            amount = int(amount)

        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(f"{self.name} heals {amount} HP! Current HP: {self.hp}/{self.max_hp}")

    def check_evasion(self, evasionRateModifier = 0):
        # 判定是否闪避成功
        if self.evasion + evasionRateModifier >= random.randint(1,100):
            print(f"{self.name} evaded the attack!")
            return True
        else:
            return False

    def receive_damage(self, damage, attacker: Pokemon):
        # 计算伤害并减去防御力，更新 HP
        if not isinstance(damage, int):
            damage = int(damage)

        damage *= attacker.type_effectiveness(self)
        damage *= attacker.damage_dealt_multiplier
        damage *= self.damage_taken_multiplier
        damage -= self.defense
        if not isinstance(damage, int):
            damage = int(damage)
        if damage <= 0:
            print(f"{self.name}'s defense absorbed the attack!")
            return

        self.hp -= damage
        print(
            f"{self.name} received {damage} damage! Remaining HP: {self.hp}/{self.max_hp}"
        )
        if self.hp <= 0:
            self.alive = False
            print(f"{self.name} has fainted!")

    def receive_effect_damage(self, damage):
        # 受到状态效果的伤害
        if not isinstance(damage, int):
            damage = int(damage)

        self.hp -= damage
        print(
            f"{self.name} received {damage} effect damage! Remaining HP: {self.hp}/{self.max_hp}"
        )
        if self.hp <= 0:
            self.alive = False
            print(f"{self.name} has fainted!")

    def add_status_effect(self, effect: Effect):
        # 添加状态效果
        if not any(type(effect) == type(existing_effect) for existing_effect in self.statuses):
            self.statuses.append(effect)
        else:
            old_effect = next(existing_effect for existing_effect in self.statuses if type(existing_effect) == type(effect))
            if old_effect.stack_limit < 0:
                old_effect.duration = effect.duration
            elif old_effect.stack_limit > 0:
                old_effect.stacks = min(old_effect.stacks + 1, old_effect.stack_limit)

    def apply_status_effect(self):
        # 应用所有当前的状态效果，并移除持续时间结束的效果
        for status in self.statuses[:]:  # 使用切片防止列表在遍历时被修改
            status.apply(self)
            status.decrease_duration()
            if status.duration == 0:
                print(f"{self.name}'s {status.name} effect has worn off.")
                self.statuses.remove(status)

    def type_effectiveness(self, opponent: Pokemon):
        # 计算属性克制的抽象方法，具体实现由子类提供
        raise NotImplementedError

    def begin(self):
        # 新回合开始时触发的方法
        self.damage_taken_multiplier = 1.0
        self.damage_dealt_multiplier = 1.0
        self.moveable = True
        self.apply_status_effect()

    def __str__(self) -> str:
        return f"{self.name} type: {self.type}"


# GlassPokemon 类
class GlassPokemon(Pokemon):
    type = "Glass"

    def type_effectiveness(self, opponent: Pokemon):
        # 针对敌方 Pokemon 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "Water":
            effectiveness = 2.0
        elif opponent_type == "Fire":
            effectiveness = 0.5
        return effectiveness

    def begin(self):
        super().begin()
        # 每个回合开始时执行玻璃属性特性
        self.glass_attribute()

    def glass_attribute(self):
        # 玻璃属性特性：每回合恢复最大 HP 的 10%
        amount = self.max_hp * 0.1
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        print(
            f"{self.name} heals {amount} HP at the start of the turn! Current HP: {self.hp}/{self.max_hp}"
        )


# Bulbasaur 类，继承自 GlassPokemon
class Bulbasaur(GlassPokemon):
    name = "Bulbasaur"

    def __init__(self, hp=100, attack=50, defense=10, evasion=10) -> None:
        # 初始化 Bulbasaur 的属性
        super().__init__(hp, attack, defense, evasion)

    def initialize_skills(self):
        # 初始化技能，具体技能是 SeedBomb 和 ParasiticSeeds
        return [skills.SeedBomb(), skills.ParasiticSeeds(amount=10)]


class ElectricPokemon(Pokemon):
    type = "Electric"

    def type_effectiveness(self, opponent: Pokemon):
        # 针对敌方 Pokemon 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "Water":
            effectiveness = 2.0
        elif opponent_type == "Glass":
            effectiveness = 0.5
        return effectiveness

    def check_evasion(self, evasionRateModifier = 0):
        # 电系被动
        if self.evasion + evasionRateModifier >= random.randint(1,100):
            print(f"{self.name} evaded the attack!")
            self.bonusTurn = True
            return True
        else:
            return False


class PikaChu(ElectricPokemon):
    name = "PikaChu"

    def __init__(self, hp=80, attack=35, defense=5, evasion=30) -> None:
        # 初始化属性
        super().__init__(hp, attack, defense, evasion)

    def initialize_skills(self):
        # 初始化技能
        return [skills.Thunderbolt(), skills.QuickAttack(activation_chance=10)]


class Zapdos(ElectricPokemon):
    name = "Zapdos"

    def __init__(self, hp=80, attack=25, defense=0, evasion=40) -> None:
        # 初始化属性
        super().__init__(hp, attack, defense, evasion)

    def initialize_skills(self):
        # 初始化技能
        return [skills.Lightning_Maneuver(), skills.Counter_Attack()]


class WaterPokemon(Pokemon):
    type = "Water"

    def type_effectiveness(self, opponent: Pokemon):
        # 针对敌方 Pokemon 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "Fire":
            effectiveness = 2.0
        elif opponent_type == "Electric":
            effectiveness = 0.5
        return effectiveness

    def receive_damage(self, damage, attacker):
        # 水系被动：受到伤害时，50% 概率减少 30% 的伤害
        if random.random() < 0.5:
            damage *= 0.70
        return super().receive_damage(damage, attacker)


class Squirtle(WaterPokemon):
    name = "Squirtle"

    def __init__(self, hp=80, attack=25, defense=20, evasion=20) -> None:
        # 初始化属性
        super().__init__(hp, attack, defense, evasion)

    def initialize_skills(self):
        # 初始化技能
        return [skills.Aqua_Jet(), skills.Shield()]


class FirePokemon(Pokemon):
    type = "Fire"

    def type_effectiveness(self, opponent: Pokemon):
        # 针对敌方 Pokemon 的类型，调整效果倍率
        effectiveness = 1.0
        opponent_type = opponent.type

        if opponent_type == "Glass":
            effectiveness = 2.0
        elif opponent_type == "Water":
            effectiveness = 0.5
        return effectiveness

    def use_skill(self, skill: Skill, opponent: Pokemon):
        # 火系被动：每次攻击，叠加 10% 攻击力，最多 4 层
        if not any(isinstance(effect, effects.AttackstrengthEffect) for effect in self.statuses):
            self.add_status_effect(effects.AttackstrengthEffect(amount=10, stack_limit=4))
        super().use_skill(skill, opponent)


class Charmander(FirePokemon):
    name = "Charmander"

    def __init__(self, hp=80, attack=35, defense=15, evasion=10) -> None:
        # 初始化属性
        super().__init__(hp, attack, defense, evasion)

    def initialize_skills(self):
        # 初始化技能
        return [skills.Ember(amount=10), skills.Flame_Charge(amount=80)]