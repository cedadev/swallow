from pywps import get_ElementMakerForVersion
from pywps.app.basic import get_xpath_ns
from pywps.tests import WpsClient, WpsTestResponse

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
    """Adapted from pywps/tests/test_execute.py
       (including adding support for bounding box data)
    TODO: make this helper method public in pywps."""
    output = {}
    for output_el in xpath_ns(doc, '/wps:ExecuteResponse'
                                   '/wps:ProcessOutputs/wps:Output'):
        identifier_el, = xpath_ns(output_el, './ows:Identifier')
        out_key = identifier_el.text

        try:
            lit_el, = xpath_ns(output_el, './wps:Data/wps:LiteralData')
            output[out_key] = lit_el.text
        except ValueError:
            pass

        try:
            ref_el, = xpath_ns(output_el, './wps:Reference')
            output[out_key] = ref_el.attrib['href']
        except ValueError:
            pass

        try:
            data_el, = xpath_ns(output_el, './wps:Data/wps:ComplexData')
            output[out_key] = data_el.text
        except ValueError:
            pass

        try:
            bbox_el, = xpath_ns(output_el, './wps:Data/wps:BoundingBoxData')
            lower_corner, = xpath_ns(bbox_el, './ows:LowerCorner')
            upper_corner, = xpath_ns(bbox_el, './ows:UpperCorner')
            output[out_key] = ([float(v) for v in lower_corner.text.split()] +
                               [float(v) for v in upper_corner.text.split()])
        except ValueError:
            pass

    return output


def show_tree(el, indent=0):
    "show an XML element tree"
    print(f"{' ' * indent}{el.tag.split('/')[3]}:{el.tag.split('}')[1]} "
          f"= {repr(el.text)}")
    for ch in el.iterchildren():
        show_tree(ch, indent + 4)
