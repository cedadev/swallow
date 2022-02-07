from pywps import (Process, LiteralInput, LiteralOutput,
                   BoundingBoxInput, BoundingBoxOutput, UOM)
from pywps.app.Common import Metadata
#from pywps.validator.mode import MODE

import logging
LOGGER = logging.getLogger("PYWPS")



class SayHello(Process):
    """A nice process saying 'hello'."""
    def __init__(self):

        #-----------------------------------------
        # Note: docs at
        # https://pywps.readthedocs.io/en/latest/api.html
        #
        # and to see allowed values of data_type:
        #   from pywps.inout.literaltypes import LITERAL_DATA_TYPES
        #   print(LITERAL_DATA_TYPES)
        #-----------------------------------------

        inputs = [
            LiteralInput('name', 'Your name',
                         abstract='Please enter your name.',
                         keywords=['name', 'firstname'],
                         data_type='string'
            ),

            LiteralInput('age', 'Your age',
                         abstract='Please enter your age.',
                         data_type='integer'),

            BoundingBoxInput('region', 'The area of interest',
                             crss=['epsg:4326'],
                             dimensions=2),
        ]
        outputs = [
            LiteralOutput('greeting', 'Output response',
                          abstract='A friendly Hello from us.',
                          keywords=['output', 'result', 'response'],
                          data_type='string'),

            LiteralOutput('age_next_birthday', 'Your age',
                          data_type='integer'),

            BoundingBoxOutput('top_right_region',
                              'The north-east quarter of the area of interest',
                              ['epsg:4326'],
                              # mode=MODE.VERYSTRICT
            ),
        ]

        super(SayHello, self).__init__(
            self._handler,
            identifier='RunNAME1',
            title='Say Hello',
            abstract='Just says a friendly Hello.'
                     'Returns literal string output based on the inputs.',
            keywords=['hello', 'demo'],
            metadata=[
                Metadata('PyWPS', 'https://pywps.org/'),
                Metadata('Birdhouse', 'http://bird-house.github.io/'),
                Metadata('PyWPS Demo', 'https://pywps-demo.readthedocs.io/en/latest/'),
                Metadata('Emu: PyWPS examples', 'https://emu.readthedocs.io/en/latest/'),
            ],
            version='1.5',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    @staticmethod
    def _handler(request, response):
        LOGGER.info("say hello")

        name = request.inputs["name"][0].data
        age = request.inputs["age"][0].data
        minx, miny, maxx, maxy = request.inputs["region"][0].data

        midx = (minx + maxx) / 2
        midy = (miny + maxy) / 2

        response.outputs['greeting'].data = (
            f'Hello {name}, your age is {age}, '
            f'your box: minx={minx:.2f} maxx={maxx:.2f} '
            f'miny={miny:.2f} maxy={maxy:.2f}')
        response.outputs['greeting'].uom = UOM('unity')

        response.outputs['age_next_birthday'].data = age + 1
        # Note - using unit "unity" again here.  The available units
        # are restricted and don't include units of time.
        # To see them:  from pywps import OGCUNIT; print(OGCUNIT)
        response.outputs['age_next_birthday'].uom = UOM('unity')

        # The bounding box data is a list: doesn't work with a tuple
        response.outputs['top_right_region'].data = [midx, midy, maxx, maxy]
        response.outputs['top_right_region'].crs = \
            request.inputs['region'][0].crs

        return response
