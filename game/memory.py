from .models import GameState

MAX_RECENT = 12

def remember(state: GameState, text: str) -> None:
    state.world.history.append(text)
    if len(state.world.history) > MAX_RECENT:
        state.world.history = state.world.history[-MAX_RECENT:]

def context(state: GameState) -> dict:
    characters = {}
    for key, npc in state.world.characters.items():
        characters[key] = {
            "name": npc.name,
            "race": npc.race,
            "personality": npc.personality,
            "goals": npc.goals,
            "memories": npc.memories[-8:],
            "relationships": npc.relationships,
            "alive": npc.alive,
        }
    return {
        "player": state.player.__dict__,
        "world": {
            "location": state.world.location,
            "day": state.world.day,
            "hour": state.world.hour,
            "weather": state.world.weather,
            "flags": state.world.flags,
            "quests": state.world.quests,
            "characters": characters,
            "recent_history": state.world.history[-MAX_RECENT:],
        },
    }
