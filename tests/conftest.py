import pytest

from pywps import Service
from pywps.tests import assert_response_success

from tests.common import client_for, get_outputs_path, cape_verde_inputs, bt_tower_inputs, custom_tokyo_inputs, custom_egypt_inputs
from swallow.processes.wps_run_name import RunNAME
from swallow.processes.wps_run_name_preset import RunNAMEPreset



@pytest.fixture(scope='session')
def cape_verde_outputs():
    client = client_for(Service(processes=[RunNAMEPreset()]))
    datainputs = (
        'title={title};'
        'runBackwards={runBackwards};'
        'time={time};'
        'elevationOut={elevationOut};'
        'resolution={resolution};'
        'startdate={startdate};'
        'enddate={enddate}'
    ).format(**cape_verde_inputs)

    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='run_name_preset',
        datainputs=datainputs)

    yield get_outputs_path(resp.xml)

@pytest.fixture(scope='session')
def bt_tower_outputs():
    client = client_for(Service(processes=[RunNAMEPreset()]))
    datainputs = (
        'title={title};'
        'runBackwards={runBackwards};'
        'time={time};'
        'elevationOut={elevationOut};'
        'resolution={resolution};'
        'startdate={startdate};'
        'enddate={enddate}'
    ).format(**bt_tower_inputs)

    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='run_name_preset',
        datainputs=datainputs)

    yield get_outputs_path(resp.xml)

@pytest.fixture(scope='session')
def custom_tokyo_outputs():
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
    ).format(**custom_tokyo_inputs)

    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='run_name',
        datainputs=datainputs)

    yield get_outputs_path(resp.xml)

@pytest.fixture(scope='session')
def custom_egypt_outputs():
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
    ).format(**custom_egypt_inputs)

    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='run_name',
        datainputs=datainputs)

    yield get_outputs_path(resp.xml)
