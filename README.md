# Gioco GPT — Anime Isekai Interattivo

Un RPG narrativo interattivo in cui il giocatore controlla direttamente il protagonista tramite testo libero. Il narratore gestisce mondo, NPC, combattimenti, conseguenze e memoria persistente.

## Obiettivi
- Azioni del protagonista esclusivamente decise dal giocatore.
- Input libero: niente menu obbligatorio di scelte.
- NPC con personalità, obiettivi, memoria e relazioni.
- Conseguenze persistenti e mondo indipendente dal protagonista.
- Combattimenti con rischio reale, fallimenti e morte possibile.
- Inventario, statistiche, abilità, quest e tempo.
- Salvataggio dello stato narrativo.
- Backend predisposto per un LLM locale tramite Ollama.

## Avvio rapido

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Su Linux/macOS:

```bash
source .venv/bin/activate
python main.py
```

## Configurazione LLM
Copia `.env.example` in `.env` e imposta il modello Ollama desiderato. Se Ollama non è disponibile, il gioco usa il narratore deterministico integrato.
