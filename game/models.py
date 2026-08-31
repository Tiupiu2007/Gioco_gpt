from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class Character:
    id: str
    name: str
    age: int | None = None
    race: str = "Umano"
    personality: str = ""
    goals: list[str] = field(default_factory=list)
    memories: list[str] = field(default_factory=list)
    relationships: dict[str, int] = field(default_factory=dict)
    alive: bool = True

@dataclass
class Player:
    name: str = "Sconosciuto"
    hp: int = 100
    max_hp: int = 100
    level: int = 1
    experience: int = 0
    attributes: dict[str, int] = field(default_factory=lambda: {
        "forza": 10, "agilita": 10, "vitalita": 10, "intelligenza": 10, "volonta": 10, "fortuna": 5
    })
    abilities: list[str] = field(default_factory=list)
    inventory: list[str] = field(default_factory=list)
    equipment: dict[str, str | None] = field(default_factory=lambda: {"arma": None, "armatura": None, "accessorio": None})

@dataclass
class WorldState:
    location: str = "Villaggio di Elaria"
    day: int = 1
    hour: int = 8
    weather: str = "sereno"
    flags: dict[str, Any] = field(default_factory=dict)
    quests: dict[str, dict[str, Any]] = field(default_factory=dict)
    characters: dict[str, Character] = field(default_factory=dict)
    history: list[str] = field(default_factory=list)

@dataclass
class GameState:
    player: Player = field(default_factory=Player)
    world: WorldState = field(default_factory=WorldState)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameState":
        p = Player(**data.get("player", {}))
        world_data = data.get("world", {})
        chars = {k: Character(**v) for k, v in world_data.get("characters", {}).items()}
        world_data["characters"] = chars
        return cls(player=p, world=WorldState(**world_data))
