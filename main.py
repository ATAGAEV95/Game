from kivy.app import App
from kivy.lang import Builder
import random

KV = """
BoxLayout:
    orientation: 'vertical'
    Label:
        id: game_label
        text: 'Угадай число!'
        size_hint: 1, 0.1
    TextInput:
        id: game_input
        multiline: False
        size_hint: 1, 0.15
    Label:
        id: guess_label
        text: ''
        size_hint: 1, 0.1
    Label:
        text: 'Введите начальное число:'
        size_hint: 1, 0.1
        canvas.before:
            Color:
                rgba: 0, 0, 1, 1  # Синий цвет
            Rectangle:
                pos: self.pos
                size: self.size
    TextInput:
        id: a_input
        multiline: False
        size_hint: 1, 0.15
    Label:
        text: 'Введите конечное число:'
        size_hint: 1, 0.1
        canvas.before:
            Color:
                rgba: 0, 0, 1, 1  # Синий цвет
            Rectangle:
                pos: self.pos
                size: self.size
    TextInput:
        id: b_input
        multiline: False
        size_hint: 1, 0.15
    Button:
        text: 'Ввод'
        on_press: app.check_number()
        size_hint: 1, 1
    Button: 
        text: 'Сгенерировать число'
        on_press: app.start_game()
        size_hint: 1, 1
"""

class MyApp(App):
    active_input = None
    def build(self):
        return Builder.load_string(KV)

    def start_game(self):
        self.root.ids.game_input.text = ''
        self.root.ids.guess_label.text = ''
        self.history = []
        self.attempts = 0
        try:
            self.a = int(self.root.ids.a_input.text)
            self.b = int(self.root.ids.b_input.text)
            if self.a >= self.b:
                self.root.ids.game_label.text = 'Конечное число должно быть больше начального числа.'
            else:
                self.x = random.randint(self.a, self.b)
                self.root.ids.game_label.text = 'Угадай число!'
        except ValueError:
            self.root.ids.game_label.text = 'Введите число'

    def check_number(self):
        if hasattr(self, 'x'):
            try:
                y = int(self.root.ids.game_input.text)
                self.attempts += 1
                if y == self.x:
                    self.root.ids.game_label.text = f'Верно! Попыток: {self.attempts}'
                    self.history.append(f'{y}: Верно!')
                elif y < self.a or y > self.b:
                    self.root.ids.game_label.text = f'Введите число от {self.a} до {self.b}'
                    self.history.append(f'{y}: Введите число от {self.a} до {self.b}')
                elif y < self.x:
                    self.root.ids.game_label.text = 'Больше'
                    self.history.append(f'{y}: Больше')
                else:
                    self.root.ids.game_label.text = 'Меньше'
                    self.history.append(f'{y}: Меньше')
                self.history = self.history[-3:]
                self.root.ids.guess_label.text = '\\   '.join(self.history)
            except ValueError:
                self.root.ids.game_label.text = 'Введите число'
        else:
            self.root.ids.game_label.text = 'Сначала сгенерируйте число'
        self.root.ids.game_input.text = ''

    def add_number(self, number):
        if self.active_input is not None:
            self.active_input.text += str(number)

    def remove_last_number(self):
        if self.active_input is not None and self.active_input.text:
            self.active_input.text = self.active_input.text[:-1]

MyApp().run()
