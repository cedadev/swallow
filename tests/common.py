from datetime import datetime, timedelta
import pytz
from dateutil.parser import parse

from pywps import get_ElementMakerForVersion
from pywps.app.basic import get_xpath_ns
from pywps.tests import WpsClient, WpsTestResponse

from swallow.utils import getjasminconfigs

VERSION = "1.0.0"
WPS, OWS = get_ElementMakerForVersion(VERSION)
xpath_ns = get_xpath_ns(VERSION)


class WpsTestClient(WpsClient):

    def get(self, *args, **kwargs):
        query = "?"
        for key, value in kwargs.items():
            query += "{0}={1}&".format(key, value)
        return super(WpsTestClient, self).get(query)


def client_for(service):
    return WpsTestClient(service, WpsTestResponse)


def get_output(doc):
    """Copied from pywps/tests/test_execute.py.
    TODO: make this helper method public in pywps."""
    output = {}
    for output_el in xpath_ns(doc, '/wps:ExecuteResponse'
                                   '/wps:ProcessOutputs/wps:Output'):
        [identifier_el] = xpath_ns(output_el, './ows:Identifier')

        lit_el = xpath_ns(output_el, './wps:Data/wps:LiteralData')
        if lit_el != []:
            output[identifier_el.text] = lit_el[0].text

        ref_el = xpath_ns(output_el, './wps:Reference')
        if ref_el != []:
            output[identifier_el.text] = ref_el[0].attrib['href']

        data_el = xpath_ns(output_el, './wps:Data/wps:ComplexData')
        if data_el != []:
            output[identifier_el.text] = data_el[0].text

    return output

def get_outputs_path(xml):
    jasconfigs = getjasminconfigs()
    output_dir = f"{jasconfigs.get('jasmin', 'outputdir')}/{get_output(xml)['runid']}"
    return output_dir

def get_valid_date(output_type):
    expected_values = test_outputs[output_type]
    release_start_string = expected_values['release_start']
    release_start = parse(release_start_string, dayfirst=True)

    release_end_string = expected_values['release_end']
    release_end = parse(release_end_string, dayfirst=True)

    middle_datetime = release_start + (release_end - release_start)/2
    return datetime.strftime(middle_datetime, "%Y/%m/%d %H:%M")

def get_invalid_date(output_type):
    expected_values = test_outputs[output_type]
    release_start_string = expected_values['release_start']
    release_start = parse(release_start_string, dayfirst=True)

    release_end_string = expected_values['release_end']
    release_end = parse(release_end_string, dayfirst=True)

    middle_datetime = release_start + (release_start - release_end)/2
    return datetime.strftime(middle_datetime, "%Y/%m/%d %H:%M")


def valid_output_file(output_file, output_type):
    expected_values = test_outputs[output_type]

    with open(output_file) as reader:
        output = reader.readlines()

    header = output[0].split()
    if header[0] != ('NAME'):
        print(header[0])
        return False

    run_name = output[1].split()
    if run_name[2] != expected_values['run_name']:
        print(run_name[2])
        return False

    run_time = output[2].split()
    run_datetime_list = run_time[2:]
    run_datetime_string = ' '.join(run_datetime_list)
    run_datetime = parse(run_datetime_string, dayfirst=True)
    if run_datetime - datetime.now(pytz.utc) > timedelta(1):
        print(run_datetime_string)
        return False

    release_start = output[4].split()
    release_start_list = release_start[3:]
    release_start_string = ' '.join(release_start_list)
    if release_start_string != expected_values['release_start']:
        print(release_start_string)
        return False

    release_end = output[5].split()
    release_end_list = release_end[3:]
    release_end_string = ' '.join(release_end_list)
    if release_end_string != expected_values['release_end']:
        print(release_end_string)
        return False

    x_grid_origin = output[10].split()
    if x_grid_origin[3] != expected_values['x_grid_origin']:
        print(x_grid_origin)
        return False

    y_grid_origin = output[11].split()
    if y_grid_origin[3] != expected_values['y_grid_origin']:
        print(y_grid_origin)
        return False

    fields = output[19].split()
    if 'Fields:' not in fields:
        print(output[19])
        return False

    ninth_field = output[28]
    if expected_values['ninth_field'] not in ninth_field:
        print(output[28])
        return False

    data_line_fifty = output[86]
    if data_line_fifty != expected_values['data_line_fifty']:
        print(output[86])
        return False

    if len(output) < expected_values['minimum_lines']:
        print(f'File is only {len(output)} lines long')
        return False

    return True


# Preset test data
cape_verde_inputs = {
    'title': 'Cape Verde',
    'runBackwards': 'true',
    'time': '1',
    'elevationOut': '0-100',
    'resolution': '0.25',
    'startdate': '2017-11-02 00:00:00+00:00',
    'enddate': '2017-11-02 00:00:00+00:00'
}

cape_verde_outputs = {
    'run_name': 'Cape_Verde',
    'release_start': '03/11/2017 00:00 UTC',
    'release_end': '02/11/2017 00:00 UTC',
    'x_grid_origin': '-120.0000',
    'y_grid_origin': '-30.00000',
    'ninth_field': 'No horizontal averaging',
    'data_line_fifty': (
        '                     380,'
        '                     188,'
        '               -25.25000,'
        '                16.75000,'
        '             4.2556094E-06,'
        '             4.5489483E-06,'
        '             4.9342293E-06,'
        '             5.2231912E-06,'
        '             5.1837869E-06,'
        '             6.3790349E-06,'
        '             6.6154576E-06,'
        '             4.8247753E-06,'
        '\n'
    ),
    'minimum_lines': 500
}

bt_tower_inputs = {
    'title': 'BT Tower (150m)',
    'runBackwards': 'false',
    'time': '1',
    'elevationOut': '0-100',
    'resolution': '0.25',
    'startdate': '2018-05-09 00:00:00+00:00',
    'enddate': '2018-05-09 00:00:00+00:00'
}

bt_tower_outputs = {
    'run_name': 'BT_Tower_150m',
    'release_start': '09/05/2018 00:00 UTC',
    'release_end': '10/05/2018 00:00 UTC',
    'x_grid_origin': '-140.0000',
    'y_grid_origin': '20.00000',
    'ninth_field': 'No horizontal averaging',
    'data_line_fifty': (
        '                     558,'
        '                     137,'
        '              -0.7500000,'
        '                54.00000,'
        '             0.0000000E+00,'
        '             0.0000000E+00,'
        '             1.4264937E-08,'
        '             0.0000000E+00,'
        '             0.0000000E+00,'
        '             0.0000000E+00,'
        '             0.0000000E+00,'
        '             0.0000000E+00,'
        '\n'
    ),
    'minimum_lines': 1500
}

preset_test_inputs = [cape_verde_inputs, bt_tower_inputs]

# Custom test data
custom_tokyo_inputs = {
    'title': 'Custom Tokyo Run',
    'longitude': '139.745556',
    'latitude': '35.658611',
    'runBackwards': 'false',
    'time': '1',
    'elevationOut': '0-100',
    'resolution': '0.25',
    'startdate': '2018-02-21 00:00:00+00:00',
    'enddate': '2018-02-21 00:00:00+00:00',
    'min_lon': '100',
    'max_lon': '180',
    'min_lat': '0',
    'max_lat': '90',
    'timestamp': '3-hourly'
}

custom_tokyo_outputs = {
    'run_name': 'Custom_Tokyo_Run',
    'release_start': '21/02/2018 00:00 UTC',
    'release_end': '22/02/2018 00:00 UTC',
    'x_grid_origin': '100.0000',
    'y_grid_origin': '0.0000000E+00',
    'ninth_field': 'No horizontal averaging',
    'data_line_fifty': (
        '                     153,'
        '                     144,'
        '                138.0000,'
        '                35.75000,'
        '             2.5829236E-08,'
        '             4.1326778E-08,'
        '             7.2321868E-08,'
        '             1.9630220E-07,'
        '             2.9445323E-07,'
        '             1.8597046E-07,'
        '             1.9630217E-07,'
        '             6.1990171E-08,'
        '\n'
    ),
    'minimum_lines': 2000
}

custom_egypt_inputs = {
    'title': 'Custom Egypt Run',
    'longitude': '31.134167',
    'latitude': '29.979167',
    'runBackwards': 'true',
    'time': '1',
    'elevationOut': '0-100',
    'resolution': '0.25',
    'startdate': '2019-01-29 00:00:00+00:00',
    'enddate': '2019-01-29 00:00:00+00:00',
    'min_lon': '-180',
    'max_lon': '180',
    'min_lat': '-90',
    'max_lat': '90',
    'timestamp': '3-hourly'
}

custom_egypt_outputs = {
    'run_name': 'Custom_Egypt_Run',
    'release_start': '30/01/2019 00:00 UTC',
    'release_end': '29/01/2019 00:00 UTC',
    'x_grid_origin': '-179.8750',
    'y_grid_origin': '-90.00000',
    'ninth_field': 'No horizontal averaging',
    'data_line_fifty': (
        '                     820,'
        '                     477,'
        '                24.87500,'
        '                29.00000,'
        '             6.3273529E-07,'
        '             2.3487900E-07,'
        '             1.9173797E-08,'
        '             0.0000000E+00,'
        '             0.0000000E+00,'
        '             0.0000000E+00,'
        '             0.0000000E+00,'
        '             0.0000000E+00,'
        '\n'
    ),
    'minimum_lines': 500
}

custom_test_inputs = [custom_tokyo_inputs, custom_egypt_inputs]

test_outputs = {
    'cape_verde': cape_verde_outputs,
    'bt_tower': bt_tower_outputs,
    'custom_tokyo': custom_tokyo_outputs,
    'custom_egypt': custom_egypt_outputs
}
