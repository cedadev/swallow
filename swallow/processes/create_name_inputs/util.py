import datetime
import string

#from jinja2 import Template
from jinja2 import Environment, FileSystemLoader


def sanitise_string(s, charset, filler='_'):
    return ''.join(c if c in charset else filler
                   for c in s)
    
def sanitise_description(description):
    charset = set(string.printable).difference(',\t')
    return sanitise_string(description, charset)

def sanitise_name(name):
    charset=(string.ascii_letters + string.digits + '_-.')
    return sanitise_string(name, charset)


def combine_dicts(*dicts):
    all = {}
    for d in dicts:
        all.update(d)
    return all


bool_to_yesno = lambda val: 'Yes' if val else 'No'


def render_template(template_file, data, include_paths=None, rendered_file=None):
    if include_paths == None:
        include_paths = []
    template_str = open(template_file).read()    
    template = Environment(loader=FileSystemLoader(include_paths)).from_string(template_str)
    rendered = template.render(**data)

    if rendered_file:
        with open(rendered_file, 'w') as f:
            f.write(rendered)

    return rendered


def get_times(start_time, num_hours, direction='Forward'):

    multipliers = {'Forward': 1,
                   'Backward': -1}

    hour_offset = datetime.timedelta(hours=1) * multipliers[direction]

    stop_time = start_time + hour_offset * num_hours
    time_after_first_hour = start_time + hour_offset

    return start_time, stop_time, time_after_first_hour
