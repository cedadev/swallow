import os
import subprocess

adaq_home = '/gws/smf/j04/cedaproc/cedawps/adaq/src/adaq_toolbox-ADAQ_Python_v7.1'

def run_adaq_script(script_name,
                    args=None):

    if args == None:
        args = []
    script_path = os.path.join(adaq_home, 'adaqscripts', script_name)
    cmd = ['python', script_path] + args
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
        
    return p.returncode, stdout, stderr


def run_adaq_scripts(scripts_and_args):

    message = ""
    
    for script, args in scripts_and_args:
        rtn_code, stdout, stderr = run_adaq_script(script, args)
        message += f'''
---- running plotting script {script} ----
script standard output:
{stdout}
script standard error:
{stderr}
return code was: {rtn_code}

'''
    return message
