import json
from pathlib import Path
from .models import GameState


def save_game(state: GameState, path: str = "saves/world.json") -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(state.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


def load_game(path: str = "saves/world.json") -> GameState | None:
    target = Path(path)
    if not target.exists():
        return None
    return GameState.from_dict(json.loads(target.read_text(encoding="utf-8")))
