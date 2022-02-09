import os
import datetime
from math import ceil
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader

from get_met_info import GetMet
from util import combine_dicts, bool_to_yesno
from paths import get_paths


#parameters passed from the user - example values
input_params = {
    'jobTitle': 'Testing of a NAME trajectory run',
    'known_location': 'MACE_HEAD',  # ReleaseLoc_Name
    'longitude': -9.9,  # ReleaseLoc_X
    'latitude': 53.3167,  # ReleaseLoc_Y
    'trajectory_heights': [100.0, 500.0, 2000.0],  # ReleaseHeights
    'run_duration': 72.,  # Duration
    #'run_direction': 'Forward',  # Backwards = 0
    'run_direction': 'Backward',  # Backwards = 1
    'met_data': 'UM Global',  # NWPMetModel
    'run_name': 'my run name',  # runName from user
    'release_date_time': datetime.datetime(2014, 7, 11, 0, 0, 0),  # in UTC
    #'release_date_time': datetime.datetime(2014, 7, 16, 0, 0, 0),  # in UTC
}

# example...
internal_run_id = '0192326540975'

# parameters which are hard coded but could later
# be passed from the user
fixed_params = {
    'domain_xmin': -105.0,
    'domain_xmax': 50.0,
    'domain_ymin': 6.0,
    'domain_ymax': 84.0,
    'constant_height': False,
    'stochastic_trajectories': False,
    'number_stochastic_trajectories': 10,
    'sync_time_minutes': 1,
    't_grid_dt': 15,
}


def get_times(params):
    directions = {'Forward': 1,
                  'Backward': -1}

    hour = datetime.timedelta(hours=1)

    run_start_time = params['release_date_time']
    run_stop_time = params['release_date_time'] + directions[params['run_direction']] * hour * params['run_duration']
    time_after_first_hour = params['release_date_time'] + directions[params['run_direction']] * hour

    return run_start_time, run_stop_time, time_after_first_hour
    


def create_inputs(paths, params):
    """
    Creates the input file for the NAME run, and return its path.
    """
    
    run_start_time, run_stop_time, time_after_first_hour = get_times(params)

    get_met = GetMet()
    global_met = get_met.get_met2(run_start_time, run_stop_time)

    met_decln_file = global_met['decln_filename'].replace('.txt', '.tmpl')
    met_defn_path = os.path.join(paths['utils_dir'], global_met['defn_filename'])
    
    timeformat = '%d/%m/%Y %H:%M'
    data = {
        'Backwards': bool_to_yesno(params['run_direction'] == 'Backward'),
        'OutputDir': paths['output_dir'],
        'CompDom_Xmax': params['domain_xmax'],
        'CompDom_Xmin': params['domain_xmin'],
        'CompDom_Ymax': params['domain_ymax'],
        'CompDom_Ymin': params['domain_ymin'],
        'EndTimeOfRun': run_stop_time.strftime(timeformat),
        'MetDefnFile': met_defn_path,
        #'MetDeclnFile': (met_decln_path),
        'MetDeclnTmpl': met_decln_file,
        'RunDuration': params['run_duration'],
        'Run_Name': params['run_name'],
        'SourceLoc_Name': params['known_location'],
        'SourceLoc_X': params['longitude'],
        'SourceLoc_Y': params['latitude'],
        'StartTimeOfRun': run_start_time.strftime(timeformat),
        'SyncTime': f'{params["sync_time_minutes"]:02d}',
        'TimeAtFirstHour': time_after_first_hour.strftime(timeformat),
        'Turbulence': bool_to_yesno(params['stochastic_trajectories']),
        'VerticalVelocity': bool_to_yesno(not params['constant_height']),
        'dT': f'{params["t_grid_dt"]:02d}',
        'nT': ceil(params['run_duration'] * 60 / params['t_grid_dt']),
        'ReleaseHeights': params['trajectory_heights'],
        'nParticlesPerSource': (params['number_stochastic_trajectories']
                                if params['stochastic_trajectories'] else 1),
        'MetDir': paths['met_dir'],
        'TopogDir': paths['topog_dir'],
        #'MetRestoreScript': paths['m']
    }

    template_str = open(paths['template_file']).read()    
    include_paths = [paths["met_decl_dir"]]
    template = Environment(loader=FileSystemLoader(include_paths)).from_string(template_str)
    rendered = template.render(**data)

    fn = paths['input_file']
    with open(fn, 'w') as f:
        f.write(rendered)
    return fn    


def main():
    params = combine_dicts(input_params, fixed_params)
    paths = get_paths(params['run_name'], internal_run_id)

    fn = create_inputs(paths, params)
    print(f'wrote NAME input file {fn}')
    
    
if __name__ == '__main__':
    main()
