from kivy.properties import StringProperty
from kivy.properties import StringProperty, ListProperty
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFillRoundFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
import pygame
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty
import os
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
import random

from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen


Window.size = (480, 650)

pygame.mixer.init()

Letters_with_sticks = ["п", "н", "т", "г", "ш", "ц"]
buttons_array1 = []
Letters_with_hooks = ["б", "д", "з", "ф", "в", "ч", "щ"]
buttons_array2 = []
Letters_with_crossbars = ["ж", "к", "т", "н", "п", "м", "л"]
buttons_array3 = []
Letters_with_loops = ["с", "э", "р", "ъ", "ь"]
buttons_array4 = []
Letters_with_double_elements = ["ж", "х", "м", "ш", "щ"]
buttons_array5 = []
Special_consonants = ["й", "ц", "ч", "щ", "ъ", "ь"]



consonants = ['б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м',
              'н', 'п', 'р', 'с', 'т', 'ф', 'х', 'ц', 'ч', 'ш', 'щ']
vowels = ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я']


class SyllableScreen1(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDGridLayout(cols=5, spacing=10, padding=20, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self.layout)

        main_layout = MDFloatLayout()
        main_layout.add_widget(scroll)

        # Добавляем кнопку "назад"
        back_btn = ImageButton(
            source='back.png',
            size_hint=(.15, .15),
            pos_hint={'x': 0.8, "y": 0.85}
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'first'))

        main_layout.add_widget(back_btn)
        self.add_widget(main_layout)

        self.create_syllables()

    def create_syllables(self):
        for consonant in Letters_with_sticks:
            for vowel in vowels:
                syllable = consonant + vowel
                btn = MDRectangleFlatButton(
                    text=syllable,
                    size_hint=(None, None),
                    text_color=(1, 1, 1, 1),
                    size=("80dp", "60dp"),
                    on_release=self.play_syllable_sound,
                )
                buttons_array1.append(btn)
                self.layout.add_widget(btn)

    def play_syllable_sound(self, instance):
        print(f"Playing sound for: {instance.text}")


class SoundGameScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.syllables = ["ба", "бо", "бу", "ва", "во", "ву", "га", "го", "гу"]
        self.current_syllable = None
        self.score = 0
        self.attempts = 0
        self.max_questions = 5

        self.layout = MDBoxLayout(orientation="vertical", padding=20, spacing=20)
        self.layout.bind(minimum_height=self.layout.setter('height'))

        # Верхняя панель
        self.top_panel = MDBoxLayout(size_hint=(1, 0.1), spacing=10)
        self.score_label = MDLabel(text=f"Счет: {self.score}")
        self.question_label = MDLabel(text=f"Вопрос 1/{self.max_questions}")
        self.top_panel.add_widget(self.score_label)
        self.top_panel.add_widget(self.question_label)

        # Кнопка воспроизведения
        self.play_btn = ImageButton(
            size_hint=(1, 0.2),
            on_release=self.play_sound,
            source='sound.png'
        )

        # Grid с вариантами
        self.answers_grid = MDGridLayout(cols=3, spacing=10, size_hint=(1, 0.6))

        # Кнопка назад
        self.back_btn = ImageButton(
            source= 'back.png',
            size_hint= (.15, .15),
            on_release=self.go_back
        )

        self.layout.add_widget(self.top_panel)
        self.layout.add_widget(self.play_btn)
        self.layout.add_widget(self.answers_grid)
        self.layout.add_widget(self.back_btn)

        scroll = ScrollView()
        scroll.add_widget(self.layout)
        self.add_widget(scroll)

        self.generate_question()

    def go_back(self, instance):
        self.manager.current = 'with_hooks'  # Возвращаемся на экран с слогами

    def load_sounds(self):
        self.sounds = {}
        for syllable in self.syllables:
            self.sounds[syllable] = SoundLoader.load(f'{syllable}.wav')

    def generate_question(self):
        self.attempts += 1
        if self.attempts > self.max_questions:
            self.show_results()
            return

        self.question_label.text = f"Вопрос {self.attempts}/{self.max_questions}"
        self.answers_grid.clear_widgets()

        self.current_syllable = random.choice(self.syllables)
        options = random.sample(self.syllables, 3)
        if self.current_syllable not in options:
            options[0] = self.current_syllable
        random.shuffle(options)

        for option in options:
            btn = Button(
                background_color= (0.5, 1, 1, 1),
                text=option,
                font_size= '60sp',
                size_hint= (.25, .15),
                on_release=self.check_answer
            )
            self.answers_grid.add_widget(btn)

    def play_sound(self, instance):
        if self.current_syllable and hasattr(self, 'sounds'):
            sound = self.sounds.get(self.current_syllable)
            if sound:
                sound.play()

    def check_answer(self, instance):
        selected = instance.text
        if selected == self.current_syllable:
            self.score += 1
            self.score_label.text = f"Счет: {self.score}"
            instance.md_bg_color = (0, 1, 0, 1)
        else:
            instance.md_bg_color = (1, 0, 0, 1)

        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.generate_question(), 1)

    def show_results(self):
        self.answers_grid.clear_widgets()
        result_label = MDLabel(
            text=f"Игра окончена!\nПравильных ответов: {self.score}/{self.max_questions}",
            halign="center"
        )
        self.answers_grid.add_widget(result_label)

        restart_btn = MDFillRoundFlatButton(
            text="Играть снова",
            on_release=self.restart_game
        )
        self.answers_grid.add_widget(restart_btn)

    def restart_game(self, instance):
        self.score = 0
        self.attempts = 0
        self.score_label.text = f"Счет: {self.score}"
        self.generate_question()


class SyllableScreen2(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = MDBoxLayout(
            orientation="vertical",
            spacing=20,
            padding=20,
            size_hint_y=None
        )
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self.main_layout)

        back_btn = ImageButton(
            source='back.png',
            size_hint=(.15, .15),
            pos_hint={'x': 0.8, "y": 0.85},
            on_press=lambda x: setattr(self.manager, 'current', 'first')
        )

        self.add_widget(scroll)
        self.add_widget(back_btn)
        self.create_syllables()

    def create_syllables(self):
        current_group_layout = None

        for consonant in Letters_with_hooks:
            if current_group_layout is None:
                current_group_layout = MDGridLayout(
                    cols=5,
                    spacing=10,
                    size_hint_y=None,
                    adaptive_height=True
                )
                self.main_layout.add_widget(current_group_layout)

            for vowel in vowels:
                syllable = consonant + vowel
                btn = MDRectangleFlatButton(
                    text=syllable,
                    size_hint=(None, None),
                    text_color=(1, 1, 1, 1),
                    size=("80dp", "60dp"),
                    on_release=lambda x, syll=syllable: self.go_to_new_screen(syll),
                )
                buttons_array2.append(btn)
                current_group_layout.add_widget(btn)

            btn_exercise = MDRectangleFlatButton(
                text="Упражнения",
                size_hint=(1, None),
                height="100dp",
                md_bg_color=(0.2, 0.2, 0.2, 1),
                on_release=self.start_game  # Изменено на вызов игры
            )
            self.main_layout.add_widget(btn_exercise)
            current_group_layout = None

    def start_game(self, instance):
        """Запуск игры при нажатии на кнопку Упражнения"""
        if hasattr(self, 'manager'):
            # Проверяем, есть ли уже экран игры в менеджере
            if not self.manager.has_screen('sound_game'):
                game_screen = SoundGameScreen(name='sound_game')
                self.manager.add_widget(game_screen)

            # Загружаем звуки при первом переходе
            if not hasattr(self.manager.get_screen('sound_game'), 'sounds_loaded'):
                self.manager.get_screen('sound_game').load_sounds()
                self.manager.get_screen('sound_game').sounds_loaded = True

            self.manager.current = 'sound_game'

    def go_to_new_screen(self, syllable):
        if hasattr(self, 'manager'):
            trial_screen = self.manager.get_screen('trial_version')
            trial_screen.syllable = syllable
            self.manager.current = 'trial_version'


class TextBuildingScreen(MDScreen):
    images = ListProperty([
        "2.png", "3.png", "4.png", "5.png", "6.png",
        "7.png", "8.png", "9.png", "10.png",
        "13.png", "14.png", "15.png"
    ])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = MDBoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20
        )

        # Заголовок
        self.header_label = MDLabel(
            text="Задание 1. Разложить серию сюжетных картинок в соответствии с прочитанным текстом.",
            font_style='H6',
            halign='center',
            size_hint_y=0.1
        )

        # Текст задания в ScrollView
        self.task_text = (
            "Три котёнка — чёрный, серый и белый — увидели мышь и бросились за ней! "
            "Мышь прыгнула в банку с мукой. Котята — за ней! Мышь убежала. "
            "А из банки вылезли три белых котёнка. Три белых котёнка увидели на дворе лягушку "
            "и бросились за ней! Лягушка прыгнула в старую самоварную трубу. Котята — за ней! "
            "Лягушка ускакала, а из трубы вылезли три чёрных котёнка. "
            "Три чёрных котёнка увидели в пруду рыбу… и бросились за ней! "
            "Рыба уплыла, а из воды вынырнули три мокрых котёнка. "
            "Три мокрых котёнка пошли домой. По дороге они обсохли и стали как были: "
            "чёрный, серый и белый."
        )
        self.task_label = MDLabel(
            text=self.task_text,
            font_style='Body1',
            size_hint_y=None,
            height=300,
            text_size=(self.width - 40, None),
            halign='left'
        )
        self.scroll_view = ScrollView(size_hint_y=0.4)
        self.scroll_view.add_widget(self.task_label)

        # Прокручиваемая сетка для изображений
        self.grid_layout = MDGridLayout(
            cols=4,
            spacing=10,
            padding=10,
            size_hint_y=None,
            adaptive_height=True
        )
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.grid_scroll = ScrollView(size_hint_y=0.5)
        self.grid_scroll.add_widget(self.grid_layout)

        # Динамически добавляем MDCard с изображениями
        for image in self.images:
            card = MDCard(
                size_hint=(None, None),
                size=("100dp", "65dp"),
                elevation=1,
                orientation='vertical',
                padding="5dp"
            )
            img = Image(
                source=image,
                allow_stretch=True,
                keep_ratio=True
            )
            card.add_widget(img)
            self.grid_layout.add_widget(card)

        self.back_button = ImageButton(
            source='back.png',
            size_hint=(None, None),
            size=("50dp", "50dp"),
            pos_hint={"x": 0.02, "y": 0.02}
        )
        self.back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'first'))

        # Добавляем виджеты в основной контейнер
        self.main_layout.add_widget(self.header_label)
        self.main_layout.add_widget(self.scroll_view)
        self.main_layout.add_widget(self.grid_scroll)
        self.main_layout.add_widget(self.back_button)

        # Добавляем основной контейнер на экран
        self.add_widget(self.main_layout)


class ImageButton(ButtonBehavior, Image):
    pass

class FirstScreen(MDScreen):
    pass


class SecondScreen(MDScreen):
    pass


class PlayScreen(MDScreen):
    pass

class Trial_versionScreen(MDScreen):
    syllable = StringProperty('')

class SentensScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Основной layout
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)

        # Метка для текста
        self.text_label = MDLabel(text="Составьте предложение", halign='center', size_hint_y=None, height="48dp")

        # Поле для ввода текста
        self.text_input = MDTextField(
            hint_text="Введите текст",
            size_hint=(1, None),
            height="48dp"
        )

        # Кнопка проверки
        self.check_btn = MDRaisedButton(
            text="Проверить предложение",
            size_hint=(None, None),
            size=("200dp", "48dp"),
            on_release=self.check_sentence
        )

        # Кнопка сброса
        self.reset_btn = MDRaisedButton(
            text="Сбросить",
            size_hint=(None, None),
            size=("200dp", "48dp"),
            on_release=self.reset_input
        )

        # Добавляем элементы в layout
        self.layout.add_widget(self.text_label)
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.check_btn)
        self.layout.add_widget(self.reset_btn)

        self.add_widget(self.layout)

    def check_sentence(self, instance):
        """Функция для проверки введенного предложения"""
        user_input = self.text_input.text
        # Простая проверка: просто проверим, есть ли в предложении глаголы или существительные
        if any(word in user_input for word in ["пошел", "сказал", "видел", "сделал"]):
            self.text_label.text = "Предложение правильное!"
        else:
            self.text_label.text = "Предложение неправильное, попробуйте снова!"

    def reset_input(self, instance):
        """Функция для сброса поля ввода"""
        self.text_input.text = ""
        self.text_label.text = "Составьте предложение"


class MyApp(MDApp):
    def build(self):
        sm = MDScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        sm.add_widget(PlayScreen(name='play'))
        sm.add_widget(SentensScreen(name='sentens'))
        sm.add_widget(SyllableScreen1(name='with_sticks'))
        sm.add_widget(SyllableScreen2(name='with_hooks'))
        sm.add_widget(TextBuildingScreen(name='text_building'))
        sm.add_widget(Trial_versionScreen(name='trial_version'))
        sm.add_widget(SoundGameScreen(name='sound_game'))  # Добавляем экран игры

        # Загружаем звуки после инициализации
        def load_sounds(dt):
            if sm.has_screen('sound_game'):
                sm.get_screen('sound_game').load_sounds()
                sm.get_screen('sound_game').sounds_loaded = True

        from kivy.clock import Clock
        Clock.schedule_once(load_sounds, 0.5)

        return sm


if __name__ == '__main__':
    MyApp().run()
