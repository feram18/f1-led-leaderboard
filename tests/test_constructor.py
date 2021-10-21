import logging
from data.constructor import Constructor


class TestConstructor:
    def test_get_logo(self):
        logo_path = Constructor.get_logo('alpine')
        assert isinstance(logo_path, str)

    def test_get_logo_2(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            Constructor.get_logo('invalid')
        assert 'No logo image found for invalid' in caplog.text
