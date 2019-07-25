import pytest

from pywps import Service
from pywps.tests import assert_response_success

from tests.common import client_for, get_valid_date, get_invalid_date
from swallow.processes.wps_plot_name import PlotNAME


# Cape verde plots
@pytest.mark.online
def test_wps_plot_name_simple_cape_verde(cape_verde_outputs):
    run_id = cape_verde_outputs.split('/')[-1]
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_timestamp_cape_verde(cape_verde_outputs):
    run_id = cape_verde_outputs.split('/')[-1]
    timestamp = get_valid_date('cape_verde')
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};timestamp={timestamp}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_daysum_cape_verde(cape_verde_outputs):
    run_id = cape_verde_outputs.split('/')[-1]
    time_summary = 'day'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_weeksum_cape_verde(cape_verde_outputs):
    run_id = cape_verde_outputs.split('/')[-1]
    time_summary = 'week'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_monthsum_cape_verde(cape_verde_outputs):
    run_id = cape_verde_outputs.split('/')[-1]
    time_summary = 'month'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_allsum_cape_verde(cape_verde_outputs):
    run_id = cape_verde_outputs.split('/')[-1]
    time_summary = 'all'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_noplotcreated_cape_verde(cape_verde_outputs):
    run_id = cape_verde_outputs.split('/')[-1]
    timestamp = get_invalid_date('cape_verde')
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};timestamp={timestamp}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


# BT Tower plots
@pytest.mark.online
def test_wps_plot_name_simple_bt_tower(bt_tower_outputs):
    run_id = bt_tower_outputs.split('/')[-1]
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_timestamp_bt_tower(bt_tower_outputs):
    run_id = bt_tower_outputs.split('/')[-1]
    timestamp = get_valid_date('bt_tower')
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};timestamp={timestamp}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_daysum_bt_tower(bt_tower_outputs):
    run_id = bt_tower_outputs.split('/')[-1]
    time_summary = 'day'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_weeksum_bt_tower(bt_tower_outputs):
    run_id = bt_tower_outputs.split('/')[-1]
    time_summary = 'week'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_monthsum_bt_tower(bt_tower_outputs):
    run_id = bt_tower_outputs.split('/')[-1]
    time_summary = 'month'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_allsum_bt_tower(bt_tower_outputs):
    run_id = bt_tower_outputs.split('/')[-1]
    time_summary = 'all'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_noplotcreated_bt_tower(bt_tower_outputs):
    run_id = bt_tower_outputs.split('/')[-1]
    timestamp = get_invalid_date('bt_tower')
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};timestamp={timestamp}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


# Custom Tokyo plots
@pytest.mark.online
def test_wps_plot_name_simple_custom_tokyo(custom_tokyo_outputs):
    run_id = custom_tokyo_outputs.split('/')[-1]
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_timestamp_custom_tokyo(custom_tokyo_outputs):
    run_id = custom_tokyo_outputs.split('/')[-1]
    timestamp = get_valid_date('custom_tokyo')
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};timestamp={timestamp}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_daysum_custom_tokyo(custom_tokyo_outputs):
    run_id = custom_tokyo_outputs.split('/')[-1]
    time_summary = 'day'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_weeksum_custom_tokyo(custom_tokyo_outputs):
    run_id = custom_tokyo_outputs.split('/')[-1]
    time_summary = 'week'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_monthsum_custom_tokyo(custom_tokyo_outputs):
    run_id = custom_tokyo_outputs.split('/')[-1]
    time_summary = 'month'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_allsum_custom_tokyo(custom_tokyo_outputs):
    run_id = custom_tokyo_outputs.split('/')[-1]
    time_summary = 'all'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_noplotcreated_custom_tokyo(custom_tokyo_outputs):
    run_id = custom_tokyo_outputs.split('/')[-1]
    timestamp = get_invalid_date('custom_tokyo')
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};timestamp={timestamp}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


# Custom Egypt verde plots
@pytest.mark.online
def test_wps_plot_name_simple_custom_egypt(custom_egypt_outputs):
    run_id = custom_egypt_outputs.split('/')[-1]
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_timestamp_custom_egypt(custom_egypt_outputs):
    run_id = custom_egypt_outputs.split('/')[-1]
    timestamp = get_valid_date('custom_egypt')
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};timestamp={timestamp}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_daysum_custom_egypt(custom_egypt_outputs):
    run_id = custom_egypt_outputs.split('/')[-1]
    time_summary = 'day'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_weeksum_custom_egypt(custom_egypt_outputs):
    run_id = custom_egypt_outputs.split('/')[-1]
    time_summary = 'week'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_monthsum_custom_egypt(custom_egypt_outputs):
    run_id = custom_egypt_outputs.split('/')[-1]
    time_summary = 'month'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_allsum_custom_egypt(custom_egypt_outputs):
    run_id = custom_egypt_outputs.split('/')[-1]
    time_summary = 'all'
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};summarise={time_summary}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)


@pytest.mark.online
def test_wps_plot_name_noplotcreated_custom_egypt_outputs(custom_egypt_outputs):
    run_id = custom_egypt_outputs.split('/')[-1]
    timestamp = get_invalid_date('custom_egypt')
    client = client_for(Service(processes=[PlotNAME()]))
    datainputs = f'filelocation={run_id};timestamp={timestamp}'
    resp = client.get(
        service='wps', request='execute', version='1.0.0',
        identifier='plot_name',
        datainputs=datainputs)
    assert_response_success(resp)
