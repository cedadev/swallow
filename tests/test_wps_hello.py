from pywps import Service
from pywps.tests import client_for, assert_response_success

from .common import get_output, show_tree
from swallow.processes.wps_say_hello import SayHello


def test_wps_hello():
    #
    # Testing a process with 3 inputs and 3 outputs.
    #
    # inputs are "name" (LiteralInput, data type 'string')
    #            "age" (LiteralInput, data type 'int')
    #            "region" (BoundingBoxInput)
    #
    # outputs are "greeting" (LiteralOutput, data type 'string')
    #             "age_next_birthday" (LiteralOutput, data type 'int')
    #             "top_right_region" (BoundingBoxOutput)
    #
    # "output" consists of a string which includes all of the inputs
    # "age_next_birthday" is the input age + 1
    # "top_right_region" is a bounding box consisting of the top-right quarter
    #                    of the input bounding box

    client = client_for(Service(processes=[SayHello()]))

    #                                       X0 Y0  X1 Y1
    datainputs = "name=LovelySugarBird;region=80,30,100,40;age=18"
    resp = client.get(
        "?service=WPS&request=Execute&version=1.0.0&identifier=hello"
        f"&datainputs={datainputs}")

    # check outputs
    outputs = get_output(resp.xml)

    #====================
    # dump some things to stdout:
    #   to see this run pytest with the "-s" option to disable output capture
    #   e.g.   python -m pytest -W ignore -s tests
    show_tree(resp.xml)
    print(outputs)
    #====================

    assert_response_success(resp)

    assert outputs == {
        'greeting': ('Hello LovelySugarBird, '
                     'your age is 18, '
                     'your box: minx=80.00 maxx=100.00 miny=30.00 maxy=40.00'),
        'age_next_birthday': '19',
        'top_right_region': [90., 35., 100., 40.]
    }
