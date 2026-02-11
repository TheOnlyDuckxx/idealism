from rich.console import Console
from ascii_art.asciimage import ASCIImage
import os

class App():
    
    def __init__(self):
        self.console = Console()
        self.ascii_image = ASCIImage()
        self.state = None
        self.running = True
        self.last_image = None
        self.current_image = "/home/Tim/Pictures/cowjake.png"

    def _register_states(self):
        self.states["MENU"]=Menu()

    def run(self):
        while self.running:
            if self.current_image != self.last_image:
                for elt in self.ascii_image.img2braille(self.current_image):
                    self.console.print(elt)
                self.last_image = self.current_image
        