import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        return Label(text='Hello world')

def launch():
    #MyApp().run()
    return 0