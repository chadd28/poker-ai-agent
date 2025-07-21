
class HandState:
    def __init__(self, hero_hand, positions, hero_stack=100, villain_stack=100, sb=1, bb=2):
        self.hero_hand = hero_hand
        self.board = []
        self.pot = 0
        self.players = positions        # contains (names, position, stack)
        self.street = 'preflop'
        self.history = []
        self.sb = sb
        self.bb = bb

        sb_player = next(name for name, info in self.players.items() if info['position'] == 'sb')
        bb_player = next(name for name, info in self.players.items() if info['position'] == 'bb')

        self.add_action(sb_player, 'post_sb', sb)
        self.add_action(bb_player, 'post_bb', bb)
        

    def add_action(self, player, action, amount=0):
        self.players[player]['stack'] -= amount
        self.pot += amount
        self.history.append({'player': player, 'action': action, 'amount': amount})

    def get_player_pot_contribution(self, player):
        """Get the total amount a player has contributed to the pot."""
        return sum(action['amount'] for action in self.history if action['player'] == player)

    def get_legal_actions(self):
        """
        Determine legal actions based on the current street and last action.
        Returns a list of legal actions.
        """
        last_action = self.history[-1] if self.history else None
        legal_actions = ['fold', 'call', 'raise']

        if self.street == 'preflop':
            if last_action == ['post_bb']:
                legal_actions.remove('check')


    def next_street(self, cards):
        self.board.extend(cards)
        if self.street == 'preflop':
            self.street = 'flop'
        elif self.street == 'flop':
            self.street = 'turn'
        elif self.street == 'turn':
            self.street = 'river'

