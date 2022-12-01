from unittest import TestCase
from Program import clear_html, request_parser, remove_repeated_spaces, string_reducer

class Program_test(TestCase):
    def test_clear_html(self):
        self.assertEqual(clear_html('<div><p>some <span>text</span></p></div>'), 'some text')

    def test_remove_repeated_spaces(self):
        self.assertEqual(remove_repeated_spaces('some         text'), 'some text')

    def test_string_reducer(self):
        text = "qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty"
        result = "qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwertyqwer..."
        self.assertEqual(string_reducer(text), result)

    def test_replace_boolean_values(self):
        self.assertEqual("True", 'Да')
        self.assertEqual("TRUE", 'Да')
        self.assertEqual("False", 'Нет')
        self.assertEqual("FALSE", 'Нет')

    def test_request_parser(self):
        self.assertEqual(request_parser('Навыки: Git, ещё что-то, что-то ещё'),['Навыки', ['Git', 'ещё что-то', 'что-то ещё']])
