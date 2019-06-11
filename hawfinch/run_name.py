import os, re
import shutil
import subprocess
import time
from datetime import timedelta, datetime
from pynameplot import Name, drawMap, Sum

from .utils import daterange, getjasminconfigs
from .write_inputfile import generate_inputfile
from .write_scriptfile import write_file

def clean_title(title):
    # List of unsafe characters to remove 
    chars_to_remove = [',','(',')']
    # First replace spaces with underscores
    clean_title = title.replace(' ', '_')
    # Remove unsafe characters with regex
    regex_expression = '[' + re.escape(''.join(chars_to_remove)) + ']'
    clean_title = re.sub(regex_expression, '', clean_title)

    return clean_title

def run_name(params, response):
    """
    This is the function to actually run NAME
    :param params: input parameters
    :param response: the WPS response object
    :return: names of the output dir and zipped file
    """
    
    # Remove any unsafe characters
    params['title'] = clean_title(params['title'])

    runtype = 'FWD'
    if params['runBackwards']:
        runtype = 'BCK'

    jasconfigs = getjasminconfigs()

    runtime = datetime.strftime(datetime.now(), '%s')
    params['runid'] = '{}{}_{}_{}_{}'.format(runtype, params['time'], params['timestamp'], params['title'], runtime)

    params['outputdir'] = os.path.join(jasconfigs.get('jasmin', 'outputdir'), params['runid'])

    if not os.path.exists(params['outputdir']):
        os.makedirs(params['outputdir'])
        os.makedirs(os.path.join(params['outputdir'], 'inputs'))
        os.makedirs(os.path.join(params['outputdir'], 'outputs'))
        os.makedirs(os.path.join(params['outputdir'], 'lotus'))

    # Will write a file that lists all the input parameters
    with open(os.path.join(params['outputdir'], 'user_input_parameters.txt'), 'w') as ins:
        for p in sorted(params):
            if p == 'outputdir':
                continue
            ins.write('%s: %s\n' % (p, params[p]))

    # Will loop through all the dates in range, including the final day
    for i, cur_date in enumerate(daterange(params['startdate'], params['enddate'] + timedelta(days=1))):
        os.makedirs(os.path.join(params['outputdir'], 'met_data', 'input{}'.format(i+1)))
        with open(os.path.join(params['outputdir'], 'inputs', 'input{}.txt'.format(i+1)), 'w') as fout:
            fout.write(generate_inputfile(params, cur_date, i+1))

    with open(os.path.join(params['outputdir'], 'script.bsub'), 'w') as fout:
        fout.write(write_file(params, i+1))

    response.update_status('Input files created', 10)

    cat = subprocess.Popen(['cat', os.path.join(params['outputdir'], 'script.bsub')], stdout=subprocess.PIPE)
    runbsub = subprocess.Popen('bsub', stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=cat.stdout)
    sout, serr = runbsub.communicate()
    jobid = sout.split(b' ')[1].replace(b'>', b'').replace(b'<', b'')
    jobrunning = True
    while jobrunning:
        time.sleep(30)
        checkjob = subprocess.check_output('bjobs')
        if jobid in checkjob:
            print('Job %s is still running' % jobid)
            processesrunning = 0
            for l in checkjob.split(b'\n'):
                if jobid in l:
                    processesrunning += 1
            percentcomplete = (((i+1)-processesrunning)/float(i+1))*85
            response.update_status('Running NAME', 10+percentcomplete)
        else:
            jobrunning = False


    

    response.update_status('NAME simulation finished', 95)


    outputs = os.path.join(params['outputdir'], 'outputs')
    # Sum all of the output files and plot them on one plot
    s = Sum(outputs)
    s.sumAll()
    plot_filename = '{}_{}_summed_all.png'.format(s.runname, s.altitude.strip('()'))
    plot_path = os.path.join(outputs, plot_filename)
    drawMap(s, 'total', outfile=plot_path)

    # Zip all the output files into one directory to be served back to the user
    zipped_path = os.path.join(params['outputdir'], params['runid'])
    shutil.make_archive(zipped_path, 'zip', os.path.join(params['outputdir'], 'outputs'))

    return params['runid'], zipped_path, plot_path
