from dotenv import load_dotenv
from game import GameEngine, GameState, OllamaNarrator
from game.save import load_game


def main():
    load_dotenv()
    state = load_game() or GameState()
    engine = GameEngine(state, OllamaNarrator())
    print("=" * 64)
    print("                 GIOCO GPT — ISEKAI")
    print("=" * 64)
    print(engine.start())
    while True:
        try:
            action = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if action.lower() in {"/esci", "/quit", "/exit"}:
            break
        if action.lower() == "/stato":
            print(state.to_dict()); continue
        print("\n" + engine.act(action))

if __name__ == "__main__":
    main()
