import pytest

from pywps import Service
from pywps.tests import assert_response_success

from tests.common import client_for, get_output
from swallow.processes.wps_nameparams import RunNAME


@pytest.mark.online
def test_wps_nameparams_success():
    client = client_for(Service(processes=[RunNAME()]))
    datainputs = 'title={};runBackwards={};time={};elevationOut={};resolution={};startdate={};enddate={};' \
                 'domain={};timestamp={}'.format(
        'CAPEVERDE',
        'true',
        '1',
        '0-100',
        '0.25',
        '2017-11-01',
        '2017-11-02',
        '-180,80,-90,90',
        '3-hourly'
    )
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='runname',
        datainputs=datainputs)
    assert_response_success(resp)

@pytest.mark.skip
def test_wps_nameparams_filename():
    client = client_for(Service(processes=[RunNAME()]))
    datainputs = 'title={};runBackwards={};time={};elevationOut={};resolution={};startdate={};enddate={};' \
                 'domain={};timestamp={}'.format(
        'CAPEVERDE',
        'true',
        '1',
        '0-100',
        '0.25',
        '2017-11-01',
        '2017-11-02',
        '-180,80,-90,90',
        '3-hourly'
    )
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='runname',
        datainputs=datainputs)
    print(get_output(resp.xml))
    assert_response_success(resp)#WIP

#{'runid': 'BCK1_3-hourly_CAPEVERDE_1562579076', 'FileContents': 'file:///tmp/ff31948a-a164-11e9-869f-05df0156c2ef/BCK1_3-hourly_CAPEVERDE_1562579076.zip', 'SummaryPlot': 'file:///tmp/ff31948a-a164-11e9-869f-05df0156c2ef/CAPEVERDE_0-100m_summed_all.png'}