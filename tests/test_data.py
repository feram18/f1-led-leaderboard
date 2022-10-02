import time

import pytest

from api.data import Data
from constants import UPDATE_RATE


class TestData:
    def setup_method(self):
        self.data = Data()

    @pytest.mark.slow
    def test_should_update(self):
        time.sleep(UPDATE_RATE)
        assert self.data.should_update() is True

    def test_should_update_2(self):
        assert self.data.should_update() is False
