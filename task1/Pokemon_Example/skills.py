import random
from typing import TYPE_CHECKING
import effects

if TYPE_CHECKING:
    from pokemon import Pokemon


class Skill:
    name: str

    def __init__(self) -> None:
        pass

    def execute(self, user: "Pokemon", opponent: "Pokemon"):
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.name}"


class SeedBomb(Skill):
    name = "Seed Bomb"

    def __init__(self, activation_chance: int = 15) -> None:
        super().__init__()
        self.activation_chance = activation_chance  # 确保激活几率被正确初始化

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> None:
        # 造成伤害
        if opponent.check_evasion():
            return

        self.damage = user.attack
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )
        opponent.receive_damage(self.damage, user)

        # 判断是否触发状态效果
        if random.randint(1, 100) <= self.activation_chance:
            opponent.add_status_effect(effects.PoisonEffect())
            print(f"{opponent.name} is poisoned by {self.name}!")
        else:
            print(f"{self.name} did not poison {opponent.name} this time.")


class ParasiticSeeds(Skill):
    name = "Parasitic Seeds"

    def __init__(self, amount: int) -> None:
        super().__init__()
        self.amount = amount

    def execute(self, user: "Pokemon", opponent: "Pokemon") -> None:
        # 给使用者添加治疗效果
        user.add_status_effect(effects.HealEffect(self.amount))
        print(f"{user.name} heals {self.amount} HP with {self.name}")

        # 给对手添加中毒效果
        opponent.add_status_effect(effects.PoisonEffect())
        print(f"{opponent.name} is poisoned by {self.name}!")


class Thunderbolt(Skill):
    name = "Thunderbolt"

    def __init__(self, activation_chance: int = 10) -> None:
        self.activation_chance = activation_chance

    def execute(self, user, opponent):
        if opponent.check_evasion():
            return

        self.damage = user.attack * 1.4
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )
        opponent.receive_damage(self.damage, user)

        if random.randint(1, 100) <= self.activation_chance:
            opponent.add_status_effect(effects.ParalysisEffect())
            print(f"{opponent.name} is paralyzed by {self.name}!")
        else:
            print(f"{self.name} did not paralyze {opponent.name} this time.")


class QuickAttack(Skill):
    name = "Quick Attack"

    def __init__(self, activation_chance: int) -> None:
        self.activation_chance = activation_chance

    def execute(self, user, opponent):
        if opponent.check_evasion():
            return

        self.damage = user.attack
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )
        opponent.receive_damage(self.damage, user)
        if random.randint(1, 100) <= self.activation_chance:
            print(f"{self.name} catch a chance to attack again!")
            if opponent.check_evasion():
                return
            print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
            )
            opponent.receive_damage(self.damage, user)


class Aqua_Jet(Skill):
    name = "Aqua Jet"

    def execute(self, user, opponent):
        if opponent.check_evasion():
            return

        self.damage = user.attack * 1.4
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )
        opponent.receive_damage(self.damage, user)


class Shield(Skill):
    name = "Shield"

    def __init__(self) -> None:
        super().__init__()

    def execute(self, user, opponent):
        # 使用者获得护盾效果
        user.add_status_effect(effects.ShieldEffect())
        print(f"{user.name} used {self.name} and gained a shield!")


class Ember(Skill):
    name = "Ember"

    def __init__(self, amount: int = 10) -> None:
        self.activation_chance = amount

    def execute(self, user, opponent):
        if opponent.check_evasion():
            return

        self.damage = user.attack
        print(
            f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
        )
        opponent.receive_damage(self.damage, user)
        if random.randint(1, 100) <= self.activation_chance:
            opponent.add_status_effect(effects.BurnEffect())
            print(f"{opponent.name} is burned by {self.name}!")
        else:
            print(f"{self.name} did not burn {opponent.name} this time.")


class Flame_Charge(Skill):
    name = "Flame Charge"

    def __init__(self, amount: int) -> None:
        self.amount = amount
        self.ChargePower = False

    def execute(self, user, opponent):
        if self.ChargePower:
            if opponent.check_evasion(20):  # 提供额外的闪避率修正
                return
            self.damage = user.attack * 3
            print(
                f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
            )
            opponent.receive_damage(self.damage, user)
            if random.randint(1, 100) <= self.amount:
                opponent.add_status_effect(effects.BurnEffect())
                print(f"{opponent.name} is burned by {self.name}!")
            else:
                print(f"{self.name} did not burn {opponent.name} this time.")
        else:
            self.ChargePower = True
            print(f"{user.name} used {self.name} and is charging up for a powerful attack!")


class Lightning_Maneuver(Skill):
    name = "Lightning Maneuver"

    def __init__(self, amount: int = 2) -> None:
        self.amount = amount

    def execute(self, user, opponent):
        user.evasion *= self.amount
        print(f"{user.name} used {self.name} and increased its evasion by {self.amount} times!")


class Counter_Attack(Skill):
    name = "Counter Attack"

    def __init__(self) -> None:
        super().__init__()

    def execute(self, user, opponent):
        if opponent.check_evasion():
            return

        if user.bonusTurn:
            self.damage = user.attack * 3
            print(
                f"Great chance! {user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
            )
            opponent.receive_damage(self.damage, user)
        else:
            self.damage = user.attack *0.8
            print(
                f"{user.name} used {self.name}, dealing {self.damage} damage to {opponent.name}"
            )
            opponent.receive_damage(self.damage, user)