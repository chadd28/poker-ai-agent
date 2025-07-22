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

def calculate_call_amount(hand_state, player):
    """
    Computes how much more a player needs to call to match the current highest bet.
    """
    # Gather all player contributions from hand_state.players
    max_bet = max(hand_state.street_contributions.values())
    player_bet = hand_state.street_contributions[player]
    return max(0, max_bet - player_bet)

def validate_action(action, amount, player, hand_state):
    """
    Validates if the chosen action is legal. Prints error and returns False if not.
    """
    stack = hand_state.players[player]['stack']
    call_amount = calculate_call_amount(hand_state, player)
    street_contribution = hand_state.street_contributions[player]
    min_raise = max((call_amount+street_contribution) * 2, hand_state.bb * 2)     # simplified rule for min raise

    if action == "fold" or action == "all in":
        return True

    elif action == "check":
        if call_amount != 0:
            print(f"Illegal check: Player owes {call_amount} to call.")
            return False
        return True

    elif action == "call":
        if call_amount > stack:
            print(f"Illegal call: Player stack ({stack}) < call amount ({call_amount}).")
            return False
        return True

    elif action == "raise":
        if amount < min_raise:
            print(f"Illegal raise: Minimum raise is to {min_raise}, tried {amount}.")
            return False
        if amount > stack:
            print(f"Illegal raise: Raise amount exceeds stack.")
            return False
        return True

    else:
        print(f"Unknown action {action}")
        return False
    
def get_legal_actions(player, hand_state):
    call_amount = calculate_call_amount(hand_state, player)
    stack = hand_state.players[player]['stack']
    street_contribution = hand_state.street_contributions[player]
    min_raise = max((call_amount+street_contribution) * 2, hand_state.bb * 2) 

    actions = ["fold", f"all in for ${stack}"]

    if call_amount == 0:
        actions.append("check")
    else:
        actions.append(f"call for ${call_amount} more")

    # Only allow raise if player has more than min_raise amount
    if stack >= min_raise:
        max_raise = stack
        actions.append(f"raise to a value between min: ${min_raise} and max: ${max_raise}")
    
    return actions
