import pytest
from datetime import datetime, timedelta
from data.grand_prix import GrandPrix


class TestGrandPrix:
    @pytest.mark.skip
    def test_convert_time(self):
        utc_date, utc_time = '2021-10-04', '12:00:00Z'
        exp_date, exp_time = '2021-10-04', '08:00'  # expected
        est_date, est_time = GrandPrix.convert_time(utc_date, utc_time)  # actual
        assert (est_date, est_time) == (exp_date, exp_time)

    def test_in_progress(self):
        result = GrandPrix.in_progress('2021-10-04', '08:00')
        assert result is False

    def test_in_progress_2(self):
        time = datetime.now() - timedelta(hours=1)
        result = GrandPrix.in_progress(f'{time:%Y-%m-%d}', f'{time:%H:%M}')
        assert result is True
