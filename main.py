from dotenv import load_dotenv
from game import GameEngine, GameState, OllamaNarrator
from game.save import load_game


def main():
    load_dotenv()
    state = load_game() or GameState()
    narrator = OllamaNarrator()
    engine = GameEngine(state, narrator)

    print("=" * 64)
    print("                 GI0CO GPT — ISEKAI")
    print("=" * 64)
    print(engine.start())

    while True:
        try:
            action = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSalvataggio...")
            break
        if action.lower() in {"/esci", "/quit", "/exit"}:
            print("Salvataggio completato.")
            break
        if action.lower() == "/stato":
            print(state.to_dict())
            continue
        print("\n" + engine.act(action))

if __name__ == "__main__":
    main()
