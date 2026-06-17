import random
from typing import List, Dict, Optional, Tuple

class BlackjackGame:
    def __init__(self, player_id: int) -> None:
        self.player_id: int = player_id
        self.deck: List[Dict[str, str]] = self._create_deck()
        random.shuffle(self.deck)
        self.player_hand: List[Dict[str, str]] = []
        self.dealer_hand: List[Dict[str, str]] = []
        self.finished: bool = False
        self.winner: Optional[str] = None
        self.player_score: int = 0
        self.dealer_score: int = 0

        for _ in range(2):
            self.player_hand.append(self._draw_card())
            self.dealer_hand.append(self._draw_card())

    def _create_deck(self) -> List[Dict[str, str]]:
        suits = ['♥', '♦', '♣', '♠']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [{'rank': r, 'suit': s} for s in suits for r in ranks]

    def _draw_card(self) -> Dict[str, str]:
        return self.deck.pop()

    def _hand_value(self, hand: List[Dict[str, str]]) -> int:
        value: int = 0
        aces: int = 0
        for card in hand:
            rank: str = card['rank']
            if rank.isdigit():
                value += int(rank)
            elif rank in ['J', 'Q', 'K']:
                value += 10
            else:
                aces += 1
                value += 11
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        return value

    def _is_bust(self, hand: List[Dict[str, str]]) -> bool:
        return self._hand_value(hand) > 21

    def _hand_str(self, hand: List[Dict[str, str]], hide_first: bool = False) -> str:
        if hide_first:
            return f"{hand[0]['rank']}{hand[0]['suit']} 🂠"
        return " ".join([f"{c['rank']}{c['suit']}" for c in hand])

    def player_turn(self, action: str) -> Tuple[str, int, int]:
        if self.finished:
            return "Игра уже закончена.", self.player_score, self.dealer_score

        if action == "hit":
            self.player_hand.append(self._draw_card())
            self.player_score = self._hand_value(self.player_hand)
            if self._is_bust(self.player_hand):
                self.finished = True
                self.winner = "dealer"
                return f"💥 Перебор! Ты проиграл.", self.player_score, self.dealer_score
            return f"✅ Взял карту. У тебя {self.player_score} очков.", self.player_score, self.dealer_score

        elif action == "stand":
            self.finished = True
            return self._dealer_turn()

        return "Неизвестное действие.", self.player_score, self.dealer_score

    def _dealer_turn(self) -> Tuple[str, int, int]:
        while self._hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self._draw_card())

        self.player_score = self._hand_value(self.player_hand)
        self.dealer_score = self._hand_value(self.dealer_hand)

        if self._is_bust(self.dealer_hand):
            self.winner = "player"
            return f"🎉 Дилер перебрал! Ты выиграл!", self.player_score, self.dealer_score
        elif self.dealer_score > self.player_score:
            self.winner = "dealer"
            return f"😞 Дилер выиграл.", self.player_score, self.dealer_score
        elif self.player_score > self.dealer_score:
            self.winner = "player"
            return f"🎉 Ты выиграл!", self.player_score, self.dealer_score
        else:
            self.winner = "tie"
            return f"🤝 Ничья!", self.player_score, self.dealer_score

    def get_status(self) -> str:
        if self.finished:
            return "Игра закончена."
        return (
            f"**Твои карты:** {self._hand_str(self.player_hand)} — {self._hand_value(self.player_hand)} очков\n"
            f"**Карты дилера:** {self._hand_str(self.dealer_hand, hide_first=True)}"
        )