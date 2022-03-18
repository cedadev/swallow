from pywps import LiteralInput
from pywps.app.exceptions import ProcessError

from .name_base_process import NAMEBaseProcess
from .create_name_inputs.make_gen_forward_input \
    import main as make_gen_forward_input

import datetime



class ExtractMetData(NAMEBaseProcess):
    """Run the NAME model to extract met data."""

    _description = "extract met data for NAME"
    
    def __init__(self):

        #-----------------------------------------
        # Note: docs at
        # https://pywps.readthedocs.io/en/latest/api.html
        #
        # and to see allowed values of data_type:
        #   from pywps.inout.literaltypes import LITERAL_DATA_TYPES
        #   print(LITERAL_DATA_TYPES)
        #-----------------------------------------

        coords_abstract = (
            'Strings of format lon,lat. '
            'Separate pairs with pipe symbols (vertical bar). '
            'Optional whitespace is permitted. '
            'Longitudes may use -180 to 180 or 0 to 360. '
            'EXAMPLE: you could enter "-1.3, 51.6 | 1,-2" '
            'for 1.3W,51.6N and 1E,2S. '
            '(This input may be omitted if known locations are selected.)'
        )

        _domains = {
            '(none)': None,
            'European domain (30W-40E, 25N-75N)': [-30., 25., 40., 75.],
            'global': [-180., -90., 180., 90.],
        }
        
        _output_grids = {
            '(none)': None,
            'European output grid (25W-35E, 30N-70N) 300x300': [-30, 25, 40, 75, 300, 300],
            'global (720x360)': [-179.75, -89.75, 179.75, 89.75, 720, 360],
        }

        inputs = [
            self._get_run_id_process_input(),
            self._get_description_process_input(),
            self._get_latitude_process_input(),
            self._get_longitude_process_input(),
            self._get_known_location_process_input(),

            
            LiteralInput('ReleaseBottom', 'release bottom',
                         abstract='height at the bottom of the release',
                         data_type='float',
                         default=0.,
                         min_occurs=1,
                         max_occurs=1),

            LiteralInput('ReleaseTop', 'release top',
                         abstract='height at the top of the release',
                         data_type='float',
                         default=500.,
                         min_occurs=1,
                         max_occurs=1),

            self._get_start_date_process_input(),
            self._get_start_time_process_input(),
            self._get_run_duration_process_input(),

            
            LiteralInput('PredefDomain', 'predefined domain',
                         abstract=('predefined model computational domain '
                                   '(alternative to choosing bounding box)'),
                         data_type='string',
                         allowed_values=list(self._domains.keys()),                         
                         min_occurs=1,
                         max_occurs=1)

            self._get_bounding_box_input('Domain',
                                         'computational domain (if not using predefined domain)')
            
            LiteralInput('PredefOutputGrid', 'predefined output grid',
                         abstract=('predefined output grid '
                                   '(alternative to choosing bounding box and resolution)'),
                         data_type='string',
                         allowed_values=list(self._domains.keys()),                         
                         min_occurs=1,
                         max_occurs=1)

            self._get_bounding_box_input('OutputGridExtent',
                                         'output grid extent (if not using predefined domain)')

            LiteralInput('OutputGridNumLon', 'output grid nx', 
                         abstract=('number of longitudes in output grid '
                                   '(if not using predefined domain)'),
                         data_type='int',
                         min_occurs=1,
                         max_occurs=1,
                         default=300),

            LiteralInput('OutputGridNumLon', 'output grid ny', 
                         abstract=('number of latitudes in output grid '
                                   '(if not using predefined domain)'),
                         data_type='int',
                         min_occurs=1,
                         max_occurs=1,
                         default=300),

            self._get_latitude_process_input(),
            self._get_longitude_process_input(),
            self._get_known_location_process_input(),

            self._get_trajectory_heights_process_input(),
            self._get_height_units_process_input(),

            
            
            #==================================================
            
            
            
            LiteralInput('MetHeight', 'met data height',
                         abstract='* height at which to extract met data',
                         data_type='float',
                         min_occurs=1,
                         max_occurs=1,
                         ),

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
            identifier='NAMEMetExtract',
            title='General forward run',
            abstract=('A forward run of the NAME model.'),
            keywords=self._keywords,
            metadata=self._metadata,
            version=self._version,
            inputs=inputs,
            outputs=outputs,
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
        
        predef_locations = self._get_input(request, 'PredefinedLocations',
                                           multi=True)
        coordinates = self._get_input(request, 'Coordinates')

        try:
            longitudes, latitudes = self._coords_to_lon_lat(coordinates)
        except ValueError as exc:
            raise ProcessError(str(exc))
            
        location_names = [f'user defined {i+1}' for i in range(len(longitudes))]
        
        if predef_locations != None:
            for location in predef_locations:
                longitude, latitude = self._stations[location]
                longitudes.append(longitude)
                latitudes.append(latitude)
                location_names.append(location)

        longitudes = [lon % 360 for lon in longitudes]
        start_date_time = self._get_start_date_time(request)

        if not longitudes:
            raise ProcessError('process inputs for coordinates and" '
                               'predefined locations are both empty')
        
        return {
            'description': self._get_input(request, 'Description',
                                           default='NAME met data extraction run'),
            'location_names': location_names,
            'longitudes': longitudes,
            'latitudes': latitudes,
            'met_height': self._get_input(request, 'MetHeight'),
            'run_duration': self._get_input(request, 'RunDuration'),
            'met_data': self._get_input(request, 'MetData'), 
            'run_name': self._get_input(request, 'RunID'),
            'start_date_time': start_date_time,
            
            # the following inputs are unused by make_met_extract_input
            'notification_email': self._get_input(request, 'NotificationEmail'),
            'image_format': self._get_input(request, 'ImageFormat'),
            'met_height_units': self._get_input(request, 'HeightUnits'),
        }


    def _handler_backend(self, internal_run_id, input_params):
        return make_met_extract_input(internal_run_id, input_params)
