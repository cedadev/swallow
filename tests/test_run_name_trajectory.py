#!/usr/bin/env python

"""Tests for `swallow` package."""

from pywps import Service
from pywps.tests import client_for, assert_response_success

import urllib.parse
import re

from .common import get_output, show_tree
from swallow.processes.wps_run_name_trajectory import RunNAMETrajectory



def _get_test_inputs():
    return [('RunID', 'myrun'),
            ('RunDuration', '24'),
            ('RunDirection', 'Forward'),
            ('TrajectoryHeights', '10.3'),
            ('TrajectoryHeights', '20.3'),
            ('TrajectoryHeightUnits', 'metres above ground level (m agl)'),
            ('MetData', 'Global'),
            ('ImageFormat', 'PNG')]


def _get_inputs_string(inputs):
    return ';'.join(f'{k}={urllib.parse.quote_plus(v)}' for k, v in inputs)

def _assert_response_failure(resp):
    assert resp.status_code % 100 != 2

def _get_response(inputs):
    client = client_for(Service(processes=[RunNAMETrajectory()]))

    datainputs = _get_inputs_string(inputs)

    print(f'\ndata inputs: {datainputs}\n')

    resp = client.get(
        "?service=WPS&request=Execute&version=1.0.0&identifier=RunNAME1"
        f"&datainputs={datainputs}")

    return resp
    

def test_wps_run_name_trajectory():

    inputs = _get_test_inputs()
    resp = _get_response(inputs)
    assert_response_success(resp)
    #====================
    # dump some things to stdout:
    #   to see this run pytest with the "-s" option to disable output capture
    #   e.g.   python -m pytest -W ignore -s tests
    show_tree(resp.xml)
    #====================
    outputs = get_output(resp.xml)
    print(outputs)

    echo_outputs = outputs['echo']
    ref_outputs = 'runID: myrun, description: None, known_location: None, latitude: None, longitude: None, release_date_time: yyyy-01-01 00:00:00, run_duration: 24, run_direction: Forward, trajectory_heights: [10.3, 20.3], trajectory_height_units: metres above ground level (m agl), met_data: Global, notification_email: None, image_format: PNG'
    print(f'Comparing:\n   {echo_outputs}\n   {ref_outputs}')    
    assert re.sub('20\d{2}-01-01', 'yyyy-01-01', echo_outputs) == ref_outputs

    
def test_wps_run_name_trajectory_missing_compulsory_input():
    inputs = _get_test_inputs()
    inputs = [(k, v) for k, v in inputs if k != 'RunDuration']
    resp = _get_response(inputs)
    _assert_response_failure(resp)
    

def test_wps_run_name_trajectory_with_disallowed_value():
    inputs = _get_test_inputs()
    inputs = [(k, v if k != 'RunDuration' else '26') for k, v in inputs]
    resp = _get_response(inputs)
    _assert_response_failure(resp)
    
