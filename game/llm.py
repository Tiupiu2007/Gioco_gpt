import json
import os
import requests
from .memory import context

SYSTEM_PROMPT = '''Sei il narratore e direttore di un RPG anime isekai persistente.
Il giocatore controlla esclusivamente il protagonista. NON decidere mai al suo posto pensieri, emozioni, dialoghi o azioni.
Puoi descrivere solo ciò che il protagonista percepisce dall'esterno e le conseguenze dell'azione dichiarata.
Il giocatore può scrivere qualsiasi azione, anche non prevista. Valutala in base a fisica, abilità, informazioni disponibili e situazione.
Gli NPC sono individui autonomi: hanno personalità, memoria, obiettivi, paure, relazioni e possono agire fuori scena.
Il mondo continua a evolvere. Le conseguenze devono essere coerenti, anche quando sono negative.
Non regalare vittorie, informazioni, oggetti o poteri senza causa. Il protagonista può fallire, essere ferito o morire.
Mantieni continuità con lo stato. Non retconare eventi già avvenuti.
Stile: anime fantasy maturo, immersivo, dialoghi naturali, scene dinamiche. Italiano.
Alla fine della risposta lascia sempre la situazione aperta senza suggerire una lista obbligatoria di scelte.
'''

class OllamaNarrator:
    def __init__(self, url=None, model=None):
        self.url = (url or os.getenv("OLLAMA_URL", "http://localhost:11434")).rstrip("/")
        self.model = model or os.getenv("OLLAMA_MODEL", "qwen3:8b")

    def available(self) -> bool:
        try:
            return requests.get(f"{self.url}/api/tags", timeout=1.5).ok
        except requests.RequestException:
            return False

    def narrate(self, state: dict, player_action: str) -> str:
        prompt = "STATO PERSISTENTE:\n" + json.dumps(state, ensure_ascii=False, indent=2) + "\n\nAZIONE DEL GIOCATORE:\n" + player_action + "\n\nNarra esclusivamente la reazione del mondo e delle persone all'azione dichiarata."
        response = requests.post(
            f"{self.url}/api/chat",
            json={"model": self.model, "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ], "stream": False,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]

    def narrate_game_state(self, game_state, player_action: str) -> str:
        return self.narrate(context(game_state), player_action)
