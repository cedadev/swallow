import sys
import re
import os
import subprocess
from PIL import Image

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

    message = ''
    
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


def convert_plots(dirname, new_ext):
    messages = ''    
    for fname in os.listdir(dirname):
        infile = os.path.join(dirname, fname)
        outfile = get_output_filename(infile, new_ext)
        if infile == outfile:
            continue
        try:
            convert_plot(infile, outfile, new_ext)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            messages += f'Caught exception when trying to produce {outfile}: {e}.\n'
        else:
            if not os.path.exists(outfile):
                messages += f'Failed to write {outfile}.\n'
            elif os.path.getsize(outfile) == 0:
                messages += f'{outfile} was empty.\n'
                sys.stderr.write(f'Dummy remove {outfile}')
                #os.remove(outfile)
            else:
                messages += f'Successfully converted {infile} to {outfile}.\n'
                os.remove(infile)
    return messages


def convert_plot(infile, outfile, new_ext):
    if new_ext.lower() == 'pdf':
        convert_to_pdf(infile, outfile)
    else:
        im = Image.open(infile)
        im_rgb = im.convert('RGB')  # remove transparency
        im_rgb.save(outfile, quality=95)
        

def get_output_filename(infile, new_ext):
    m = re.match('^(.*)\.[^\.]+$', infile)
    return f'{m.group(1) if m else infile}.{new_ext}'
        

def convert_to_pdf(infile, outfile,
                   paper_width_cm=21.,
                   paper_height_cm=29.7,
                   margin_cm=2.):

    '''
    Convert image to a PDF file, centred on the page.
    '''
    
    # paper dimensions and minimum margins
    cm_per_inch = 2.54

    pwidth = paper_width_cm / cm_per_inch
    pheight = paper_height_cm / cm_per_inch
    margin = margin_cm / cm_per_inch
    white = (255, 255, 255)

    im = Image.open(infile)
    
    # calculate output resolution
    xsize = pwidth - 2 * margin
    ysize = pheight - 2 * margin
    res = max(im.width / xsize, im.height / ysize)

    # image is written to bottom left of page (no margins), 
    # so calculate number of pixels to pad in each dimension
    # in order to centre the image
    offx = round((pwidth * res - im.width) / 2)
    offy = round((pheight * res - im.height) / 2)

    # create a larger (padded) image
    im_padded = Image.new('RGB',
                          (im.width + offx, im.height + offy),
                          white)
    # offset is from top-left of this area, so 
    im_padded.paste(im, box=(offx, 0))

    # write to file
    im_padded.save(outfile, format='PDF', resolution=res)
