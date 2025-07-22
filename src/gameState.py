from typing import List, Dict, Any

class GameState:
    """
    Tracks overall game state, settings, and completed hands.
    """
    def __init__(self, sb=1, bb=2, starting_stack=200):
        self.player_count = 0
        self.sb = sb
        self.bb = bb
        self.starting_stack = starting_stack
        self.hand_history = []  # Store completed HandState objects
        self.players = {}     # maps player to their position and stack
    
    def add_player(self, player_name, position):
        """Add a player with their position."""
        self.players[player_name] = {
            'position': position,
            'stack': self.starting_stack,
            'contribution': 0  
        }
        self.player_count += 1

    def add_hand(self, hand_state):
        """Add a completed HandState to history."""
        self.hand_history.append(hand_state)

    def last_hand(self):
        """Return the most recent completed hand, or None."""
        if self.hand_history:
            return self.hand_history[-1]
        return None

    def get_settings(self):
        """Return a copy of current game settings."""
        return self.settings.copy()
    
    def action_order(self, street):
        """
        Return the order of players based on their positions and the current street.
        Preflop: UTG -> MP -> CO -> BTN -> SB -> BB
        Postflop: SB -> BB -> UTG -> MP -> CO -> BTN
        """
        if street == 'preflop':
        # Preflop order: UTG first, then MP, CO, BTN, SB, BB
            position_order = ['utg', 'mp', 'co', 'button', 'sb', 'bb']
        else:
            # Postflop order: SB first, then BB, UTG, MP, CO, BTN
            position_order = ['sb', 'bb', 'utg', 'mp', 'co', 'button']

        # Sort players based on position order, then extract just the player names
        sorted_players = sorted(
            self.players.items(),
            key=lambda x: position_order.index(x[1]['position']) if x[1]['position'] in position_order else 999
        )

        return [player_name for player_name, _ in sorted_players]

    def action_order_detailed(self):
        """Return the order of players based on their positions."""
        position_order = ['sb', 'bb', 'utg', 'mp', 'co', 'button']

        # Sort players based on position order, then extract player names and their positions
        sorted_players = sorted(
        self.players.items(),
        key=lambda x: position_order.index(x[1]['position']) if x[1]['position'] in position_order else 999
        )

        return {i + 1: (player_name, info['position']) for i, (player_name, info) in enumerate(sorted_players)}
    
    def __repr__(self):
        return f"<GameState players={self.players} stakes={self.stakes} hands_played={len(self.hand_history)}>"
