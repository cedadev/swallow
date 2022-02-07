from pywps import (Process, LiteralInput, LiteralOutput,
                   BoundingBoxInput, BoundingBoxOutput, UOM)
from pywps.app.Common import Metadata
#from pywps.validator.mode import MODE

import datetime
import logging
LOGGER = logging.getLogger("PYWPS")


class RunNAMETrajectory(Process):
    """Run the NAME trajectory model."""
    def __init__(self):

        #-----------------------------------------
        # Note: docs at
        # https://pywps.readthedocs.io/en/latest/api.html
        #
        # and to see allowed values of data_type:
        #   from pywps.inout.literaltypes import LITERAL_DATA_TYPES
        #   print(LITERAL_DATA_TYPES)
        #-----------------------------------------

        inputs = [
            LiteralInput('RunID', 'run identifier',
                         abstract='short text string to describe task',
                         data_type='string',
                         min_occurs=1,
                         max_occurs=1),

            LiteralInput('Description', 'description',
                         abstract='longer text description',
                         data_type='string',
                         min_occurs=0,
                         max_occurs=1),

            LiteralInput('KnownLocation', 'known location',
                         abstract='known location',
                         data_type='string',
                         min_occurs=0,
                         max_occurs=1),
            #(optional): from a list of labelled location

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

            LiteralInput('ReleaseTime', 'release time',
                         abstract='date and time when particles are released',
                         data_type='dateTime',
                         min_occurs=0,
                         max_occurs=1),
            
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
            LiteralOutput('echo', 'Example "echo" output',
                          abstract='This output just gives a string confirming the inputs used.',
                          keywords=['output', 'result', 'response'],
                          data_type='string'),
        ]

        super(RunNAMETrajectory, self).__init__(
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

    @staticmethod
    def _get_input(request, key, multi=False):

        inputs = request.inputs.get(key)

        if inputs == None:
            return None
        
        if multi:
            return [inp.data for inp in inputs]
        else:
            inp, = inputs
            return inp.data
        

    @staticmethod
    def _handler(request, response):
        LOGGER.info("run NAME trajectory")

        # need default value of ReleaseTime (   # default to 00Z on 1st Jan of current year)

        runID = RunNAMETrajectory._get_input(request, 'RunID')
        description = RunNAMETrajectory._get_input(request, 'Description')
        known_location = RunNAMETrajectory._get_input(request, 'KnownLocation')
        latitude = RunNAMETrajectory._get_input(request, 'Latitude')
        longitude = RunNAMETrajectory._get_input(request, 'Longitude')
        release_time = RunNAMETrajectory._get_input(request, 'ReleaseTime')
        run_duration = RunNAMETrajectory._get_input(request, 'RunDuration')
        run_direction = RunNAMETrajectory._get_input(request, 'RunDirection')
        trajectory_heights = RunNAMETrajectory._get_input(request, 'TrajectoryHeights', multi=True)
        trajectory_height_units = RunNAMETrajectory._get_input(request, 'TrajectoryHeightUnits')
        met_data = RunNAMETrajectory._get_input(request, 'MetData')
        notification_email = RunNAMETrajectory._get_input(request, 'NotificationEmail')
        image_format = RunNAMETrajectory._get_input(request, 'ImageFormat')

        if release_time == None:
            year = datetime.datetime.now().year
            release_time = datetime.datetime(year, 1, 1)
        
        response.outputs['echo'].data = (
            f'runID: {runID}, '
            f'description: {description}, '
            f'known_location: {known_location}, '
            f'latitude: {latitude}, '
            f'longitude: {longitude}, '
            f'release_time: {release_time}, '
            f'run_duration: {run_duration}, '
            f'run_direction: {run_direction}, '
            f'trajectory_heights: {trajectory_heights}, '
            f'trajectory_height_units: {trajectory_height_units}, '
            f'met_data: {met_data}, '
            f'notification_email: {notification_email}, '
            f'image_format: {image_format}'
            )

        return response
