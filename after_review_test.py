# coding: utf-8
import unittest
from after_review_deck_of_cards import *


class TestStringMethods(unittest.TestCase):
    def test_xceededMaximumCardsException(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9",
                    "10", "валет", "дама", "король", "туз"]
        suits = ["пики", "червы", "бубны", "трефы", "Spades",
                    "Hearts", "Diamonds", "Clubs"]
        with self.assertRaises(ExceededMaximumCardsException):
            _ = Deck(suits, ranks)

    def test_duplicateCardsException(self):
        ranks = ["2", "2", "2", "валет", "дама", "король", "туз"]
        suits = ["пики", "червы", "бубны", "трефы"]
        with self.assertRaises(DuplicateCardsException):
            _ = Deck(suits, ranks)

    def test_Card(self):
        rank = "2"
        suit = "пики"
        seniority = 1
        # типы класса (class '__main__.Card') и строки ('str') не совпадают
        # они просто имеют одинаковые str представления потому класс в строку
        self.assertEqual(str(Card(suit, rank, seniority)), rank + " " + suit)

    def test_Deck_create_list_cards(self):
        ranks = ["2", "3", "4", "5", "валет", "дама", "король", "туз"]
        suits = ["пики", "червы", "бубны", "трефы"]
        deck = Deck(suits, ranks)

        cards = []
        for suit in suits:
            for rank in ranks:
                cards.append(rank + " " + suit)

        cards_from_class = []
        for card in deck.list_cards():
            cards_from_class.append(str(card))

        self.assertEqual(cards_from_class, cards)

    def test_Deck_how_many(self):
        ranks = ["2", "3", "4", "5", "валет", "дама", "король", "туз"]
        suits = ["пики", "червы", "бубны", "трефы"]
        deck1 = Deck(suits, ranks)
        b = len(ranks) * len(suits)
        self.assertEqual(deck1.how_many, b)

    def test_Deck_shuffle(self):
        ranks = ["2", "3", "4", "5", "валет", "дама", "король", "туз"]
        suits = ["пики", "червы", "бубны", "трефы"]
        deck2 = Deck(suits, ranks)
        deck2.shuffle()

        cards = []
        for suit in suits:
            for rank in ranks:
                cards.append(rank + " " + suit)

        cards_from_class = []
        for card in deck2.list_cards():
            cards_from_class.append(str(card))

        self.assertNotEqual(cards_from_class, cards)

    def test_Deck_sort_deck(self):
        ranks = ["2", "3", "4", "5", "валет", "дама", "король", "туз"]
        suits = ["пики", "червы", "бубны", "трефы"]
        deck3 = Deck(suits, ranks)
        deck3.shuffle()
        deck3.sort_deck()

        cards = []
        for suit in suits:
            for rank in ranks:
                cards.append(rank + " " + suit)

        cards_from_class = []
        for card in deck3.list_cards():
            cards_from_class.append(str(card))

        self.assertEqual(cards_from_class, cards)

    def test_Deck_dict_for_file_json(self):
        # для неперемешанной колоды
        ranks = ["2", "3", "4", "5", "валет", "дама", "король", "туз"]
        suits = ["пики", "червы", "бубны", "трефы"]
        deck4 = Deck(suits, ranks)

        order = 0
        dict_order = {}
        dict_order["shafled"] = False
        n = 0
        for suit in suits:
            for rank in ranks:
                n += 1
                print(rank + " " + suit)
                dict_card = {}
                dict_card["rank"] = rank
                dict_card["suit"] = suit
                dict_card["seniority"] = n
                order += 1
                dict_order[order] = dict_card
        # независимый словарь равен словарю из колоды
        self.assertEqual(deck4.dict_for_file_json(), dict_order)

    def test_Deck_from_file_json(self):
        # для неперемешанной колоды
        ranks = ["2", "3", "4", "5", "валет", "дама", "король", "туз"]
        suits = ["пики", "червы", "бубны", "трефы"]
        deck5 = Deck(suits, ranks)

        order = 0
        dict_From_file_json = {}
        dict_From_file_json["shafled"] = False
        n = 0
        for suit in suits:
            for rank in ranks:
                n += 1
                print(rank + " " + suit)
                dict_card = {}
                dict_card["rank"] = rank
                dict_card["suit"] = suit
                dict_card["seniority"] = n
                order += 1
                dict_From_file_json[order] = dict_card
        # создали колоду из словаря
        # метод удаляет "shafled" из принимаемого словаря
        deck5.from_file_json(dict_From_file_json)
        # поэтому добавляем "shafled" назад в словарь
        dict_From_file_json["shafled"] = False
        # возвращенный из колоды словарь должен быть
        # равен словарю передаваемому в колоду (учтя "shafled")
        self.assertEqual(deck5.dict_for_file_json(), dict_From_file_json)


if __name__ == '__main__':
    unittest.main()
