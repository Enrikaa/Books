from enum import Enum


class ChoicesEnum(Enum):
    """Enum for model char field choice constants."""

    @classmethod
    def get_choices(cls) -> list[tuple[str, str]]:
        choices = []
        for prop in cls:
            choices.append((prop.value, prop.name))
        return choices

    @classmethod
    def get_all_values(cls) -> list[str]:
        return [prop.value for prop in cls]

    def __str__(self):
        return self.value
