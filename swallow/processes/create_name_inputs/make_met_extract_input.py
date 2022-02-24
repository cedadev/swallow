import os
import datetime

from .get_met_info import GetMet
from .util import (bool_to_yesno, render_template, get_times,
                   sanitise_name, sanitise_description)

from .paths import get_paths



def create_inputs(paths, params):
    """
    Creates the input file for the NAME met extract run, and return its path.
    """
    
    run_start_time, run_stop_time, _ = \
        get_times(params['start_date_time'], params['run_duration'])

    get_met = GetMet()
    global_met = get_met.get_met2(run_start_time, run_stop_time)

    met_decln_file = global_met['decln_filename'].replace('.txt', '.tmpl')
    met_defn_path = os.path.join(paths['met_defns_dir'],
                                 global_met['defn_filename'])
    
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
        'OutputDir': paths['work_dir'],
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


def main(internal_run_id, params):

    paths = get_paths(params['run_name'], internal_run_id,
                      run_type='met_extract')
    fn = create_inputs(paths, params)
    return f'wrote NAME met extract input file {fn}'
    

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

    msg = main(internal_run_id, input_params)
    print(msg)


if __name__ == '__main__':
    do_example()
