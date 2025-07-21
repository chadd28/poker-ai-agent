def print_hand_state(hs):
    from pprint import pprint
    print("\n--- HAND STATE ---")
    filtered = {k: v for k, v in hs.__dict__.items() if k not in ('street', 'sb', 'bb')}
    pprint(filtered)

def print_game_settings(gs):
    from pprint import pprint
    print("\n--- GAME SETTINGS ---")
    pprint(gs.__dict__)

def print_players(gs):
    print("\n--- PLAYERS ---")
    for player, position in gs.positions.items():
        print(f"{player}: {position}")