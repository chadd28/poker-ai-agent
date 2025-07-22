from handState import HandState
from dealCards import deal_hole_cards, deal_community_cards
from aiAgent import AIAgent
from utils import calculate_call_amount, print_hand_state, print_game_settings, print_players, validate_action, get_legal_actions
from gameState import GameState
import json

def human_decision(hand_state, player):
    legal_actions = get_legal_actions(player, hand_state)
    print(f"Legal actions for {player}: {', '.join(legal_actions)}")

    action_input = input("Your action: ").strip().lower()

    # Parse into standardized form
    if action_input.startswith("call"):
        action = "call"
        call_amount = calculate_call_amount(hand_state, player)
        total_amount = call_amount + hand_state.street_contributions.get(player, 0)
    elif action_input.startswith("check"):
        action = "check"
        total_amount = hand_state.street_contributions.get(player, 0)
    elif action_input.startswith("raise"):
        raise_to = int(input("Enter raise to amount (total): "))
        action = "raise"
        total_amount = raise_to
    elif action_input.startswith("all in"):
        action = "all in"
        total_amount = hand_state.players[player]['stack']
    else:
        action = "fold"
        total_amount = 0

    return action, total_amount

def ai_decision(player, hand_state, game_state, agent):
    legal_actions = get_legal_actions("AI", hand_state)
    agent_decision = json.loads(agent.make_decision(hand_state, game_state, legal_actions))
    action_input = agent_decision.get('action')
    declared_raise = agent_decision.get('raise_size', 0)

    print(f"AI Decision: {agent_decision}")

    print(f"AI Action: {action_input}, Raise Size: {declared_raise}")

    # Validate AI action
    if action_input.startswith("call"):
        action_input = "call"
        call_amount = calculate_call_amount(hand_state, player)
        total_amount = call_amount + hand_state.street_contributions.get(player, 0)

    elif action_input.startswith("check"):
        action_input = "check"
        total_amount = 0

    elif action_input.startswith("raise"):
        if validate_action("raise", declared_raise, player, hand_state):
            action_input = "raise"
            total_amount = declared_raise
        else:
            print("AI tried illegal raise. Forcing call instead.")
            action_input = "call"
            call_amount = calculate_call_amount(hand_state, player)
            total_amount = call_amount + hand_state.street_contributions.get(player, 0)
    elif action_input.startswith("all in"):
        action_input = "all in"
        total_amount = hand_state.players[player]['stack']
    elif action_input == "fold":
        total_amount = 0
    
    return action_input, total_amount
    

def run():
    # gemeni: gemini-1.5-flash
    # groq: llama-3.1-8b-instant
    agent = AIAgent(provider='groq', model_name='llama-3.1-8b-instant')
    game = GameState(sb=1, bb=2, starting_stack=200)

    game.add_player('AI', 'sb')
    game.add_player('Chad', 'bb')
    # game.add_player('John', 'button')
    
    print("==== Initialized New Game ====")
    print_game_settings(game)

    print("\n==== Hand #1 ====")
    # ['Ah', 'Kd'] is a sample hand
    AI_hand = ['9h', '9d']

    position = game.players['AI'].get('position')       # gets your position
    stack = game.players['AI'].get('stack')            # gets your stack

    print(f"Dealt hand: {AI_hand} in position {position} with stack {stack}")

    # create a new hand
    hand_state = HandState(AI_hand, game.players, sb=1, bb=2)


    betting_active = True
    while betting_active:
            player_order = game.action_order(hand_state.street)

            while not hand_state.betting_round_complete():
                for player in player_order:
                    if hand_state.betting_round_complete():
                        break  # Exit early if round is already complete

                    if player == 'Chad':  # HUMAN INPUT
                        action, total_amount = human_decision(hand_state, player)
                        if not validate_action(action, total_amount, player, hand_state):
                            print("Illegal action. Forcing fold instead.")
                            action, total_amount = "fold", 0
                        hand_state.add_action(player, action, total_amount)

                    elif player == 'AI':  # AI DECISION
                        action, total_amount = ai_decision(player, hand_state, game, agent)
                        hand_state.add_action(player, action, total_amount)
                    
                    print_hand_state(hand_state)
            
            # ✅ Betting round finished
            print(f"\n==== {hand_state.street.capitalize()} betting complete ====")

            # ✅ Check if only one player left → End hand
            active_players = hand_state.active_players
            if len(active_players) <= 1 or hand_state.street == "river":
                betting_active = False
                break

            # ✅ Move to next street
            if hand_state.street == 'preflop':
                hand_state.next_street(deal_community_cards(3))
                print("=== DEALING FLOP ===")
                print_hand_state(hand_state)
            elif hand_state.street == 'flop':
                hand_state.next_street(deal_community_cards(1))
                print("=== DEALING TURN ===")
                print_hand_state(hand_state)
            elif hand_state.street == 'turn':
                hand_state.next_street(deal_community_cards(1))
                print("=== DEALING RIVER ===")
                print_hand_state(hand_state)

    print("\n==== Hand Complete ====")







if __name__ == "__main__":
    run()