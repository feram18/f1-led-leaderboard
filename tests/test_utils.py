import pytest
import sys
import logging
import PIL
import rgbmatrix
import utils


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestUtils:
    def test_read_json(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            utils.read_json('invalid.json')
        assert "Couldn't find file at invalid.json" in caplog.text

    def test_load_font(self):
        font = utils.load_font('rpi-rgb-led-matrix/fonts/5x7.bdf')
        assert isinstance(font, rgbmatrix.graphics.Font)

    def test_load_font_2(self):
        font = utils.load_font('rpi-rgb-led-matrix/fonts/5x7.bdf')
        assert font.baseline, 6

    def test_load_font_3(self):
        font = utils.load_font('rpi-rgb-led-matrix/fonts/5x7.bdf')
        assert font.height, 7

    def test_load_font_4(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            utils.load_font('invalid.bdf')
        assert f"Couldn't find font invalid.bdf. Setting font to default 4x6." in caplog.text

    def test_load_font_5(self):
        font = utils.load_font('invalid.bdf')
        assert isinstance(font, rgbmatrix.graphics.Font)

    def test_load_font_6(self):
        font = utils.load_font('invalid.bdf')
        assert font.baseline == 5

    def test_load_font_7(self):
        font = utils.load_font('invalid.bdf')
        assert font.height == 6

    def test_load_image(self):
        image = utils.load_image('assets/img/error.jpg', (15, 15))
        assert isinstance(image, PIL.Image.Image)

    def test_load_image_2(self):
        image = utils.load_image('assets/img/error.jpg', (15, 15))
        assert image.size <= (15, 15)

    def test_load_image_3(self):
        image = utils.load_image('assets/img/error.jpg')
        assert isinstance(image, PIL.Image.Image)

    def test_load_image_4(self):
        image = utils.load_image('assets/img/error.jpg')
        assert image.size <= (64, 32)

    def test_load_image_5(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            utils.load_image('invalid.jpg')
        assert f"Couldn't find image invalid.jpg" in caplog.text

    def test_load_image_6(self):
        image = utils.load_image('invalid.jpg')
        assert image is None

    def test_center_image(self):
        x, y = utils.center_image((28, 28), 64, 32)
        assert (x, y) == (18, 2)

    def test_center_image_2(self):
        x, y = utils.center_image((28, 0), canvas_width=64)
        assert (x, y) == (18, 0)

    def test_center_image_3(self):
        x, y = utils.center_image((0, 28), canvas_height=32)
        assert (x, y) == (0, 2)

    def test_align_text_center(self):
        x, y = utils.align_text_center('Lorem ipsum', 64, 32, 4, 6)
        assert (x, y) == (10, 19)

    def test_align_text_center_2(self):
        x, y = utils.align_text_center('Lorem ipsum', canvas_width=64, font_width=4)
        assert (x, y) == (10, 0)

    def test_align_text_center_3(self):
        x, y = utils.align_text_center('Lorem ipsum', canvas_height=32, font_height=6)
        assert (x, y) == (0, 19)

    def test_align_text_center_4(self):
        x, y = utils.align_text_center('Lorem ipsum')
        assert (x, y) == (0, 0)

    def test_split_into_pages(self):
        lst = [0, 1, 2, 5, 7, 9, 13]
        n = 2
        pages = utils.split_into_pages(lst, n)
        assert len(pages) == 7
