import re
import os
import subprocess
import time

install_root = "/gws/smf/j04/cedaproc/cedawps/swallow/files/"
exe_rel_path = "model/run_name.sh"


def run_name_model(input_file, logdir,
                   version=None,
                   stdout_file='name.stdout',
                   stderr_file='name.stderr',
                   update_status_callback=None,
                   start_percent=0,
                   end_percent=100):

    """
    Run the NAME model using the input file specified.

    For status reporting (using the update_status_callback function),
    the start_percent and end_percent are assumed percentages of the
    overall WPS process during which the model itself runs.
    """
    
    exe_path = get_path(exe_rel_path, version=version)

    stdout_path = os.path.join(logdir, stdout_file)
    stderr_path = os.path.join(logdir, stderr_file)

    with open(stdout_path, 'w') as fout, open(stderr_path, 'w') as ferr:        
        p = subprocess.Popen([exe_path, input_file],
                             stdout=fout, stderr=ferr)
        if update_status_callback:
            numbers_file = get_numbers_file(input_file)
            update_status_callback('NAME model running', start_percent)
            while True:
                new_percent = get_new_percent(numbers_file)
                if new_percent is not None:
                    overall_percent = start_percent + (end_percent - start_percent) * new_percent / 100.
                    update_status_callback('NAME model running', overall_percent)
                try:
                    p.wait(timeout=0)
                except subprocess.TimeoutExpired:
                    pass
                else:
                    break
                time.sleep(1)
            update_status_callback('NAME model finished', end_percent)
        else:
            p.communicate()
        
    return p.returncode, stdout_path, stderr_path


def get_numbers_file(input_file):
    """
    Parse the input file to get the output path, and use it to create a dictionary
    describing the accesses to the numbers file, that can be passed to get_new_percent
    """
    with open(input_file, "r") as f:
        contents = f.read()
    match = re.search("Output Options: *\nFolder *\n(.*?)\n", contents, re.MULTILINE)
    if not match:
        return None
    dirname = match.group(1)

    filename = os.path.join(dirname, "Numbers_C1.txt")

    return {'name': filename,
            'handle': None,
            'last_size': None,
            'contents': ''}


def get_new_percent(nf):
    """
    returns new percentage, or None if it is unchanged
    """
    fh = nf['handle']
    name = nf['name']
    if fh is None:        
        if os.path.exists(name):
            fh = nf['handle'] = open(name)
        else:
            return None
    size = os.path.getsize(name)
    if size == nf['last_size']:
        return None
    nf['contents'] += fh.read()
    nf['last_size'] = size
    
    # parse whole file each time it changes, rather than just the new data
    # (could optimise later, probably not worth it)
    pc = None
    for line in nf['contents'].split("\n"):
        m = re.match("\s*[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2} ...,\s*([0-9.]+),", line)
        if m:
            pc = float(m.group(1))
    return pc


def get_path(relpath, version=None):
    
    if version == None:
        version = sorted(os.listdir(install_root))[-1]

    return os.path.join(install_root, version, exe_rel_path)
