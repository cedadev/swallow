import os
import datetime
import logging

from pywps import (Process, LiteralInput, LiteralOutput)
from pywps.app.Common import Metadata

LOGGER = logging.getLogger("PYWPS")



class NAMEBaseProcess(Process):

    _logger = LOGGER

    _version = '1.5'
    
    _keywords = ["name", "model", "atmospheric", "dispersion", "trajectory",
                 "forward", "backward", "air", "pollution", "transport"]
    
    _metadata = [
        Metadata('PyWPS', 'https://pywps.org/'),
        Metadata('Birdhouse', 'http://bird-house.github.io/'),
        Metadata('PyWPS Demo', 'https://pywps-demo.readthedocs.io/en/latest/'),
        Metadata('Emu: PyWPS examples', 'https://emu.readthedocs.io/en/latest/'),
    ]

    _stations = _stations = {
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

    _null_label = '(none)'

    def _get_request_internal_id(self):
        # FIXME: is there any kind of request ID in the request? 
        # (I didn't find one.)
        return f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{os.getpid()}'


    def _get_input(self, request, key, multi=False, default=None):

        inputs = request.inputs.get(key)

        if inputs == None:
            return default
        
        if multi:
            return [inp.data for inp in inputs]
        else:
            inp, = inputs
            return inp.data

    def _get_start_date_time(self, request):
        date = self._get_input(request, 'StartDate')
        tme = self._get_input(request, 'StartTime')
        return datetime.datetime(date.year,
                                 date.month,
                                 date.day,
                                 tme.hour,
                                 tme.minute,
                                 tme.second)

    
    def _get_met_data_process_input(self):
        return LiteralInput('MetData', 'met data',
                            abstract='which forcing dataset to use',
                            data_type='string',
                            allowed_values=["Global", "UK 1.5km", "Global + UK 1.5km"],
                            min_occurs=1,
                            max_occurs=1)

    def _get_notification_email_process_input(self):
        return LiteralInput('NotificationEmail', 'notification email',
                            abstract='which email address to send notifications to',
                            data_type='string',
                            min_occurs=0,
                            max_occurs=1)
    
    def _get_image_format_process_input(self):
        return LiteralInput('ImageFormat', 'image format',
                            abstract='format of output image file',
                            data_type='string',
                            default='PNG',
                            allowed_values=['PNG', 'JPG', 'PDF'],
                            min_occurs=1,
                            max_occurs=1)

    def _get_run_duration_process_input(self):
        return LiteralInput('RunDuration', 'run duration',
                            abstract='duration of run, in hours',
                            data_type='integer',
                            allowed_values=[12, 24, 36, 48, 72, 96, 120, 144, 168, 240, 360, 480],
                            min_occurs=1,
                            max_occurs=1)

    def _get_height_units_process_input(self):
        return LiteralInput('HeightUnits', 'height units',
                            abstract='units for the height value',
                            data_type='string',
                            allowed_values=['metres above ground level (m agl)', 'metres above sea level (m asl)'],
                            min_occurs=1,
                            max_occurs=1)
            
    def _get_start_date_process_input(self):        
        current_year = datetime.datetime.now().year
        return LiteralInput('StartDate', 'start date',
                            abstract='* date of start of run (enter as yyyy-mm-dd or yyyymmdd format)',
                            data_type='date',
                            min_occurs=1,
                            max_occurs=1,
                            default=f'{current_year}-01-01')

    def _get_start_time_process_input(self):        
        return LiteralInput('StartTime', 'start time',
                            abstract='* time of start of run (enter as hh:mm or hh:mm:ss format)',
                            data_type='time',
                            min_occurs=1,
                            max_occurs=1,
                            default='00:00')

    def _get_run_id_process_input(self):
        return LiteralInput('RunID', 'run identifier',
                            abstract='* short text string to describe task',
                            data_type='string',
                            min_occurs=1,
                            max_occurs=1)

    def _get_description_process_input(self):
        return LiteralInput('Description', 'description',
                            abstract='longer text description',
                            data_type='string',
                            min_occurs=0,
                            max_occurs=1)

    def _get_inputs_process_output(self):
        return LiteralOutput('inputs', 'Copy of inputs',
                             abstract='This output just gives a string confirming the inputs used.',
                             keywords=['output', 'result', 'response'],
                             data_type='string')

    def _get_message_process_output(self):
        return LiteralOutput('message', 'Status message',
                             abstract='This output gives a response from the job submission process.',
                             keywords=['output', 'result', 'response'],
                             data_type='string')

    
    def _handler(self, request, response):
        self._logger.info(self._description)

        internal_run_id = self._get_request_internal_id()
        input_params = self._get_processed_inputs(request)
        msg = self._handler_backend(internal_run_id, input_params)
        response.outputs['message'].data = msg

        d = input_params
        response.outputs['inputs'].data = ', '.join(f'{k}: {d[k]}'
                                                    for k in sorted(d))

        # uncomment to show inputs in UI
        response.outputs['message'].data += f' INPUTS: {response.outputs["inputs"].data}'
        
        return response
