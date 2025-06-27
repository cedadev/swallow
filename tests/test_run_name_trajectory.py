#!/usr/bin/env python

"""Tests for `swallow` package."""

from pywps import Service
from pywps.tests import client_for, assert_response_success

import tempfile
import urllib.parse
import re
import os
import shutil
import glob
from PIL import Image

from .common import get_output, show_tree
from swallow.processes.wps_run_name_trajectory import RunNAMETrajectory



def _get_test_inputs():
    return [
        ('RunDirection', 'Forward'),
        ('RunDuration', '12'),
        ('HeightUnits', 'metres above ground level (m agl)'),
        ('Heights', '100.0'),
        ('Start', '2024-01-01 00:00'),
        ('MetData', 'Global'),
        ('ImageFormat', 'PNG'),
        ('KnownLocation', 'Harwell'),
        ('RunID', 'trajtest'),
        ]


def _get_inputs_string(inputs):
    return ';'.join(f'{k}={urllib.parse.quote_plus(v)}' for k, v in inputs)

def _assert_response_failure(resp):
    assert resp.status_code % 100 != 2

def _get_response(inputs, output_dir=None):

    service_kwargs = {'processes': [RunNAMETrajectory()]}

    if output_dir:
        _, config_file = tempfile.mkstemp(prefix="name.conf.")
        with open(config_file, "w") as fout:
            fout.write(f"[server]\noutputpath={output_dir}\n")
        service_kwargs['cfgfiles'] = config_file

    datainputs = _get_inputs_string(inputs)
    print(f'\ndata inputs: {datainputs}\n')

    client = client_for(Service(**service_kwargs))

    resp = client.get(
        "?service=WPS&request=Execute&version=1.0.0&identifier=NAMERunTrajectory"
        f"&datainputs={datainputs}")

    if output_dir:
        os.remove(config_file)

    return resp
    

def test_wps_run_name_trajectory():
    inputs = _get_test_inputs()
    output_dir = tempfile.mkdtemp()
    resp = _get_response(inputs, output_dir=output_dir)

    try:
        assert_response_success(resp)
        #====================
        # dump some things to stdout:
        #   to see this run pytest with the "-s" option to disable output capture
        #   e.g.   python -m pytest -W ignore -s tests
        show_tree(resp.xml)
        #====================
        outputs = get_output(resp.xml)
        print(outputs)

        message = outputs['message']
        expected_strings = ['description: NAME trajectory run',
                            'image_format: PNG',
                            'known_location: Harwell',
                            'latitude: 51.57',  # this is truncated (substring)
                            'longitude: -1.32', # likewise
                            'met_data: Global',
                            'release_date_time: 2024-01-01 00:00:00',
                            'run_direction: Forward',
                            'run_duration: 12',
                            'run_name: trajtest',
                            'trajectory_height_units: metres above ground level (m agl)',
                            'trajectory_heights: [100.0]']

        for str_ in expected_strings:
            assert str_ in message

        if 'Traceback' in message:
            raise Exception(f"wps response message includes a Traceback: {message}")

        # if trajectory run has completed, expect particle position at end time
        with open(glob.glob(f"{output_dir}/*/Data_Traj_C1_Source1_Particle1.txt")[0]) as trajout:
            for line in trajout:
                if "01/01/2024 00:00:00 UTC,  01/01/2024 12:00:00 UTC" in line:
                    break
            else:
                raise Exception("didn't find expected line in trajectory output file")

        # check that the expected plot exists
        pngfile = glob.glob(f"{output_dir}/*/TrajectoryPlot.png")[0]
        image = Image.open(pngfile)
        assert image.width == 700 and image.height == 900

    finally:
        if "KEEP_OUTPUT" in os.environ:
            print(f"left output in: {output_dir}")
        else:
            print(f"Removing output in {output_dir}.")
            print("Rerun with env var KEEP_OUTPUT set (to anything) to prevent removal.")
            shutil.rmtree(output_dir)

    
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
    
