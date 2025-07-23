import os
import string

from .util import sanitise_name

this_dir = os.path.dirname(os.path.realpath(__file__))
template_dir = os.path.join(this_dir, 'templates')

base_dir = '/gws/smf/j04/cedaproc/cedawps/swallow/files/20250325_1'

_paths = {
    'met_decl_dir': f'{template_dir}/met_declarations',
    'utils_dir': f'{base_dir}/utils',
    'met_defns_dir': f'{base_dir}/src/name/Resources/Defns',
    'adaqpython_dir': f'{base_dir}/adaq',
    'topog_dir': f'{base_dir}/topog',
    'model_dir': f'{base_dir}/model',
    'met_dir': '{work_dir}/met_data',
    'input_file': '{work_dir}/{run_label}.txt',
    'output_dir': '{work_dir}/NAME_Results_{run_label}',
}
_paths['met_restore_script'] = f'{_paths["utils_dir"]}/MetRestore_JASMIN.sh'


_paths_by_run_type = {
    'traj': {
        'template_file': f'{template_dir}/traj_input.tmpl',
    },
    'met_extract': {
        'template_file': f'{template_dir}/met_extract_input.tmpl',
    },
    'gen_forward': {
        'template_file': f'{template_dir}/gen_forward_input.tmpl',
    },
    'air_history': {
        'template_file': f'{template_dir}/air_history_input.tmpl',
    },
}



def get_paths(run_name, internal_run_id, work_dir, run_type=None):

    paths = _paths.copy()
    
    if run_type:
        run_name = f'{run_type}_{run_name}'

    run_label = f'{sanitise_name(run_name)}_{internal_run_id}'

    substs = {
        'run_label': run_label,
        'work_dir': work_dir,
        }
    
    paths.update(_paths_by_run_type.get(run_type, {}))

    for k, v in paths.items():
        if '{' in v:
            paths[k] = v.format(**substs)

    return paths
