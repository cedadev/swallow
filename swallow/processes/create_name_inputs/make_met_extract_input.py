import os
import datetime

from .get_met_info import get_met_files
from .util import (bool_to_yesno, render_template, get_times,
                   sanitise_name, sanitise_description)

from .paths import get_paths



def create_inputs(paths, params):
    """
    Creates the input file for the NAME met extract run, and return its path.
    """
    
    run_start_time, run_stop_time, _ = \
        get_times(params['start_date_time'], params['run_duration'])

    met_decln_file, met_defn_path = get_met_files(params, paths,
                                                  run_start_time, run_stop_time)
    
    timeformat = '%d/%m/%Y %H:%M'
    data = {
        'EndTimeOfRun': run_stop_time.strftime(timeformat),
        'LocationNames': params['location_names'],
        'LocationX': params['longitudes'],
        'LocationY': params['latitudes'],
        'MetDeclnTmpl': met_decln_file,
        'MetDefnFile': met_defn_path,
        'MetDir': paths['met_dir'],
        'MetHeight': params['met_height'],
        'MetRestoreScript': paths['met_restore_script'],
        'OutputDir': paths['output_dir'],
        'Run_Name': sanitise_name(params['run_name']),
        #'Run_Name': sanitise_description(params['description']),
        'StartTimeOfRun': run_start_time.strftime(timeformat),
        'TopogDir': paths['topog_dir'],
        'nOutputTimes': params['run_duration'] + 1,
        }

    name_input_file = paths['input_file']
    render_template(paths['template_file'], data,
                    include_paths=[paths['met_decl_dir']], 
                    rendered_file=name_input_file)
    return name_input_file


def main(internal_run_id, params, work_dir):

    paths = get_paths(params['run_name'], internal_run_id, work_dir,
                      run_type='met_extract')

    fn = create_inputs(paths, params)
    output_dir = paths['output_dir']
    dirs_to_create = [output_dir, paths['met_dir']]
    return fn, output_dir, dirs_to_create
    

def do_example():
    # example...
    internal_run_id = '0192326540975'

    #parameters passed from the user - example values
    input_params = {
        'location_names': ['MACE_HEAD', 'EXETER', 'HALLEY'],
        'longitudes': [-9.90, -3.47, -25.50],
        'latitudes': [53.32, 50.73, -75.50],
        'met_height': 10.0,
        'run_duration': 72,
        'met_data': 'UM Global',
        'run_name': 'my run name',
        'description': 'Testing of a NAME met extract run',
        'start_date_time': datetime.datetime(2022, 1, 1, 0, 0, 0),  # in UTC
    }

    work_dir = '/tmp'
    
    print(main(internal_run_id, input_params, work_dir))


if __name__ == '__main__':
    do_example()
