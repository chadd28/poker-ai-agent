import os
from dotenv import load_dotenv
load_dotenv()

class AIAgent:
    def __init__(self, provider='gemini', model_name='gemini-1.5-flash'):
        self.model_name = model_name
        self.provider = provider

        if provider == 'gemini':
            from google import genai
            # The client gets the API key from the environment variable `GEMINI_API_KEY`.
            self.client = genai.Client()
        if provider == 'groq':
            from groq import Groq
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def make_decision(self, hand_state, game_state, legal_actions):
        """
        Notes:
        ** Ive noticed that more prompt makes the AI less accurate **
            HAND STRENGTH GUIDE (preflop only):
            - PREMIUM: AA, KK, QQ, JJ, AK
            - STRONG: AQ, AJ, AT, KQ, KJ, TT, 99, 88, 77, high suited connectors (see definition)

             DEFINITION:
            - "Suited connectors" are two CONSECUTIVE cards of the same suit, e.g., 7h 8h, 9s Ts, Jc Qc.
                - Example: Jd 9d is NOT a suited connector (not consecutive), but Jd Td is.
            - "Suited one-gappers" are two cards of the same suit with one rank between, e.g., 6d 8d, 9c Jc.

            STRATEGY:
            - You can play with whatever strategy you want, but you must follow the rules below.

            CRITICAL RULES:
                - Your hand is exactly 2 cards. Do NOT confuse two different cards as a pair.
                - Use ONLY the information above. Do NOT assume suits, connections, or hand strength unless explicitly present.
                - If the board is empty (preflop), do NOT reference pairs or made hands unless you have a pocket pair.
                - Do NOT assume you will see a flop or future cards; other players may raise or fold after you (unless you are last to act).
                - Only choose legal actions for this street and situation.
                    - Bet/raise sizes must be between the minimum bet size and your stack.
                    - Do NOT suggest bets larger than the pot or stack.
                    - MINIMUM BET SIZE: For "raise", bet_size must be at least the previous bet/raise plus the amount of the last raise (minimum raise = previous bet + last raise amount), and no more than your stack.
                - Position matters: button is best, blinds are worst.
                    - The order of play is sb, bb, utg, mp, co, button. This adjusts based on the number of players.
                - If checking is allowed, you may check (bet_size = 0).
                - If folding is allowed, you may fold.
                - If calling is allowed, you may call.
                    
            
            REASONING:
                - You must state both cards in plain English (e.g., "ten of diamonds and three of diamonds").
                - Mention how your position affects your decision.
                - State what the action is trying to achieve briefly.
                - If you are unsure or confused about the input, respond in reasoning with "I do not understand because...".
            
        
        """
        strategy = "AGRESSIVE"
        prompt = f"""
            You are a professional No-Limit Hold'em poker player named AlbertIntel (AI) playing against {game_state.player_count - 1} opponents.
            You have extensive knowledge of poker strategy, hand evaluation, and the rules of poker.
            All cards are represented as a two-character string, e.g., 'Js' for Jack of spades. 
                (h = hearts, d = diamonds, c = clubs, s = spades)
            
            GAME INFO:
            - Small blind: ${game_state.sb}, Big blind: ${game_state.bb}
            - Your hand: {hand_state.hero_hand}
            - Board: {hand_state.board if hand_state.board else 'No board yet, preflop'}
            - You have contributed: ${hand_state.get_player_pot_contribution('AI')} so far into the pot.
            - Current pot: ${hand_state.pot}
            - Your position and stack: {hand_state.players.get('AI')}
            - Players (position & stack): {hand_state.players}
            - There are {len(hand_state.active_players)} active players: {hand_state.active_players}
            - Action history: {hand_state.history}
                - "act" is the action taken by the player.
                - "amt" is the total contribution after the action (not increment).
                - "str" is the street (preflop, flop, turn, river) of the logged action.
            - Last action: {hand_state.history[-1]}
            - Current street: {hand_state.street}

            <strategy>{strategy}</strategy>

            RULES FOR DECISION:
            1. ONLY use the information provided — do not infer hidden cards or made hands (like top pair preflop) unless explicitly present.
            2. "action" must be one of: {legal_actions} (EXACTLY as written, no amounts included in the action).
            3. "raise_size" must represent the **TOTAL amount you are raising TO**, not how much more you are adding.
                - Example: If the current highest bet is $5 and you raise to $12, `raise_size` = 12.
            4. If you choose "call", "all in", "check", or "fold", ALWAYS set "raise_size" = 0.
            5. Always choose a valid legal action based on the current pot and betting rules.
            6. Briefly explain your reasoning in 2-3 sentences referencing your exact hand in english, bluff opportunities (if applicable), the history of the hand, the board, and pot odds (if applicable).
             
            RESPOND ONLY IN VALID JSON (no extra text):
            {{
                "action": "fold" | "check" | "call" | "raise" | "all in",
                "raise_size": <integer>,
                "reasoning": "<your explanation>"
            }}
            """
        
        # print(f"AI Prompt: {prompt}")

        if self.provider == 'gemini':
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text.strip()
        
        elif self.provider == 'groq':
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
            )

            return chat_completion.choices[0].message.content
