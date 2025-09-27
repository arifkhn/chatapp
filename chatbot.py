from kivymd.app import MDApp
from kivy.lang import Builder 
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.modalview import ModalView
from kivymd import images_path
from kivymd.uix.card import MDCard
import speech_recognition as sr
import os 
import webbrowser
import random
import numpy as np




Window.size = (300, 630)



class ChatBot(MDApp):

    def change_screen(self, name):
        screen_manager.current = name


    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("Main.kv"))
        screen_manager.add_widget(Builder.load_file("Chats.kv"))
        screen_manager.add_widget(Builder.load_file("chat.kv"))
        return screen_manager
    

if __name__=='__main__':
    ChatBot().run()

