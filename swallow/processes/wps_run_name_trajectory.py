from pywps import LiteralInput

from ._name_base_process import NAMEBaseProcess
from .create_name_inputs.make_traj_input import main as make_traj_input
from ._util import lon_to_str, lat_to_str


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
            
            LiteralInput('RunDirection', 'Run Direction',
                         abstract='whether to run forward or backward trajectories',
                         data_type='string',
                         allowed_values=['Forward', 'Backward'],
                         min_occurs=1,
                         max_occurs=1),

            self._get_heights_process_input('Trajectory Heights'),
            self._get_height_units_process_input(),
            self._get_met_data_process_input(),
            self._get_notification_email_process_input(),
            self._get_image_format_process_input(),
            
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
            store_supported=True,
            status_supported=True,
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
        trajectory_heights = self._get_input(request, 'Heights', multi=True)
        release_date_time = self._get_start_date_time(request)

        if known_location != None and known_location != self._null_label:
            longitude, latitude = self._stations[known_location]

        return {
            'description': self._get_input(request, 'Description',
                                           default='NAME trajectory run'),
            'known_location': known_location,
            'longitude': longitude,
            'latitude': latitude,
            'trajectory_heights': trajectory_heights,
            'run_duration': self._get_input(request, 'RunDuration'),
            'run_direction': self._get_input(request, 'RunDirection'),
            'met_data': self._get_input(request, 'MetData'), 
            'run_name': runID,
            'release_date_time': release_date_time,

            # used by _get_adaq_scripts_and_args
            'image_format': self._get_input(request, 'ImageFormat'),

            # the following inputs are currently unused
            'notification_email': self._get_input(request, 'NotificationEmail'),
            'trajectory_height_units': self._get_input(request, 'HeightUnits'),
        }


    def _make_name_input(self, *args):
        return make_traj_input(*args)


    def _get_adaq_scripts_and_args(self, input_params, outputs_dir, plots_dir, image_extension):

        location = input_params['known_location']
        site = f'"{location}"' if location not in (None, self._null_label) else None
        plot_trajectory_ini_contents = f'''
# plot configuration file for plotting NAME particle trajectories

models_dir_list = ["{outputs_dir}/Data_Traj_C1_*.txt"]
plot_dir        = "{plots_dir}"

marker_interval = 3  # Marker interval in hours
title = "{input_params['description']}"
plotname = 'TrajectoryPlot.{image_extension}'
mo_branding = False
release_info_list = [ {site} ]
mapping = 'countries'
'''
        plot_traj_args = [self._make_work_file(plot_trajectory_ini_contents, 'plot_trajectory.ini')]
        
        return [
            ('plot_trajectory.py', plot_traj_args),
        ]
