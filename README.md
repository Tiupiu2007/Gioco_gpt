# Gioco GPT — Anime Isekai Interattivo

RPG narrativo in cui **il giocatore controlla il protagonista con testo libero**. L'AI interpreta il mondo, gli NPC e le conseguenze, ma non decide mai volontariamente cosa fa il protagonista.

## Cosa include
- GUI desktop PyQt6.
- Input libero: puoi descrivere qualsiasi azione.
- Narratore locale tramite Ollama.
- NPC autonomi con personalità, obiettivi, memoria e relazioni.
- Mondo persistente con luogo, tempo, meteo, quest e flag.
- Statistiche, HP, livello, abilità, inventario ed equipaggiamento.
- Salvataggio automatico in `saves/world.json`.
- Memoria recente limitata per evitare di gonfiare il prompt all'infinito.
- Possibilità di fallire, subire conseguenze e morire.
- Modalità CLI mantenuta in `cli.py`.

## Installazione Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ollama

Installa e avvia Ollama, poi scarica il modello indicato nel `.env`.

Copia `.env.example` in `.env` e modifica `OLLAMA_MODEL` se necessario.

## Avvio

```powershell
python main.py
```

Si apre la finestra del gioco. Scrivi direttamente cosa vuoi che faccia il protagonista e premi **Agisci**.

Per la modalità terminale:

```powershell
python cli.py
```

Se Ollama non è raggiungibile, il gioco continua usando il narratore di fallback invece di bloccarsi.
