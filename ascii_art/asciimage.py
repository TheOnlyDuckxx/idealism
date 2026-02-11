from PIL import Image
from rich.console import Console


class ASCIImage():
    def __init__(self): 
        self.BRAILLE_MAP = [
            (0, 0, 0x01),
            (0, 1, 0x02),
            (0, 2, 0x04),
            (1, 0, 0x08),
            (1, 1, 0x10),
            (1, 2, 0x20),
            (0, 3, 0x40),
            (1, 3, 0x80),
        ]
        self.image_map = []
        self.braille_map = {}

    def _luminance(self,r,g,b):
        return int(0.299*r+0.587*g+0.114*b)

    def img2braille(self,path,width_chars=75):
        """
            1. Découper l'image en braille 2x4
            2. Pour chaque pixel regarder la luminance et décider l'état du point braille
            3. Transformer le binaire du bloc en un caractere unicode
            4. Choisir la couleur
            5. Afficher ligne par ligne
        """
        if path in self.image_map:
            return self.braille_map[path]
        img = Image.open(path).convert("RGB")
        w,h = img.size
        new_w = width_chars*2
        new_h = int((h/w)*new_w)

        img = img.resize((new_w,new_h))
        px = img.load()

        braille = []

        for y in range(0, new_h, 4):
            line=''
            for x in range(0,new_w, 2):
                code = 0
                rsum = gsum = bsum = 0
                count = 0

                for dx, dy, bit in self.BRAILLE_MAP:
                    if x+dx < new_w and y+dy < new_h:
                        r, g, b = px[x+dx, y+dy]
                        if self._luminance(r,g,b) < 200:
                            code |= bit
                        rsum += r
                        gsum += g
                        bsum += b
                        count += 1

                ch = chr(0x2800 + code)
                r = rsum // count
                g = gsum // count
                b = bsum // count

                line += f"[rgb({r},{g},{b})]{ch}[/]"
            braille.append(line)
        self.image_map.append(path)
        self.braille_map[path] = braille
        return braille
