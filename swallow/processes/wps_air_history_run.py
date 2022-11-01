from pywps import LiteralInput
from pywps.app.exceptions import ProcessError

from ._name_base_process import NAMEBaseProcess
from .create_name_inputs.make_air_history_input \
    import main as make_air_history_input


class AirHistoryRun(NAMEBaseProcess):
    """Run the NAME model in air history mode."""

    _description = "run the NAME model in air history mode"
    
    _domains = {
        '(none)': None,
        'European domain (30W-40E, 25N-75N)': [-30., 25., 40., 75.],
        'global': [-180., -90., 180., 90.],
    }
        
    _output_grids = {
        '(none)': None,
        'European output grid (25W-35E, 30N-70N) 300x300': [-25, 30, 35, 70, 300, 300],
        'global (720x360)': [-179.75, -89.75, 179.75, 89.75, 720, 360],
    }

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

        ] + self._get_start_date_time_process_inputs() + [
            self._get_run_duration_process_input(),
            
        ] + (self._get_date_time_process_inputs('ArrivalStart', 'Arrival Start',
                                                'start of arrival period') +
             self._get_date_time_process_inputs('ArrivalStop', 'Arrival Stop',
                                                'end of arrival period [NOTE: EARLIER than ArrivalStart, as backwards-running model]',
                                                default_add_hours=-3)
        ) + [
            LiteralInput('PredefDomain', 'Predefined Domain',
                         abstract=('predefined model computational domain '
                                   '(alternative to choosing bounding box)'),
                         data_type='string',
                         allowed_values=list(self._domains.keys()),                         
                         min_occurs=1,
                         max_occurs=1),

            self._get_bounding_box_input('Domain',
                                         'Computational Domain (if no predefined domain selected)'),
            
            LiteralInput('PredefOutputGrid', 'Predefined Output Grid',
                         abstract=('predefined output grid '
                                   '(alternative to choosing bounding box and resolution)'),
                         data_type='string',
                         allowed_values=list(self._output_grids.keys()),                         
                         min_occurs=1,
                         max_occurs=1),
                                                    
            self._get_bounding_box_input('OutputGridExtent',
                                         'Output Grid Extent (if no predefined output grid selected)'),

            LiteralInput('OutputGridNumLon', 'Output Grid nx (if no predefined output grid selected)', 
                         abstract=('enter number of longitudes in output grid '
                                   'unless you have chosen a predefined output grid'),
                         data_type='integer',
                         min_occurs=1,
                         max_occurs=1,
                         default=300),

            LiteralInput('OutputGridNumLat', 'Output Grid ny (if no predefined output grid selected)', 
                         abstract=('enter number of latitudes in output grid '
                                   'unless you have chosen a predefined output grid'),
                         data_type='integer',
                         min_occurs=1,
                         max_occurs=1,
                         default=300),

            self._get_heights_process_input('Grid Levels'),
            self._get_height_units_process_input(),

            LiteralInput('MainTGrid_dT', 'Timestep', 
                         abstract='main computational grid time resolution (hours)',
                         data_type='integer',
                         min_occurs=1,
                         max_occurs=1,
                         default=6),
            
            #==================================================
 
            #self._get_notification_email_process_input(),
            #self._get_image_format_process_input(),
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


    def _coords_to_lon_lat(self, coords_string):

        if coords_string is None:
            return ([], [])
        
        longitudes = []
        latitudes = []

        allowed_chars = '0123456789,.-+| '
        for c in coords_string:
            if c not in allowed_chars:
                raise ValueError(f'unexpected character {c} '
                                 f'in coordinates string {coords_string}')
        
        s = coords_string.replace(' ', '')

        for point_str in s.split('|'):
            if point_str:
                try:
                    lon_str, lat_str = point_str.split(',')
                except ValueError:
                    raise ValueError(f'location specification {point_str} '
                                     'not in format lon,lat')
                lon = float(lon_str)
                lat = float(lat_str)
                if not (-180 <= lon < 360):
                    raise ValueError(f'longitude {lon} out of range')
                if not (-90 <= lat <= 90):
                    raise ValueError(f'latitude {lat} out of range')                
                longitudes.append(lon)
                latitudes.append(lat)
            
        return longitudes, latitudes
        
        
    def _get_processed_inputs(self, request):
        """
        returns dictionary of inputs, some of which are used raw, 
        while others need some processing
        """
        runID = self._get_input(request, 'RunID')
        
        known_location = self._get_input(request, 'KnownLocation')
        latitude = self._get_input(request, 'Latitude')
        longitude = self._get_input(request, 'Longitude')

        if known_location != None and known_location != self._null_label:
            longitude, latitude = self._stations[known_location]

        domain = self._get_input(request, 'Domain')
        predef_domain_name = self._get_input(request, 'PredefDomain')
        predef_domain = self._domains[predef_domain_name]
        if predef_domain is not None:
            domain = predef_domain

        hgrid_nx = self._get_input(request, 'OutputGridNumLon')
        hgrid_ny = self._get_input(request, 'OutputGridNumLat')
        hgrid_extent = self._get_input(request, 'OutputGridExtent')
        predef_output_grid_name = self._get_input(request, 'PredefOutputGrid')
        predef_output_grid = self._output_grids[predef_output_grid_name]
        if predef_output_grid is not None:
            hgrid_nx, hgrid_ny = predef_output_grid[4:6]
            hgrid_extent = predef_output_grid[0:4]
                    
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
            'ArrivalStart': self._get_date_time(request, 'ArrivalStart'),
            'ArrivalStop': self._get_date_time(request, 'ArrivalStop'),
            'ArrivalTop': self._get_input(request, 'ArrivalTop'),
            'RunName': runID,
            'RunStart': self._get_start_date_time(request),
            'ZGrid': self._get_input(request, 'Heights', multi=True),

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
        
        plot_field_ini_contents = f'''

# plot configuration file for plotting NAME field output

# NAME output fields
field_attribute_dict = {{'Species':'INERT-TRACER'}}
# z level choices - optional
z_level_list = [50]
z_leveltype = 'height'

short_name_list = ["INERT-TRACER_AIR_CONCENTRATION"]

models_list     = ["name"]
models_fmt_list = ["name"]
models_dir_list = ["{outputs_dir}/Fields_grid1_C1_*.txt"]

plot_dir        = "{plots_dir}"

# Style options
#levels_list = [1.0e-8, 3.2e-8, 1.0e-7, 3.2e-7, 1.0e-6, 3.2e-6, 1.0e-5, 3.2e-5]
extent_list = [-30, 40, 25, 75]
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
#annote              = 'Here are a few lines of text\n intended to test the annotation feature.\n\n \
#You can replace this with your own text or\nchoose one of the default annotation options.'
annote              = ''

'''
        plot_field_args = [self._make_work_file(plot_field_ini_contents, 'plot_field.ini')]
        
        return [
            ('name_field_plot.py', plot_field_args),
        ]
