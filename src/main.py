from handState import HandState
from dealCards import deal_hole_cards, deal_community_cards
from aiAgent import AIAgent
from utils import print_hand_state, print_game_settings, print_players
from gameState import GameState
import json


def run():
    starting_stack = 200
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
    AI_hand = deal_hole_cards()

    position = game.players['AI'].get('position')       # gets your position
    stack = game.players['AI'].get('stack')            # gets your stack

    print(f"Dealt hand: {AI_hand[0]} in position {position} with stack {stack}")

    # create a new hand
    hand_state = HandState(AI_hand, game.players, starting_stack, starting_stack)


    for street in ["preflop", "flop", "turn", "river"]:
        hand_state.street = street
        if street == "flop":
            hand_state.next_street(deal_community_cards(3))  # random flop
        elif street == "turn":
            hand_state.next_street(deal_community_cards(1))
        elif street == "river":
            hand_state.next_street(deal_community_cards(1))

        print(f"\n==== {street.upper()} ====")
        print_hand_state(hand_state)

        betting_active = True
        while betting_active:
            player_order = game.action_order(hand_state.street)

            for player in player_order:
                print_hand_state(hand_state)

                if player == 'Chad':
                    action_input = input("Your action (call/fold/raise/check): ")
                    amount_input = input("Enter amount to raise (0 for check/fold): ")
                if player == 'AI':
                    agent_decision = agent.make_decision(hand_state, game, legal_actions=['fold', 'call', 'raise'])
                    agent_decision = json.loads(agent_decision) # Parse JSON string to dict
                    action_input = agent_decision.get('action')
                    amount_input = agent_decision.get('raise_size')

                    print(f"AI Decision: {agent_decision}")

                hand_state.add_action(player, action_input, amount_input)







if __name__ == "__main__":
    run()