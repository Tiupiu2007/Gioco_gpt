from .models import GameState
from .save import save_game
from .memory import context

INTRO = '''La pioggia batte contro la strada deserta. Torni a casa dopo una giornata apparentemente normale.
Un istante dopo, una luce bianca inghiotte ogni cosa.

Quando riapri gli occhi, sei disteso sull'erba umida. Sopra di te non c'è il cielo che conosci.
Due lune illuminano una foresta sconosciuta. In lontananza senti il suono di una campana... e un urlo.

Non hai idea di dove ti trovi. Non hai ricevuto una spiegazione. Non sai se qualcuno ti sta cercando.

Davanti a te il sentiero si divide: a sinistra conduce verso le luci di un villaggio; a destra scompare nella foresta.

**Cosa fai?**'''

class GameEngine:
    def __init__(self, state: GameState, narrator=None, save_path="saves/world.json"):
        self.state = state
        self.narrator = narrator
        self.save_path = save_path

    def start(self):
        if not self.state.world.history:
            self.state.world.history.append(INTRO)
        return self.state.world.history[-1]

    def apply_time(self, hours=1):
        self.state.world.hour += hours
        while self.state.world.hour >= 24:
            self.state.world.hour -= 24
            self.state.world.day += 1

    def act(self, action: str) -> str:
        action = action.strip()
        if not action:
            return "Devi prima decidere cosa fare."
        self.apply_time(1)
        if self.narrator and self.narrator.available():
            if hasattr(self.narrator, "narrate_game_state"):
                text = self.narrator.narrate_game_state(self.state, action)
            else:
                text = self.narrator.narrate(context(self.state), action)
        else:
            text = self._fallback(action)
        self.state.world.history.append(f"AZIONE: {action}\n{text}")
        save_game(self.state, self.save_path)
        return text

    def _fallback(self, action: str) -> str:
        return (f"Dopo la tua azione — {action} — il mondo reagisce senza aspettare. "
                "Il vento cambia direzione e dalla foresta arriva un rumore di rami spezzati. "
                "Qualcosa potrebbe averti notato.\n\n**Cosa fai?**")
