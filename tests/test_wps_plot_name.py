import pytest

from pywps import Service
from pywps.tests import assert_response_success

from tests.common import client_for
from swallow.processes.wps_plot_name import PlotNAME


@pytest.mark.online
def test_wps_plot_name_simple():
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = 'filelocation={}'.format(
        'BCK_3-hourly_CAPEVERDE',
    )
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='PlotNAME',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_timestamp():
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = 'filelocation={};timestamp={}'.format(
        'BCK_3-hourly_CAPEVERDE',
        '2017-11-01 12:00'
    )
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='PlotNAME',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_daysum():
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = 'filelocation={};summarise={}'.format(
        'BCK_3-hourly_CAPEVERDE',
        'day'
    )
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='PlotNAME',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_weeksum():
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = 'filelocation={};summarise={}'.format(
        'BCK_3-hourly_CAPEVERDE',
        'week'
    )
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='PlotNAME',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_monthsum():
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = 'filelocation={};summarise={}'.format(
        'BCK_3-hourly_CAPEVERDE',
        'month'
    )
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='PlotNAME',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_allsum():
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = 'filelocation={};summarise={}'.format(
        'BCK_3-hourly_CAPEVERDE',
        'all'
    )
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='PlotNAME',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_noplotcreated():
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = 'filelocation={};timestamp={}'.format(
        'BCK_3-hourly_CAPEVERDE',
        '2018-05-12 13:00'
    )
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='PlotNAME',
        datainputs=datainputs)
    assert_response_success(resp)
