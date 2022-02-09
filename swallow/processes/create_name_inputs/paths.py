import os

from util import sanitise_name


this_dir = os.path.dirname(os.path.realpath(__file__))

_paths = {
    'gws': '/gws/nopw/j04/name',
    'scratch_dir': '/work/scratch-pw/............',
    'usercache_dir': '/work/scratch-pw/............',
    'work_dir': '....................',
    'template_file': f'{this_dir}/traj_input.tmpl',
    'met_decl_dir': f'{this_dir}/met_declarations',
}

_paths.update({
    'script_dir': f'{_paths["usercache_dir"]}/SimpleTrajectoryRun',
    'utils_dir': f'{_paths["usercache_dir"]}/CommonUtilities',
    'adaqpython_dir': f'{_paths["gws"]}/code/ADAQ_Python_v6.2',
    'nameiii_dir': f'{_paths["gws"]}/code/NAMEIII_v7_2_lotus',
    'topog_dir': f'{_paths["gws"]}/code/NAMEIII_v7_2_lotus/Resources/Topog',
    'met_dir': f'{_paths["work_dir"]}/met_data',    
})

input_file_fmt = '{run_label}.txt'
output_dir_fmt = f'{_paths["usercache_dir"]}/NAME_Results_' '{run_label}'


def get_paths(run_name, internal_run_id):

    paths = _paths.copy()
    
    run_label = f'{sanitise_name(run_name)}_{internal_run_id}'

    paths['output_dir'] = output_dir_fmt.format(run_label=run_label)
    paths['input_file'] = input_file_fmt.format(run_label=run_label)

    return paths
