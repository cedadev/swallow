import os

from .util import sanitise_name


this_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(this_dir, 'templates')

_paths = {
    'gws': '/gws/nopw/j04/name'
}
_paths.update({
    'scratch_dir': '/work/scratch-pw/............', ##CHANGEME
    'usercache_dir': f'{_paths["gws"]}/cache/users/arjones',  ##CHANGEME
    'work_dir': '/work/scratch-pw/iwi/work.12345',  ##CHANGEME
    'template_file': f'{template_dir}/traj_input.tmpl',
    'met_decl_dir': f'{template_dir}/met_declarations',
})
_paths.update({
    'name_input_dir': '/tmp', ##CHANGEME  # where to put the input file
    'script_dir': f'{_paths["usercache_dir"]}/SimpleTrajectoryRun',
    'utils_dir': f'{_paths["usercache_dir"]}/CommonUtilities',
    'adaqpython_dir': f'{_paths["gws"]}/code/ADAQ_Python_v6.2',
    'nameiii_dir': f'{_paths["gws"]}/code/NAMEIII_v7_2_lotus',
    'topog_dir': f'{_paths["gws"]}/code/NAMEIII_v7_2_lotus/Resources/Topog',
    'met_dir': f'{_paths["work_dir"]}/met_data',    
})
_paths.update({
    'met_restore_script': f'{_paths["utils_dir"]}/MetRestore_JASMIN.sh',
})


input_file_fmt = '{run_label}.txt'
output_dir_fmt = f'{_paths["usercache_dir"]}/NAME_Results_' '{run_label}'


def get_paths(run_name, internal_run_id):

    paths = _paths.copy()
    
    run_label = f'{sanitise_name(run_name)}_{internal_run_id}'

    paths['output_dir'] = output_dir_fmt.format(run_label=run_label)
    paths['input_file'] = os.path.join(paths['name_input_dir'],
                                       input_file_fmt.format(run_label=run_label))

    return paths
