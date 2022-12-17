import os
import datetime
#from math import ceil

from .get_met_info import get_met_files
from .util import (combine_dicts, bool_to_yesno, render_template, get_times,
                   sanitise_name, sanitise_description)
from .paths import get_paths
from .get_domain_inputs import get_domain_inputs


# parameters which are hard coded but could later
# be passed from the user
fixed_params = {
    'Domain_Xmin': -180.,
    'Domain_Xmax': 180.,
    'Domain_Ymin': -90.,
    'Domain_Ymax': 90.,
    'Domain_Zmax': 19000.,
    'constant_height': False,
    'stochastic_trajectories': False,
    'number_stochastic_trajectories': 10,
    'sync_time_minutes': 1,
    't_grid_dt': 15,
}


def create_inputs(paths, params):
    """
    Creates the input file for the NAME run, and return its path.
    """
    
    run_start_time, run_stop_time, time_after_first_hour = \
        get_times(params['release_date_time'], params['run_duration'],
                  params['run_direction'])

    met_decln_file, met_defn_path = get_met_files(params, paths,
                                                  run_start_time, run_stop_time)
    
    timeformat = '%d/%m/%Y %H:%M'
    data = {
        'Backwards': bool_to_yesno(params['run_direction'] == 'Backward'),
        'OutputDir': paths['output_dir'],
        'EndTimeOfRun': run_stop_time.strftime(timeformat),
        'MetDefnFile': met_defn_path,
        #'MetDeclnFile': (met_decln_path),
        'MetDeclnTmpl': met_decln_file,
        'RunDuration': params['run_duration'],
        #'Run_Name': sanitise_description(params['description']),
        'Run_Name': sanitise_name(params['run_name']),
        'SourceLoc_Name': params['known_location'],
        'SourceLoc_X': params['longitude'],
        'SourceLoc_Y': params['latitude'],
        'StartTimeOfRun': run_start_time.strftime(timeformat),
        'SyncTime': f'{params["sync_time_minutes"]:02d}',
        'TimeAtFirstHour': time_after_first_hour.strftime(timeformat),
        'Turbulence': bool_to_yesno(params['stochastic_trajectories']),
        'VerticalVelocity': bool_to_yesno(not params['constant_height']),
        'dT': f'{params["t_grid_dt"]:02d}',
        #'nT': ceil(params['run_duration'] * 60 / params['t_grid_dt']),
        'nT': 1 + (params['run_duration'] * 60 // params['t_grid_dt']),
        'ReleaseHeights': params['trajectory_heights'],
        'nParticlesPerSource': (params['number_stochastic_trajectories']
                                if params['stochastic_trajectories'] else 1),
        'MetDir': paths['met_dir'],
        'TopogDir': paths['topog_dir'],
        'MetRestoreScript': paths['met_restore_script']
    }
    data.update(get_domain_inputs(params))

    name_input_file = paths['input_file']
    render_template(paths['template_file'], data,
                    include_paths=[paths["met_decl_dir"]], 
                    rendered_file=name_input_file)
    return name_input_file


def main(internal_run_id, input_params, work_dir):

    params = combine_dicts(input_params, fixed_params)
    paths = get_paths(params['run_name'], internal_run_id, work_dir, run_type="traj")
        
    fn = create_inputs(paths, params)
    output_dir = paths['output_dir']
    dirs_to_create = [output_dir, paths['met_dir']]
    return fn, output_dir, dirs_to_create
    

def do_example():
    # example...
    internal_run_id = '0192326540975'

    #parameters passed from the user - example values
    input_params = {
        'known_location': 'MACE_HEAD',  # ReleaseLoc_Name
        'longitude': -9.9,  # ReleaseLoc_X
        'latitude': 53.3167,  # ReleaseLoc_Y
        'trajectory_heights': [100.0, 500.0, 2000.0],  # ReleaseHeights
        'run_duration': 72,  # Duration
        'run_direction': 'Forward',  # Backwards = 0
        #'run_direction': 'Backward',  # Backwards = 1
        'met_data': 'UM Global',  # NWPMetModel
        'run_name': 'my run name',  # runName from user
        'description': 'Testing of a NAME trajectory run', # description from user
        'release_date_time': datetime.datetime(2018, 1, 1, 0, 0, 0),  # in UTC
        #'release_date_time': datetime.datetime(2014, 7, 16, 0, 0, 0),  # in UTC
    }
    work_dir = '/tmp/'

    print(main(internal_run_id, input_params, work_dir))


if __name__ == '__main__':
    do_example()
