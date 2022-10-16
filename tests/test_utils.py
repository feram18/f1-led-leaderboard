import logging
import sys
from datetime import datetime, timedelta

import pytest
from PIL import Image, ImageFont

import utils
from data.session_status import SessionStatus


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestUtils:
    def setup_method(self):
        self.font = utils.load_font('assets/fonts/tom-thumb.bdf')

    def test_read_json(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            utils.read_json('invalid.json')
        assert "Couldn't find file at invalid.json" in caplog.text

    def test_load_font(self):
        assert isinstance(self.font, ImageFont.ImageFont)

    def test_load_font_2(self):
        assert self.font.getsize('A')[0], 4

    def test_load_font_3(self):
        assert self.font.getsize('A')[1], 6

    def test_load_font_4(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            utils.load_font('invalid.bdf')
        assert f"Couldn't find font invalid.bdf" in caplog.text

    def test_load_image(self):
        image = utils.load_image('assets/img/error.png', (15, 15))
        assert isinstance(image, Image.Image)

    def test_load_image_2(self):
        image = utils.load_image('assets/img/error.png', (15, 15))
        assert image.size <= (15, 15)

    def test_load_image_5(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            utils.load_image('invalid.jpg', (15, 15))
        assert f"Couldn't find image invalid.jpg" in caplog.text

    def test_load_image_6(self):
        image = utils.load_image('invalid.jpg', (15, 15))
        assert image is None

    def test_align_text(self):
        x, y = utils.align_text(self.font.getsize('Lorem ipsum'), 64, 32, utils.Position.CENTER, utils.Position.CENTER)
        assert (x, y) == (11, 13)

    def test_align_text_2(self):
        x = utils.align_text(self.font.getsize('Lorem ipsum'), col_width=64, x=utils.Position.RIGHT)[0]
        assert x == 22

    def test_align_text_3(self):
        x = utils.align_text(self.font.getsize('Lorem ipsum'), col_height=32, y=utils.Position.BOTTOM)[0]
        assert x == 21

    def test_align_image(self):
        img = utils.load_image('assets/img/error.png', (15, 15))
        x, y = utils.align_image(img, 64, 32, utils.Position.CENTER, utils.Position.CENTER)
        assert (x, y) == (25, 10)

    def test_align_image_2(self):
        img = utils.load_image('assets/img/error.png', (15, 15))
        x = utils.align_image(img, col_width=64, x=utils.Position.CENTER)[0]
        assert x == 25

    def test_align_image_3(self):
        img = utils.load_image('assets/img/error.png', (15, 15))
        y = utils.align_image(img, col_height=32, y=utils.Position.CENTER)[1]
        assert y == 10

    @pytest.mark.skip(reason='Will fail if not on EST timezone')
    def test_convert_time_est(self):
        utc_date, utc_time = '2030-10-04', '12:00:00Z'
        exp_date, exp_time = '2030-10-04', '08:00'  # expected
        est_date, est_time = utils.convert_time(utc_date, utc_time)  # actual, in EST
        assert (est_date, est_time) == (exp_date, exp_time)

    def test_get_session_status(self):
        time = datetime.now().replace(year=2031, month=10, day=26, hour=8, minute=0).astimezone(tz=None)
        result = utils.get_session_status(time)
        assert result == SessionStatus.UPCOMING

    def test_get_session_status_2(self):
        time = datetime.now().astimezone(tz=None) - timedelta(hours=1)
        result = utils.get_session_status(time)
        assert result == SessionStatus.IN_PROGRESS

    def test_get_session_status_3(self):
        time = datetime.now().astimezone(tz=None) - timedelta(hours=3)
        result = utils.get_session_status(time)
        assert result == SessionStatus.FINISHED
