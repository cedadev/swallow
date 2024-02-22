from pywps import LiteralInput
from pywps.app.exceptions import ProcessError

from ._name_base_process import NAMEBaseProcess
from .create_name_inputs.make_air_history_input \
    import main as make_air_history_input


class AirHistoryRun(NAMEBaseProcess):
    """Run the NAME model in air history mode."""

    _description = "run the NAME model in air history mode"
    
    def __init__(self):

        inputs = [
            self._get_run_id_process_input(),
            self._get_description_process_input(),
            self._get_latitude_process_input(),
            self._get_longitude_process_input(),
            self._get_known_location_process_input(),
            
            LiteralInput('ArrivalBottom', 'Arrival Bottom',
                         abstract='height at the bottom of the arrival region',
                         data_type='float',
                         default=0.,
                         min_occurs=1,
                         max_occurs=1),

            LiteralInput('ArrivalTop', 'Arrival Top',
                         abstract='height at the top of the arrival region',
                         data_type='float',
                         default=500.,
                         min_occurs=1,
                         max_occurs=1),

            self._get_start_datetimestr_process_input(),
            self._get_run_duration_process_input(),
            
            self._get_datetimestr_process_input('ArrivalStart', 'Arrival Start [if not start of run]:',
                                                'start of arrival period',
                                                optional=True, add_abstract=' - leave blank to use start of run'),
            self._get_datetimestr_process_input('ArrivalStop', 'Arrival Stop [if not end of run]:',
                                                'end of arrival period [NOTE: EARLIER than ArrivalStart, as backwards-running model]',
                                                optional=True, add_abstract=' - leave blank to use end of run'),
                                                    
        ] + self._get_output_horiz_grid_process_inputs() + [
            self._get_halo_process_input(),
            self._get_heights_process_input('Grid Levels'),
            self._get_height_units_process_input(),
            self._get_met_data_process_input(),
            self._get_timestamp_process_input(),
        
            #self._get_notification_email_process_input(),
            self._get_image_format_process_input(),
        ]
        
        super().__init__(
            self._handler,
            identifier='NAMEAirHistory',
            title='Air History Run',
            abstract=('An air history run of the NAME model.'),
            keywords=self._keywords,
            metadata=self._metadata,
            version=self._version,
            inputs=inputs,
            store_supported=True,
            status_supported=True
        )


    def _get_processed_inputs(self, request):
        """
        returns dictionary of inputs, some of which are used raw, 
        while others need some processing
        """

        known_location, longitude, latitude = self.get_processed_location(request)        
        hgrid_nx, hgrid_ny, hgrid_extent, domain = self.get_processed_grid_and_domain(request)
                                
        return {
            'Description': self._get_input(request, 'Description',
                                           default='NAME air history run'),
            'Domain_Xmax': domain[2],
            'Domain_Xmin': domain[0],
            'Domain_Ymax': domain[3],
            'Domain_Ymin': domain[1],
            'Duration': self._get_input(request, 'RunDuration'),
            'HGrid_nX': hgrid_nx,
            'HGrid_nY': hgrid_ny,
            'HGrid_Xmax': hgrid_extent[2],
            'HGrid_Xmin': hgrid_extent[0],
            'HGrid_Ymax': hgrid_extent[3],
            'HGrid_Ymin': hgrid_extent[1],
            'MainTGrid_dT': self._get_input(request, 'MainTGrid_dT'),
            'ArrivalBottom': self._get_input(request, 'ArrivalBottom'),
            'ArrivalLoc_Name': known_location,
            'ArrivalLoc_X': longitude,
            'ArrivalLoc_Y': latitude,
            'ArrivalStart': self._get_datetime(request, 'ArrivalStart'),
            'ArrivalStop': self._get_datetime(request, 'ArrivalStop'),
            'ArrivalTop': self._get_input(request, 'ArrivalTop'),
            'RunName': self._get_input(request, 'RunID'),
            'RunStart': self._get_start_datetime(request),
            'ZGrid': self._get_input(request, 'Heights', multi=True, sort=True),
            'met_data': self._get_input(request, 'MetData'), 

            # the following inputs are unused by make_wps_air_history_input
            #'notification_email': self._get_input(request, 'NotificationEmail'),
            'image_format': self._get_input(request, 'ImageFormat'),
            'met_height_units': self._get_input(request, 'HeightUnits'),
        }


    def _make_name_input(self, *args):
        return make_air_history_input(*args)


    def _get_adaq_scripts_and_args(self, input_params, outputs_dir, plots_dir):
        # image_extension not used as does not seem to be supported in name_field_plot.py
        # so also commented out above the call to self._get_image_format_process_input
        # and the inclusion in the dictionary returned by _get_processed_inputs
        
        z_level_list = self._get_z_level_list(input_params)
        extent_list = self._get_extent_list(input_params)
        plot_field_ini_contents = f'''

# plot configuration file for plotting NAME field output

# NAME output fields
field_attribute_dict = {{'Species':'INERT-TRACER'}}
# z level choices - optional
z_level_list = {z_level_list}
z_leveltype = 'height'

short_name_list = ["INERT-TRACER_AIR_CONCENTRATION"]

models_list     = ["name"]
models_fmt_list = ["name"]
models_dir_list = ["{outputs_dir}/Fields_grid1_C1_*.txt"]

plot_dir        = "{plots_dir}"

# Style options
#levels_list = [1.0e-8, 3.2e-8, 1.0e-7, 3.2e-7, 1.0e-6, 3.2e-6, 1.0e-5, 3.2e-5]
extent_list = {extent_list}
cmap        = 'YlGnBu'
mapping     = 'countries'
projection  = 'PlateCarree'
plottype    = 'pcolormesh'
cbar        = True
#cbar_label  = 'Concentration'
title       = 'name_verbose'
suptitle    = "{input_params['Description']}"
mobrand     = False
back        = True

annote_location     = 'right'
annote              = ''

'''
        plot_field_args = [self._make_work_file(plot_field_ini_contents, 'plot_field.ini')]
        
        return [
            ('name_field_plot.py', plot_field_args),
        ]
