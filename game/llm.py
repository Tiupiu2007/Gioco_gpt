import os
import requests

SYSTEM_PROMPT = '''Sei il narratore e direttore di un RPG anime isekai persistente.
Il giocatore controlla esclusivamente il protagonista. Non decidere mai volontariamente cosa pensa,
dice o fa il protagonista: presenta situazione, percezioni esterne e conseguenze.
Gli NPC hanno volontà propria, memoria, obiettivi, relazioni e possono mentire o agire senza il giocatore.
Il mondo evolve anche fuori scena. Le azioni hanno conseguenze coerenti e non devi proteggere il giocatore dal fallimento.
Non regalare poteri o vittorie senza motivo. Mantieni continuità con lo stato fornito.
Rispondi in italiano, con prosa immersiva ma senza dilungarti inutilmente.
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
        prompt = f'''STATO ATTUALE:\n{state}\n\nAZIONE DEL GIOCATORE:\n{player_action}\n\nContinua la scena. Non controllare il protagonista.'''
        response = requests.post(
            f"{self.url}/api/chat",
            json={"model": self.model, "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
