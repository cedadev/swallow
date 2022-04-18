import os
import subprocess

install_root = "/gws/smf/j04/cedaproc/cedawps/swallow/files/"
exe_rel_path = "model/run_name.sh"

def run_name_model(input_file, logdir,
                   version=None,
                   stdout_file='name.stdout',
                   stderr_file='name.stderr'):

    if version == None:
        version = sorted(os.listdir(install_root))[-1]

    exe_path = os.path.join(install_root, version, exe_rel_path)

    stdout_path = os.path.join(logdir, stdout_file)
    stderr_path = os.path.join(logdir, stderr_file)

    with open(stdout_path, 'w') as fout, open(stderr_path, 'w') as ferr:        
        p = subprocess.Popen([exe_path, input_file],
                             stdout=fout, stderr=ferr)
        p.communicate()
        
    return p.returncode, stdout_path, stderr_path
