from kivy.app import App
from kivy.uix.widget import Widget
from tetris import main as tetris_main

class TetrisGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        tetris_main()

class TetrisApp(App):
    def build(self):
        return TetrisGame()

if __name__ == '__main__':
    TetrisApp().run() 