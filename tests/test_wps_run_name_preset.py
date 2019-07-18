import pytest

from pywps import Service
from pywps.tests import assert_response_success

from tests.common import client_for
from swallow.processes.wps_run_name_preset import RunNAMEPreset


@pytest.mark.online
def test_wps_run_name_preset_success():
    client = client_for(Service(processes=[RunNAMEPreset()]))
    datainputs = 'title={};runBackwards={};time={};elevationOut={};resolution={};startdate={};enddate={}'.format(
        'Cape Verde',
        'true',
        '1',
        '0-100',
        '0.25',
        '2017-11-01',
        '2017-11-02'
    )
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='runnamestd',
        datainputs=datainputs)
    assert_response_success(resp)
