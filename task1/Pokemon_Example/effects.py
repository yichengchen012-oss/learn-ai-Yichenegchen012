from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pokemon import Pokemon


class Effect:
    name: str

    def __init__(self, duration: int) -> None:
        # 初始化效果持续时间
        self.duration = duration
        self.stack_limit = -1  # 默认不可叠加
        self.stacks = 0  # 当前叠加层数

    def apply(self, pokemon: "Pokemon") -> None:
        # 应用效果的抽象方法，子类需要实现
        raise NotImplementedError

    def decrease_duration(self) -> None:
        # 减少效果持续时间
        if self.duration > 0:
            self.duration -= 1
            print(f"{self.name} effect duration decreased. Remaining: {self.duration}")


class PoisonEffect(Effect):
    name = "Poison"

    def __init__(self, damage: int = 10, duration: int = 3) -> None:
        super().__init__(duration)
        self.damage = damage

    def apply(self, pokemon: "Pokemon") -> None:
        self.damage = int(self.damage / 100 * pokemon.max_hp)
        pokemon.receive_effect_damage(self.damage)
        print(f"{pokemon.name} takes {self.damage} poison damage!")


class HealEffect(Effect):
    name = "Heal"

    def __init__(self, amount: int, duration: int = 3) -> None:
        super().__init__(duration)
        self.amount = amount

    def apply(self, pokemon: "Pokemon") -> None:
        pokemon.heal_self(self.amount)
        print(f"{pokemon.name} heals {self.amount} HP!")


class ParalysisEffect(Effect):
    name = "Paralysis"

    def __init__(self, duration: int = 1) -> None:
        super().__init__(duration)

    def apply(self, pokemon: "Pokemon") -> None:
        pokemon.moveable = False
        print(f"{pokemon.name} is paralyzed and cannot move this turn!")


class ShieldEffect(Effect):
    name = "Shield"

    def __init__(self, duration: int = 1) -> None:
        super().__init__(duration)

    def apply(self, pokemon: "Pokemon") -> None:
        # 提供一个护盾效果
        pokemon.damage_taken_multiplier = 0.5


class AttackstrengthEffect(Effect):
    name = "Attack Strength"

    def __init__(self, amount: int,  stack_limit: int, duration: int = -1) -> None:
        super().__init__(duration)
        self.amount = amount
        self.stack_limit = stack_limit

    def apply(self, pokemon: "Pokemon") -> None:
        # 增加攻击力
        if self.stacks < self.stack_limit:
            self.stacks += 1
        pokemon.damage_dealt_multiplier += self.amount / 100 * self.stacks
        print(f"{pokemon.name}'s attack strength increased by {self.amount * self.stacks}%!")


class BurnEffect(Effect):
    name = "Burn"

    def __init__(self, damage: int = 10, duration: int = 2) -> None:
        super().__init__(duration)
        self.damage = damage

    def apply(self, pokemon: "Pokemon") -> None:
        pokemon.receive_effect_damage(self.damage)