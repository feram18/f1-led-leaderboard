import time
import random
from PIL import Image
from renderer.renderer import Renderer


class Test(Renderer):
    def __init__(self, matrix, canvas, config):
        super().__init__(matrix, canvas, config)
        self.image = Image.new('RGBA', (self.matrix.width, self.matrix.height))

    def render(self):
        self.canvas.Clear()
        self.render_img()
        time.sleep(7.0)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def render_img(self):
        lst = ['assets/img/constructors/alfa.png',
               'assets/img/constructors/red_bull.png',
               'assets/img/constructors/ferrari.png',
               'assets/img/constructors/mclaren.png',
               'assets/img/numbers/max_verstappen.png']
        img = Image.open(random.choice(lst)).convert('RGBA')
        self.image.paste(img, img.size, img)
        print(self.image.size)
        self.canvas.SetImage(self.image.convert('RGB'))

    # def draw_text(self, position, text, font, fill=None, align="left", bg_color=None, bg_offset=[1, 1, 1, 1]):
    #     width = 0
    #     height = 0
    #
    #     text_chars = text.split("\n")
    #     offsets = []
    #
    #     for index, chars in enumerate(text_chars):
    #         spacing = 0 if index == 0 else 1
    #
    #         offset = font.getoffset(chars)
    #         offset_x = offset[0]
    #         offset_y = offset[1] - height - spacing
    #
    #         offsets.append((offset_x, offset_y))
    #
    #         bounding_box = font.getmask(chars).getbbox()
    #         if bounding_box is not None:
    #             width = bounding_box[2] if bounding_box[2] > width else width
    #             height += bounding_box[3] + spacing
    #
    #     width -= 1
    #     height -= 1
    #     size = (width, height)
    #
    #     x, y = self.align_position(align, position, size)
    #
    #     if bg_color is not None:
    #         self.draw_rectangle((x - bg_offset[0], y - bg_offset[1]),
    #                             (width + bg_offset[0] + bg_offset[2], height + bg_offset[1] + bg_offset[3]),
    #                             bg_color)
    #
    #     for index, chars in enumerate(text_chars):
    #         offset = offsets[index]
    #         chars_position = (x - offset[0], y - offset[1])
    #
    #         self.draw.text(chars_position, chars, fill=fill, font=font)
    #
    # def draw_image(self, position, image, align="left"):
    #     position = self.align_position(align, position, image.size)
    #     self.image.paste(image, position, image)
    #
    # def draw_rectangle(self, position, size, color):
    #     self.draw.rectangle([position[0],
    #                          position[1],
    #                          position[0] + size[0],
    #                          position[1] + size[1]],
    #                         fill=color)
    #
    # def align_position(self, align, position, size):
    #     align = align.split("-")
    #     x, y = position
    #
    #     # Handle percentages by converting to pixels
    #     x = self.parse_location(x, self.width)
    #     y = self.parse_location(y, self.height)
    #
    #     if align[0] == "center":
    #         x -= size[0] / 2
    #     elif align[0] == "right":
    #         x -= size[0]
    #
    #     if len(align) > 1:
    #         if align[1] == "center":
    #             y -= size[1] / 2 + 1
    #         elif align[1] == "bottom":
    #             y -= size[1]
    #
    #     if x % 2 == 0:
    #         x = math.ceil(x)
    #     else:
    #         x = math.floor(x)
    #
    #     return round_normal(x), round_normal(y)
