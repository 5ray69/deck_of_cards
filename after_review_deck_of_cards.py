# -*- coding: utf-8 -*-
import clr
clr.AddReference('System.Windows.Forms')
import System.Windows.Forms as WF
from random import shuffle
import json

class ExceededMaximumCardsException(Exception):
    def __init__(self):
        self.message = "В колоде должно быть не более 100 карт. \
                        \nНужно уменьшить количества в списках"
        WF.MessageBox.Show(self.message)

    def __str__(self):
        return (self.message)


class DuplicateCardsException(Exception):
    def __init__(self):
        self.message = "В списках не должно быть повторяющихся элементов. \
                        \nУдалите повторяющиеся элементы"
        WF.MessageBox.Show(self.message)

    def __str__(self):
        return (self.message)


class Card(object):
    def __init__(self, suit, rank, seniority):
        self.rank = rank  # часть названия карты, ранг
        self.suit = suit  # другая часть названия карты, масть
        self.seniority = seniority  # для создания порядка в колоде, заданного пользователем

    def __str__(self):
        return (self.rank + " " + self.suit)


class Deck(object):
    def __init__(self, suits, ranks):
        self.ranks = ranks  # список званий карт
        self.suits = suits  # список мастей карт
        self.shafled = False  # перемешана ли колода
        self.cards = self._create_cards(ranks, suits)

    @staticmethod
    def _create_cards(ranks, suits):
        cards = []

        if len(ranks) * len(suits) > 100:
            raise ExceededMaximumCardsException()
            return cards

        if len(ranks) != len(set(ranks)) or (len(suits) != len(set(suits))):
            raise DuplicateCardsException()
            return cards

        n = 0
        for suit in suits:
            for rank in ranks:
                n += 1
                cards.append(Card(suit, rank, n))
        return cards

    @property
    def how_many(self):
        return len(self.cards)

    def list_cards(self):
        return self.cards

    def shuffle(self):
        shuffle(self.cards)
        self.shafled = True

    def sort_deck(self):
        self.cards.sort(key=lambda card: card.seniority, reverse=False)
        self.shafled = False

    def dict_for_file_json(self):
        order = 0
        dict_order = {}
        dict_order["shafled"] = self.shafled
        for card in self.list_cards():
            dict_card = {}
            dict_card["rank"] = card.rank
            dict_card["suit"] = card.suit
            dict_card["seniority"] = card.seniority
            order += 1
            dict_order[order] = dict_card
        return dict_order

    def from_file_json(self, dict_From_file_json):
        json_create_cards = []
        # значение индикатора перемешана ли колода
        self.shafled = dict_From_file_json.pop("shafled")
        # отсортировали в порядке(order) в каком карты упаковывались в json
        sorted_tuple = sorted(
            dict_From_file_json.items(), key=lambda x: int(x[0]))
        for key_order, value_dict_card in sorted_tuple:
            json_create_cards.append(
                Card(
                    value_dict_card["suit"],
                    value_dict_card["rank"],
                    value_dict_card["seniority"]
                    )
            )
        self.cards = json_create_cards

if __name__ == '__main__':
    # список карт в порядке возрастания старшинства для создания колоды
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "валет", "дама", "король", "туз"]
    # список мастей карт в порядке возрастания старшинства для создания колоды
    suits = ["пики", "червы", "бубны", "трефы"]

    # Создаем экземпляр колоды
    deck = Deck(suits, ranks)
    # перемешиваем колоду
    deck.shuffle()

    # создаем файл json
    with open('my.json', 'w') as file:
        json.dump(deck.dict_for_file_json(), file, indent=4)

    # читаем файл json
    with open('my.json', 'r') as file:
        dict_From_file_json = json.load(file)

    # экземпляр колоды созданной десериализацией
    deck.from_file_json(dict_From_file_json)

    # печатаем карты колоды созданной десериализацией
    for card in deck.list_cards():
        print('№ {}, имя карты - {}'.format(card.seniority, card))
