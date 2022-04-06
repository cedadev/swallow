from pywps import LiteralInput

from .name_base_process import NAMEBaseProcess
from .create_name_inputs.make_traj_input import main as make_traj_input


class RunNAMETrajectory(NAMEBaseProcess):
    """Run the NAME trajectory model."""

    _description = "run NAME trajectory"
    
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
            
            self._get_run_id_process_input(),
            self._get_description_process_input(),
            self._get_latitude_process_input(),
            self._get_longitude_process_input(),
            self._get_known_location_process_input(),
        ] + self._get_start_date_time_process_inputs() + [
            self._get_run_duration_process_input(),
            
            LiteralInput('RunDirection', 'run direction',
                         abstract='whether to run forward or backward trajectories',
                         data_type='string',
                         allowed_values=['Forward', 'Backward'],
                         min_occurs=1,
                         max_occurs=1),

            self._get_trajectory_heights_process_input(),
            self._get_height_units_process_input(),
            self._get_met_data_process_input(),
            self._get_notification_email_process_input(),
            self._get_image_format_process_input(),
            
        ]
        outputs = [
            self._get_inputs_process_output(),
            self._get_message_process_output(),
        ]

        super().__init__(
            self._handler,
            identifier='NAMERunTrajectory',
            title='Run NAME Trajectory',
            abstract=('A forwards or backwards run of the NAME model outputting '
                      'particle trajectories following the mean flow only.'),
            keywords=self._keywords,
            metadata=self._metadata,
            version=self._version,
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    
    def _get_processed_inputs(self, request):
        """
        returns dictionary of inputs, some of which are used raw, 
        while others need some processing
        """
        runID = self._get_input(request, 'RunID')
        known_location = self._get_input(request, 'KnownLocation')
        latitude = self._get_input(request, 'Latitude')
        longitude = self._get_input(request, 'Longitude')
        trajectory_heights = self._get_input(request, 'TrajectoryHeights', multi=True)
        release_date_time = self._get_start_date_time(request)

        if known_location != None and known_location != self._null_label:
            longitude, latitude = self._stations[known_location]

        return {
            'description': self._get_input(request, 'Description',
                                           default='NAME trajectory run'),
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
            'trajectory_height_units': self._get_input(request, 'HeightUnits'),
        }


    def _handler_backend(self, *args):
        return make_traj_input(*args)
