class HandState:
    def __init__(self, hero_hand, players, sb=1, bb=2):
        self.hero_hand = hero_hand
        self.board = []
        self.pot = 0
        self.players = players        # contains (names: position, stack, contribution)
        self.active_players = list(players.keys())
        self.street = 'preflop'
        self.street_contributions = {player: 0 for player in players}
        self.history = []
        self.sb = sb
        self.bb = bb

        sb_player = next(name for name, info in self.players.items() if info['position'] == 'sb')
        bb_player = next(name for name, info in self.players.items() if info['position'] == 'bb')

        self.add_message('Preflop Start')
        self.add_action(sb_player, 'post_sb', sb)
        self.add_action(bb_player, 'post_bb', bb)
        

    def add_action(self, player, action, amount):
        """
        amount = total contribution this street after this action (NOT increment).
        Example:
        - If player had 2 in already and raises to 10, amount=10 (not +8).
        """
        prev_contribution = self.street_contributions.get(player, 0)


        if action in ["call", "raise", "all in", "bet", "post_sb", "post_bb"]:
            # Update total contribution for this street
            self.street_contributions[player] = amount

            # Only add the increment to pot/stack
            increment = amount - prev_contribution
            self.players[player]['stack'] -= increment
            self.players[player]['contribution'] += increment
            self.pot += increment

            self.history.append({'player': player, 'act': action, 'amt': amount, 'str': self.street})

        elif action in ["check"]:
            self.history.append({'player': player, 'act': "check", 'str': self.street})

        elif action in ["fold"]: 
            self.active_players.remove(player)
            self.add_message(f"{player} folds")

    def add_message(self, message):
        """Add a message to the history for logging purposes."""
        self.history.append(message)

    def get_player_pot_contribution(self, player):
        """Get the total amount a player has contributed to the pot."""
        return self.players[player]['contribution']


    def next_street(self, cards):
        self.board.extend(cards)
        self.street_contributions = {p: 0 for p in self.players}  # reset per-street bets
        if self.street == 'preflop':
            self.add_message('Flop Start')
            self.street = 'flop'
        elif self.street == 'flop':
            self.add_message('Turn Start')
            self.street = 'turn'
        elif self.street == 'turn':
            self.add_message('River Start')
            self.street = 'river'
        elif self.street == 'river':
            self.add_message('Showdown')

    def betting_round_complete(self):
        """Returns True if betting round is finished."""
        active_players = self.active_players
        
        # If only 1 player left, round is auto-complete
        if len(active_players) <= 1:
            return True

        highest_bet = max(self.street_contributions.values())

        for p in active_players:
            contrib = self.street_contributions[p]
            stack = self.players[p]["stack"]

            # ✅ If someone hasn't matched the highest bet and is not all-in
            if contrib < highest_bet and stack > 0:
                return False
            
            # if player has a stack, they must act on this street
            if stack > 0:
                # Check if player has acted in this street (excluding messages)
                has_acted = False
                for action in self.history:
                    if isinstance(action, dict) and action.get('player') == p and action.get('str') == self.street:
                        has_acted = True
                        break
                        
                # If player hasn't acted this street, betting round isn't complete
                if not has_acted:
                    return False

        return True
