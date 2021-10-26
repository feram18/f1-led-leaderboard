import pytest
from datetime import datetime, timedelta
from data.grand_prix import GrandPrix
from data.gp_status import GrandPrixStatus


class TestGrandPrix:
    @pytest.mark.skip(reason='Will fail if not on EST timezone')
    def test_convert_time_est(self):
        utc_date, utc_time = '2030-10-04', '12:00:00Z'
        exp_date, exp_time = '2030-10-04', '08:00'  # expected
        est_date, est_time = GrandPrix.convert_time(utc_date, utc_time)  # actual, in EST
        assert (est_date, est_time) == (exp_date, exp_time)

    def test_get_status(self):
        result = GrandPrix.get_status('2031-10-26', '08:00')
        assert result == GrandPrixStatus.UPCOMING

    def test_get_status_2(self):
        time = datetime.now() - timedelta(hours=1)
        result = GrandPrix.get_status(f'{time:%Y-%m-%d}', f'{time:%H:%M}')
        assert result == GrandPrixStatus.IN_PROGRESS

    def test_get_status_3(self):
        time = datetime.now() - timedelta(hours=3)
        result = GrandPrix.get_status(f'{time:%Y-%m-%d}', f'{time:%H:%M}')
        assert result == GrandPrixStatus.FINISHED
