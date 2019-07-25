import glob
import pytest

from pywps import Service
from pywps.tests import assert_response_success

from tests.common import client_for, preset_test_inputs, valid_output_file
from swallow.processes.wps_run_name_preset import RunNAMEPreset


@pytest.mark.skip
@pytest.mark.parametrize('inputs', preset_test_inputs)
def test_wps_run_name_preset_inputs_success(inputs):
    client = client_for(Service(processes=[RunNAMEPreset()]))
    datainputs = (
        'title={title};'
        'runBackwards={runBackwards};'
        'time={time};'
        'elevationOut={elevationOut};'
        'resolution={resolution};'
        'startdate={startdate};'
        'enddate={enddate}'
    ).format(**inputs)

    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='run_name_preset',
        datainputs=datainputs)

    assert_response_success(resp)

@pytest.mark.online
def test_wps_run_name_preset_cape_verde_outputs(cape_verde_outputs):
    output_files = glob.glob(f'{cape_verde_outputs}/outputs/*.txt')
    for output in output_files:
        assert valid_output_file(output, 'cape_verde')

@pytest.mark.online
def test_wps_run_name_preset_bt_tower_outputs(bt_tower_outputs):
    output_files = glob.glob(f'{bt_tower_outputs}/outputs/*.txt')
    for output in output_files:
        assert valid_output_file(output, 'bt_tower')
