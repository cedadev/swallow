from pywps import (Process, LiteralInput, LiteralOutput,
                   BoundingBoxInput, BoundingBoxOutput, UOM)
from pywps.app.Common import Metadata

from .create_name_inputs.make_traj_input import main as make_traj_input
#from pywps.validator.mode import MODE

import os
import datetime
import logging
LOGGER = logging.getLogger("PYWPS")



_stations = {
    'Auchencorth Moss': (-3.347222328, 55.88333511),
    'BT Tower (150m)': (-0.13888, 51.5215),
    'Bachok: (Malaysia)': (102.425, 6.009),
    'Beijing Pinggu': (117.0406996, 40.1659),
    'Beijing Tower': (116.377, 39.975),
    'Cape Fuguei (Taiwan)': (121.538, 25.297),
    'Cape Verde': (-24.867222, 16.863611),
    'Chilbolton Observatory': (-1.438228000, 51.14961700),
    'Coyhaique': (-72.049977,  -45.578936),
    'Delhi (Kashmere gate)': (77.23184, 28.6644),
    'Halley': (26.16667, -75.58333),
    'Hanoi (Vietnam)': (105.4902, 21.0024),
    'Harwell': (-1.326666594, 51.57110977),
    'Ho Chi Minh City (Vietnam)': (106.4057, 10.4544),
    'Mace Head': (-9.938888550, 53.41388702),
    'North Kensington': (-0.213333338, 51.52111053),
    'Penlee (PML)': (-4.1931, 50.3189),
    'Weybourne': (1.1219, 52.9503)
}


class RunNAMETrajectory(Process):
    """Run the NAME trajectory model."""

    _null_label = '(none)'

    def __init__(self):

        #-----------------------------------------
        # Note: docs at
        # https://pywps.readthedocs.io/en/latest/api.html
        #
        # and to see allowed values of data_type:
        #   from pywps.inout.literaltypes import LITERAL_DATA_TYPES
        #   print(LITERAL_DATA_TYPES)
        #-----------------------------------------

        current_year = datetime.datetime.now().year

        inputs = [
            LiteralInput('RunID', 'run identifier',
                         abstract='* short text string to describe task',
                         data_type='string',
                         min_occurs=1,
                         max_occurs=1),

            LiteralInput('Description', 'description',
                         abstract='longer text description',
                         data_type='string',
                         min_occurs=0,
                         max_occurs=1),

            LiteralInput('Latitude', 'latitude',
                         abstract='latitude of trajectory start/end-point',
                         data_type='float',
                         min_occurs=0,
                         max_occurs=1),
            
            LiteralInput('Longitude', 'longitude',
                         abstract='longitude of trajectory start/end-point',
                         data_type='float',
                         min_occurs=0,
                         max_occurs=1),

            LiteralInput('KnownLocation', 
                         'standard location name (alternative to lon/lat)',
                         abstract='known location',
                         data_type='string',
                         min_occurs=0,
                         max_occurs=1,
                         allowed_values=[self._null_label] + sorted(_stations.keys())),
            LiteralInput('ReleaseDate', 'release date',
                         abstract='* date when particles are released (enter as yyyy-mm-dd or yyyymmdd format)',
                         data_type='date',
                         min_occurs=1,
                         max_occurs=1,
                         default=f'{current_year}-01-01'),

            LiteralInput('ReleaseTime', 'release time',
                         abstract='* time when particles are released (enter as hh:mm or hh:mm:ss format)',
                         data_type='time',
                         min_occurs=1,
                         max_occurs=1,
                         default='00:00'),
            
            LiteralInput('RunDuration', 'run duration',
                         abstract='duration of trajectory run, in hours',
                         data_type='integer',
                         allowed_values=[12, 24, 36, 48, 72, 96, 120, 144, 168, 240, 360, 480],
                         min_occurs=1,
                         max_occurs=1),

            LiteralInput('RunDirection', 'run direction',
                         abstract='whether to run forward or backward trajectories',
                         data_type='string',
                         allowed_values=['Forward', 'Backward'],
                         min_occurs=1,
                         max_occurs=1),

            LiteralInput('TrajectoryHeights', 'trajectory heights',
                         abstract='array of start/end heights of particles',
                         data_type='float',
                         min_occurs=1,
                         max_occurs=999,
                         ),

            LiteralInput('TrajectoryHeightUnits', 'trajectory height units',
                         abstract='units for the TrajectoryHeights array',
                         data_type='string',
                         allowed_values=['metres above ground level (m agl)', 'metres above sea level (m asl)'],
                         min_occurs=1,
                         max_occurs=1),

            LiteralInput('MetData', 'met data',
                         abstract='which forcing dataset to use to drive the trajectory model',
                         data_type='string',
                         allowed_values=["Global", "UK 1.5km", "Global + UK 1.5km"],
                         min_occurs=1,
                         max_occurs=1),

            LiteralInput('NotificationEmail', 'notification email',
                         abstract='which email address to send notifications to',
                         data_type='string',
                         min_occurs=0,
                         max_occurs=1),

            LiteralInput('ImageFormat', 'image format',
                         abstract='format of output image file',
                         data_type='string',
                         default='PNG',
                         allowed_values=['PNG', 'JPG', 'PDF'],
                         min_occurs=1,
                         max_occurs=1),
            
        ]
        outputs = [
            LiteralOutput('inputs', 'Copy of inputs',
                          abstract='This output just gives a string confirming the inputs used.',
                          keywords=['output', 'result', 'response'],
                          data_type='string'),

            LiteralOutput('message', 'Status message',
                          abstract='This output gives a response from the job submission process.',
                          keywords=['output', 'result', 'response'],
                          data_type='string'),
        ]

        super().__init__(
            self._handler,
            identifier='RunNAME1',
            title='Run NAME Trajectory',
            abstract='A forwards or backwards run of the NAME model outputting particle trajectories following the mean flow only.',
            keywords=["name", "model", "atmospheric", "dispersion", "trajectory", "forward", "backward", "air", "pollution", "transport"],
            metadata=[
                Metadata('PyWPS', 'https://pywps.org/'),
                Metadata('Birdhouse', 'http://bird-house.github.io/'),
                Metadata('PyWPS Demo', 'https://pywps-demo.readthedocs.io/en/latest/'),
                Metadata('Emu: PyWPS examples', 'https://emu.readthedocs.io/en/latest/'),
            ],
            version='1.5',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )


    def _get_input(self, request, key, multi=False, default=None):

        inputs = request.inputs.get(key)

        if inputs == None:
            return default
        
        if multi:
            return [inp.data for inp in inputs]
        else:
            inp, = inputs
            return inp.data

    
    def _get_processed_inputs(self, request):
        """
        returns dictionary of inputs, some of which are used raw, 
        while others need some processing
        """
        runID = self._get_input(request, 'RunID')
        known_location = self._get_input(request, 'KnownLocation')
        latitude = self._get_input(request, 'Latitude')
        longitude = self._get_input(request, 'Longitude')
        release_date = self._get_input(request, 'ReleaseDate')
        release_time = self._get_input(request, 'ReleaseTime')
        trajectory_heights = self._get_input(request, 'TrajectoryHeights', multi=True)

        release_date_time = datetime.datetime(release_date.year,
                                              release_date.month,
                                              release_date.day,
                                              release_time.hour,
                                              release_time.minute,
                                              release_time.second)

        if known_location != None and known_location != self._null_label:
            longitude, latitude = _stations[known_location]

        return {
            'jobTitle': self._get_input(request, 'Description', default='NAME trajectory run'),
            'known_location': known_location,
            'longitude': longitude,
            'latitude': latitude,
            'trajectory_heights': self._get_input(request, 'TrajectoryHeights', multi=True),
            'run_duration': self._get_input(request, 'RunDuration'),
            'run_direction': self._get_input(request, 'RunDirection'),
            'met_data': self._get_input(request, 'MetData'), 
            'run_name': runID,
            'release_date_time': release_date_time,

            # the following inputs are unused by make_traj_input
            'notification_email': self._get_input(request, 'NotificationEmail'),
            'image_format': self._get_input(request, 'ImageFormat'),
            'trajectory_height_units': self._get_input(request, 'TrajectoryHeightUnits'),
        }
        

    def _get_request_internal_id(self):
        # FIXME: is there any kind of request ID in the request? 
        # (I didn't find one.)
        return f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{os.getpid()}'


    def _handler(self, request, response):
        LOGGER.info("run NAME trajectory")

        internal_run_id = self._get_request_internal_id()
        input_params = self._get_processed_inputs(request)
        msg = make_traj_input(internal_run_id, input_params)
        response.outputs['message'].data = msg

        d = input_params
        response.outputs['inputs'].data = ', '.join(f'{k}: {d[k]}'
                                                    for k in sorted(d))

        # uncomment to show inputs in UI
        response.outputs['message'].data += f' INPUTS: {response.outputs["inputs"].data}'
        
        return response
