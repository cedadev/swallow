import pytest

from pywps import Service
from pywps.tests import assert_response_success

from tests.common import client_for
from swallow.processes.wps_nameparams import RunNAME


@pytest.mark.online
def test_wps_nameparams():
    client = client_for(Service(processes=[RunNAME()]))
    datainputs = "title={};runBackwards={};time={};elevationOut={};resolution={};startdate={};enddate={};" \
                 "domain={};timestamp={}".format(
        "CAPEVERDE",
        "true",
        "1",
        "0-100",
        "0.25",
        "2017-11-01",
        "2017-11-02",
        "-180,80,-90,90",
        "3-hourly"
    )
    print(datainputs)
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='runname',
        datainputs=datainputs)
    print("data")
    print(resp.data)
    print("xml")
    print(resp.xml)
    assert_response_success(resp)
