import glob
import pytest

from pywps import Service
from pywps.tests import assert_response_success

from tests.common import client_for, custom_test_inputs, valid_output_file
from swallow.processes.wps_run_name import RunNAME


@pytest.mark.skip
@pytest.mark.parametrize('inputs', custom_test_inputs)
def test_wps_run_name_inputs_success(inputs):
    client = client_for(Service(processes=[RunNAME()]))
    datainputs = (
        'title={title};'
        'longitude={longitude};'
        'latitude={latitude};'
        'runBackwards={runBackwards};'
        'time={time};'
        'elevationOut={elevationOut};'
        'resolution={resolution};'
        'startdate={startdate};'
        'enddate={enddate};'
        'min_lon={min_lon};'
        'max_lon={max_lon};'
        'min_lat={min_lat};'
        'max_lat={max_lat};'
        'timestamp={timestamp}'
    ).format(**inputs)

    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='run_name',
        datainputs=datainputs)
    assert_response_success(resp)

@pytest.mark.online
def test_wps_run_name_tokyo_outputs(custom_tokyo_outputs):
    output_files = glob.glob(f'{custom_tokyo_outputs}/outputs/*.txt')
    for output in output_files:
        assert valid_output_file(output, 'custom_tokyo')
        
@pytest.mark.online
def test_wps_run_name_egypt_outputs(custom_egypt_outputs):
    output_files = glob.glob(f'{custom_egypt_outputs}/outputs/*.txt')
    for output in output_files:
        assert valid_output_file(output, 'custom_egypt')
