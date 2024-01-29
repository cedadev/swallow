import os
import datetime
import logging
import time
import sys

from pywps import (Process, LiteralInput, LiteralOutput, ComplexOutput,
                   BoundingBoxInput, BoundingBoxOutput, FORMATS)
from pywps.inout.outputs import MetaLink4, MetaFile
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError

from ._run_name_model import run_name_model
from ._plot_output import run_adaq_scripts, convert_plots
from .create_name_inputs.get_met_info import met_dataset_names

LOGGER = logging.getLogger("PYWPS")


class NAMEBaseProcess(Process):

    _logger = LOGGER

    _version = '1.5'
    
    _keywords = ["name", "model", "atmospheric", "dispersion", "trajectory",
                 "forward", "backward", "air", "pollution", "transport"]
    
    _metadata = [
        Metadata('PyWPS', 'https://pywps.org/'),
        Metadata('Birdhouse', 'http://bird-house.github.io/'),
        Metadata('Met Office dispersion model', 'https://www.metoffice.gov.uk/research/approach/modelling-systems/dispersion-model')
    ]

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

    _null_label = '(none)'

    def __init__(self, *args, **kwargs):
        key = 'outputs'
        if key in kwargs:
            outputs = kwargs[key].copy()
        else:
            outputs = []
        outputs.extend(self._get_common_outputs())
        kwargs[key] = outputs
        super().__init__(*args, **kwargs)
        

    def _get_common_outputs(self):
        #
        # Outputs which are common to all run types.
        # In principle, individual run types can specify other output by passing
        # outputs=[....] to the base class init (see above), but currently
        # none of them need to do so.
        #
        return [
            ComplexOutput('model_output_files',
                          'METALINK v4 output',
                          abstract='Metalink v4 document with references to output files.',
                          as_reference=True,
                          supported_formats=[FORMATS.META4],
            ),
            ComplexOutput('name_input_file', 'Copy of NAME model input file',
                          as_reference=True,
                          supported_formats=[FORMATS.TEXT]
            ),
            ComplexOutput('name_stdout', 'NAME model standard output',
                          as_reference=True,
                          supported_formats=[FORMATS.TEXT]
            ),
            ComplexOutput('name_stderr', 'NAME model standard error',
                          as_reference=True,
                          supported_formats=[FORMATS.TEXT]
            ),
            LiteralOutput('message', 'Status message',
                          abstract=('This output gives a response from '
                                    'the job submission process.'),
                          keywords=['output', 'result', 'response'],
                          data_type='string'),
        ]
        
        
    def _get_request_internal_id(self):
        # FIXME: is there any kind of request ID in the request? 
        # (I didn't find one.)
        return (f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_'
                f'{os.getpid()}')


    def _get_input(self, request, key, multi=False, default=None, sort=None):

        inputs = request.inputs.get(key)

        if inputs == None:
            return default
        
        if multi:
            vals = [inp.data for inp in inputs]
            return sorted(vals) if sort else vals
        else:
            inp, = inputs
            return inp.data

        
    def _get_date_time(self, request, name):
        date = self._get_input(request, f'{name}Date')
        tme = self._get_input(request, f'{name}Time')
        return datetime.datetime(date.year,
                                 date.month,
                                 date.day,
                                 tme.hour,
                                 tme.minute,
                                 tme.second)

    def _get_start_date_time(self, request):
        return self._get_date_time(request, 'Start')

    #================= INPUTS ======================
    
    def _get_met_data_process_input(self):
        return LiteralInput('MetData', 'Met Data',
                            abstract='which forcing dataset to use',
                            data_type='string',
                            allowed_values=met_dataset_names,
                            min_occurs=1,
                            max_occurs=1)

    ## Notification Email - we have decided to take this from user database rather
    ##                      than form input - should not need this input any more
    #
    # def _get_notification_email_process_input(self):
    #     return LiteralInput('NotificationEmail', 'Notification Email',
    #                         abstract=('which email address to send '
    #                                   'notifications to'),
    #                         data_type='string',
    #                         min_occurs=0,
    #                         max_occurs=1)

    
    def _get_image_format_process_input(self):
        return LiteralInput('ImageFormat', 'Image Format',
                            abstract='format of output image file',
                            data_type='string',
                            default='PNG',
                            allowed_values=['PNG', 'JPG', 'PDF'],
                            min_occurs=1,
                            max_occurs=1)

    
    def _get_run_duration_process_input(self):
        return LiteralInput('RunDuration', 'Run Duration',
                            abstract='duration of run, in hours',
                            data_type='integer',
                            allowed_values=[12, 24, 36, 48, 72, 96, 120,
                                            144, 168, 240, 360, 480],
                            min_occurs=1,
                            max_occurs=1)

    
    def _get_height_units_process_input(self):
        return LiteralInput('HeightUnits', 'Height Units',
                            abstract=('units for the height value '
                                      '(currently only m agl supported)'),
                            data_type='string',
                            #allowed_values=['metres above ground level (m agl)', 'metres above sea level (m asl)'],
                            allowed_values=['metres above ground level (m agl)'],
                            min_occurs=1,
                            max_occurs=1)
            

    def _get_default_datetime(self):
        current_year = datetime.datetime.now().year
        return datetime.datetime(current_year, 1, 1)
    
    def _get_date_process_input(self, name, label, description, default_datetime=None):
        if default_datetime is None:
            default_datetime = self._get_default_datetime()
        default_date = default_datetime.strftime("%Y-%m-%d")
            
        return LiteralInput(name, label,
                            abstract=(f'* date of {description} (enter as '
                                      'yyyy-mm-dd or yyyymmdd format)'),
                            data_type='date',
                            min_occurs=1,
                            max_occurs=1,
                            default=default_date)

    
    def _get_time_process_input(self, name, label, description, default_datetime=None):
        if default_datetime is None:
            default_datetime = self._get_default_datetime()
        default_time = default_datetime.strftime("%H:%M")
        return LiteralInput(name, label,
                            abstract=(f'* time of {description} (enter as hh:mm '
                                      'or hh:mm:ss format)'),
                            data_type='time',
                            min_occurs=1,
                            max_occurs=1,
                            default=default_time)

    def _get_date_time_process_inputs(self, name, label, description,
                                      default_datetime=None, default_add_hours=None):
        if default_datetime is None:
            default_datetime = self._get_default_datetime()
        if default_add_hours is not None:
            default_datetime += datetime.timedelta(hours=default_add_hours)
        return [self._get_date_process_input(f'{name}Date', f'{label} Date', description,
                                             default_datetime=default_datetime),
                self._get_time_process_input(f'{name}Time', f'{label} Time', description,
                                             default_datetime=default_datetime)]

    def _get_start_date_time_process_inputs(self):
        return self._get_date_time_process_inputs('Start', 'Start', 'start of run')

    def _get_run_id_process_input(self):
        return LiteralInput('RunID', 'Run Identifier',
                            abstract='* short text string to describe task',
                            data_type='string',
                            min_occurs=1,
                            max_occurs=1)

    
    def _get_description_process_input(self):
        return LiteralInput('Description', 'Description',
                            abstract='longer text description',
                            data_type='string',
                            min_occurs=0,
                            max_occurs=1)


    def _get_latitude_process_input(self):
        return LiteralInput('Latitude', 'Latitude',
                            abstract='latitude of trajectory start/end-point',
                            data_type='float',
                            min_occurs=0,
                            max_occurs=1)

    def _get_longitude_process_input(self):
        return LiteralInput('Longitude', 'Longitude',
                            abstract='longitude of trajectory start/end-point',
                            data_type='float',
                            min_occurs=0,
                            max_occurs=1)

    def _get_known_location_process_input(self):
        return LiteralInput('KnownLocation', 
                            'Standard Location Name (alternative to lon/lat)',
                            abstract='known location',
                            data_type='string',
                            min_occurs=0,
                            max_occurs=1,
                            allowed_values=[self._null_label] + sorted(self._stations.keys()))

    
    def _get_heights_process_input(self, label):
        return LiteralInput('Heights', label,
                            abstract='array of heights',
                            data_type='float',
                            min_occurs=1,
                            max_occurs=999,
        )

    def _get_bounding_box_input(self, name, description):
        return BoundingBoxInput(name, description,
                                crss=['epsg:4326'],
                                dimensions=2)


    def _create_metalink(self, dir_paths, extra_file_paths, identity, description):
        
        ml4 = MetaLink4(identity=identity,
                        description=description,
                        workdir=self.workdir,
                        publisher='swallow WPS')

        outputs = []
        for dir_path in dir_paths:
            filenames = sorted(os.listdir(dir_path))
            for fname in filenames:
                path = os.path.join(dir_path, fname)
                outputs.append((fname, path))
        for path in extra_file_paths:
            fname = os.path.basename(path)
            outputs.append((fname, path))
            
        n = len(outputs)
        for i, (fname, path) in enumerate(outputs, start=1):
            file_desc = f'{description} (file {i}/{n}: {fname})'
            mf = MetaFile(file_desc, file_desc, fmt=FORMATS.TEXT)
            mf.file = path
            ml4.append(mf)

        return ml4.xml


    _adaq_scripts_use_image_extension = False

    def _get_adaq_scripts_and_args(self, *args):
        # to override in subclasses
        return []
    

    def _make_work_file(self, contents, filename, keep=True):
        path = os.path.join(self.workdir, filename)
        with open(path, 'w') as fout:
            fout.write(contents)
        if keep:
            self._work_files_to_keep.append(path)
        return path


    def _update_status(self, message, percentage):
        pc = round(percentage)
        pc = max(pc, 0)
        pc = min(pc, 100)
        self.response.update_status(message, pc)
        sys.stderr.write(f"UPDATE STATUS: {message} {pc}\n")
        
    
    def _handler(self, request, response):
        self._logger.info(self._description)
        model_start_pc = 10
        model_end_pc = 90

        self._work_files_to_keep = []
        
        # Set self.response so it can be modified in other methods
        self.response = response
        
        self._update_status('Job is now running', 0)
        
        internal_run_id = self._get_request_internal_id()
        input_params = self._get_processed_inputs(request)

        name_input_file, output_dir, dirs_to_create = \
            self._make_name_input(internal_run_id, input_params, self.workdir)

        self._update_status('Input file for Model model created', model_start_pc)

        plots_dir = os.path.join(self.workdir, 'plots')
        dirs_to_create.append(plots_dir)
        
        for path in dirs_to_create:
            if not os.path.isdir(path):
                os.makedirs(path)

        t_start = time.time()
        rtn_code, stdout_path, stderr_path = run_name_model(name_input_file,
                                                            logdir=self.workdir,
                                                            update_status_callback=self._update_status,
                                                            start_percent=model_start_pc,
                                                            end_percent=model_end_pc)
        run_time = time.time() - t_start

        if rtn_code != 0:
            raise ProcessError(f"NAME Fortran code exited abnormally (status={rtn_code})")
            
        self._update_status('Model code completed - starting plotting', model_end_pc)        

        image_extension = self._get_image_extension(input_params)
        args = [input_params, output_dir, plots_dir]
        if self._adaq_scripts_use_image_extension:
            args.append(image_extension)
        adaq_scripts_and_args = self._get_adaq_scripts_and_args(*args)
        if adaq_scripts_and_args:
            default_extension = 'png'  # format written by scripts that do not support filename input
            adaq_message = run_adaq_scripts(adaq_scripts_and_args)

            if image_extension != default_extension and not self._adaq_scripts_use_image_extension:
                percent = round((model_end_pc + 100) / 2)
                self._update_status(f'Plots produced as {default_extension}', percent)
                message = convert_plots(plots_dir, image_extension)
                adaq_message += f"Plot format conversion messages:\nf{message}"
                self._update_status(f'Plots converted to {image_extension}', 100)
                
            self._update_status('Plots completed', 100)  # basically 100% done at this point
        else:
            adaq_message = '(plots not produced for this run type)'
            self._update_status('Run completed', 100)
            
        response.outputs['name_input_file'].file = name_input_file
        response.outputs['name_stdout'].file = stdout_path
        response.outputs['name_stderr'].file = stderr_path
        
        response.outputs['model_output_files'].data = \
            self._create_metalink([output_dir, plots_dir],
                                  self._work_files_to_keep,
                                  'name-result', 'NAME model output files')

        d = input_params
        inputs = ', '.join(f'\n  {k}: {d[k]}' for k in sorted(d))

        message = f'''
NAME model run type: {self._description}.
WPS inputs: {inputs}
Using working directory: {self.workdir} .
Run time was {run_time} seconds.
Stdout path was {stdout_path} .
Stderr path was {stderr_path} .

Messages from plotting routines (if any):
{adaq_message}
'''
        response.outputs['message'].data = message
                
        #os.system(f'cp {stdout_path} /tmp/')  # debug...
        #os.system(f'cp {stderr_path} /tmp/')  # debug...
        #os.system(f'cp -r {self.workdir} /tmp/copy/')  # debug...
               
        return response

    
    def _get_image_extension(self, input_params):
        """
        Convert selected filename extension to image format.  It so happens that for the recognised
        formats it is just a matter of lower case equivalent, but this will force it to default to png
        if it is anything else (or if the input is not provided by the form).
        """
        image_format = input_params.get('image_format')

        # dictionary keys should match the allowed values in _get_image_format_process_input above
        lookup = {'PNG': 'png',
                  'JPG': 'jpg',
                  'PDF': 'pdf'}

        return lookup.get(image_format, 'png')


    def _get_z_level_list(self, input_params):
        """
        Get the interface levels from the vertical grid.
        Used by general forward run and air history run for plotting.
        """
        zgrid = input_params['ZGrid']
        return [(lower + upper) / 2 for lower, upper in zip(zgrid, zgrid[1:])]

    
    def _get_extent_list(self, input_params):
        """
        Get the horizontal extent list for plotting.
        Used by general forward run and air history run for plotting.
        Note that this is in a different ordering from the input domain
        """
        suffixes = ['Xmin', 'Xmax', 'Ymin', 'Ymax']
        #prefix = 'Domain_'
        prefix = 'HGrid_'
        return [ input_params[f"{prefix}{suffix}"] for suffix in suffixes ]
