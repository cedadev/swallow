import os
import string

from .util import sanitise_name

this_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(this_dir, 'templates')

_paths = {
    'gws': '/gws/nopw/j04/name'
}
_paths.update({
    'work_dir': '/work/scratch-nopw/iwi/work.12345',  ##CHANGEME
    'met_decl_dir': f'{template_dir}/met_declarations',
})
_paths.update({
    'name_input_dir': '/tmp', ##CHANGEME  # where to put the input file
    'script_dir': f'{_paths["gws"]}/cache/users/arjones/SimpleTrajectoryRun',
    'utils_dir': f'{_paths["gws"]}/cache/users/arjones/CommonUtilities',    
    'defns_dir': f'{_paths["gws"]}/cache/users/arjones/FCM/vn8.0_jasmin/Resources/Defns',
    'adaqpython_dir': f'{_paths["gws"]}/code/ADAQ_Python_v6.2',
    'met_dir': f'{_paths["work_dir"]}/met_data',
})
_paths.update({
    'met_restore_script': f'{_paths["utils_dir"]}/MetRestore_JASMIN.sh',
})

_paths_by_run_type = {
    'traj': {
        'template_file': f'{template_dir}/traj_input.tmpl',
        'nameiii_dir': f'{_paths["gws"]}/code/NAMEIII_v7_2_lotus',
        'topog_dir': f'{_paths["gws"]}/code/NAMEIII_v7_2_lotus/Resources/Topog',
    },
    'met_extract': {
        'template_file': f'{template_dir}/met_extract_input.tmpl',
        'nameiii_dir': f'{_paths["gws"]}/code/NAME_v8_3',
        'topog_dir': f'{_paths["gws"]}/data/UMTopogData',
        'met_defns_dir': f'{_paths["gws"]}/code/NAME_v8_3/Resources/Defns/',
    },
}


input_file_fmt = '{run_label}.txt'
output_dir_fmt = f'{_paths["work_dir"]}/NAME_Results_' '{run_label}'


def get_paths(run_name, internal_run_id, run_type=None):

    paths = _paths.copy()
    
    if run_type:
        run_name = f'{run_type}_{run_name}'

    run_label = f'{sanitise_name(run_name)}_{internal_run_id}'

    paths['output_dir'] = output_dir_fmt.format(run_label=run_label)
    paths['input_file'] = os.path.join(paths['name_input_dir'],
                                       input_file_fmt.format(run_label=run_label))

    paths.update(_paths_by_run_type.get(run_type, {}))

    return paths
