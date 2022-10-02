import logging

from data.circuit import Circuit


class TestCircuit:
    def test_get_logo(self):
        image_path = Circuit.get_logo('americas')
        assert isinstance(image_path, str)

    def test_get_logo_2(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            Circuit.get_logo('invalid')
        assert 'No logo image found for invalid' in caplog.text

    def test_get_track(self):
        image_path = Circuit.get_track('americas')
        assert isinstance(image_path, str)

    def test_get_track_2(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            Circuit.get_track('invalid')
        assert 'No track image found for invalid' in caplog.text
