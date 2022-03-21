import os
import datetime

from .get_met_info import GetMet
from .util import (render_template, get_times,
                   sanitise_name, combine_dicts)

from .paths import get_paths



fixed_params = {
    'nParticlesPerHr': 10000,
    'NWPMetModel': 'UM Global',
    'SyncTime_Minutes': 5,
}


def create_inputs(paths, params):
    """
    Creates the input file for the NAME general forward run, and return its path.
    """
    
    run_start_time, run_stop_time, time_after_first_hour = \
        get_times(params['RunStart'], params['Duration'])

    _, main_grid_t0, _ = \
        get_times(params['RunStart'], params['MainTGrid_dT'])

    get_met = GetMet()
    global_met = get_met.get_met(run_start_time, run_stop_time)

    met_decln_file = global_met['decln_filename'].replace('.txt', '.tmpl')
    met_defn_path = os.path.join(paths['met_defns_dir'],
                                 global_met['defn_filename'])
    
    timeformat = '%d/%m/%Y %H:%M'

    sync_steps_per_hr = 60 // params['SyncTime_Minutes']
    assert(60 % params['SyncTime_Minutes'] == 0)
    
    data = {
        'AvTimesAll': sync_steps_per_hr * params['Duration'],
        'AvTimesMain': sync_steps_per_hr * params['MainTGrid_dT'],
        'CompDom_Xmax': params['Domain_Xmax'],
        'CompDom_Xmin': params['Domain_Xmin'],
        'CompDom_Ymax': params['Domain_Ymax'],
        'CompDom_Ymin': params['Domain_Ymin'],
        'Duration': params['Duration'],
        'EndTimeOfRun': run_stop_time.strftime(timeformat),
        'HGrid_Xmax': params['HGrid_Xmax'],
        'HGrid_Xmin': params['HGrid_Xmin'],
        'HGrid_Ymax': params['HGrid_Ymax'],
        'HGrid_Ymin': params['HGrid_Ymin'],
        'HGrid_nX': params['HGrid_nX'],
        'HGrid_nY': params['HGrid_nY'],
        'HourlyTGrid_T0': time_after_first_hour.strftime(timeformat),
        'HourlyTGrid_nT': params['Duration'],
        'MainTGrid_T0': main_grid_t0.strftime(timeformat),
        'MainTGrid_dT': params['MainTGrid_dT'],
        'MainTGrid_nT': params['Duration'] // params['MainTGrid_dT'],
        'MetDeclnTmpl': met_decln_file,
        'MetDefnFile': met_defn_path,
        'MetDir': paths['met_dir'],
        'MetRestoreScript': paths['met_restore_script'],
        'nParticlesPerHr': params['nParticlesPerHr'],
        'OutputDir': paths['output_dir'],
        'ReleaseDZ': params['ReleaseTop'] - params['ReleaseBottom'],
        'ReleaseStart': params['ReleaseStart'].strftime(timeformat),
        'ReleaseStop': params['ReleaseStop'].strftime(timeformat),
        'ReleaseZ': (params['ReleaseTop'] + params['ReleaseBottom']) / 2,
        'Run_Name': sanitise_name(params['RunName']),
        'SourceLoc_Name': params['ReleaseLoc_Name'],
        'SourceLoc_X': params['ReleaseLoc_X'],
        'SourceLoc_Y': params['ReleaseLoc_Y'],
        'StartTimeOfRun': run_start_time.strftime(timeformat),
        'SyncTime': params['SyncTime_Minutes'],
        'TopogDir': paths['topog_dir'],
        'ZGrid': params['ZGrid'],
    }
    
    name_input_file = paths['input_file']
    render_template(paths['template_file'], data,
                    include_paths=[paths['met_decl_dir']], 
                    rendered_file=name_input_file)
    return name_input_file


def main(internal_run_id, input_params):

    params = combine_dicts(input_params, fixed_params)
    paths = get_paths(params['RunName'], internal_run_id,
                      run_type='gen_forward')
    fn = create_inputs(paths, params)
    return f'wrote NAME general forward run input file {fn}'
    

def do_example():
    # example...
    internal_run_id = '0192326540975'

    #parameters passed from the user - example values
    input_params = {
        'Domain_Xmax': 40.,
        'Domain_Xmin': -30.,
        'Domain_Ymax': 75.,
        'Domain_Ymin': 25.,
        'Duration': 72,
        'HGrid_nX': 300,
        'HGrid_nY': 300,
        'HGrid_Xmax': 35.,
        'HGrid_Xmin': -25.,
        'HGrid_Ymax': 70.,
        'HGrid_Ymin': 30.,
        #'JobTitle': 'NAME forwards run',
        'MainTGrid_dT': 6,
        'ReleaseBottom': 0.,
        'ReleaseLoc_Name': 'MACE_HEAD',
        'ReleaseLoc_X': -9.9,
        'ReleaseLoc_Y': 53.3167,
        'ReleaseStart': datetime.datetime(2018, 1, 1, 0, 0, 0),
        'ReleaseStop': datetime.datetime(2018, 1, 1, 6, 0, 0),
        'ReleaseTop': 500.,
        'RunName': 'Testing of a NAME general forward run',
        'RunStart': datetime.datetime(2018, 1, 1, 0, 0, 0),
        'ZGrid': [0., 500., 2000., 5000.],
    }

    msg = main(internal_run_id, input_params)
    print(msg)


if __name__ == '__main__':
    do_example()
