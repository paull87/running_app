import pytest
import os
from decimal import Decimal
from VDOT.VDOT import VDOT
from settings.database import DB


@pytest.fixture()
def database(tmpdir):
    return DB(os.path.join(tmpdir, 'db.db'))


def test_calculate_vdot_1500(database):
    vdot = VDOT(database)
    vdot.calculate_vdot('1500', '00:02:39')
    assert vdot.vdot_score == Decimal('85')


def test_calculate_vdot_mile(database):
    vdot = VDOT(database)
    vdot.calculate_vdot('Mile', '00:37:39')
    assert vdot.vdot_score == Decimal('30')


def test_calculate_vdot_2mile(database):
    vdot = VDOT(database)
    vdot.calculate_vdot('2Mile', '00:18:39')
    assert vdot.vdot_score == Decimal('31.3')


def test_calculate_vdot_3000(database):
    vdot = VDOT(database)
    vdot.calculate_vdot('3000', '00:12:40')
    assert vdot.vdot_score == Decimal('45')


def test_calculate_vdot_5000(database):
    vdot = VDOT(database)
    vdot.calculate_vdot('5000', '00:21:40')
    assert vdot.vdot_score == Decimal('45.4')


def test_calculate_vdot_10k(database):
    vdot = VDOT(database)
    vdot.calculate_vdot('10K', '00:41:40')
    assert vdot.vdot_score == Decimal('49.55')


def test_calculate_vdot_15k(database):
    vdot = VDOT(database)
    vdot.calculate_vdot('15K', '01:00:40')
    assert vdot.vdot_score == Decimal('52.8')


def test_calculate_vdot_10mile(database):
    vdot = VDOT(database)
    vdot.calculate_vdot('10Mile', '01:10:00')
    assert vdot.vdot_score == Decimal('48.75')


def test_calculate_vdot_half_marathon(database):
    vdot = VDOT(database)
    vdot.calculate_vdot('HalfMarathon', '01:37:39')
    assert vdot.vdot_score == Decimal('46.44')


def test_calculate_vdot_marathon(database):
    vdot = VDOT(database)
    vdot.calculate_vdot('Marathon', '03:37:39')
    assert vdot.vdot_score == Decimal('42.72')


def test_save_vdot(database):
    vdot = VDOT(database)
    vdot.calculate_vdot('Marathon', '03:37:39')
    vdot.save_vdot()
    current_settings = database.get_current_settings()
    assert vdot.vdot_score == Decimal(str(current_settings[2]))
