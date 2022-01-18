import os

from pywps import (
    BoundingBoxInput,
    LiteralInput,
    Process,
    FORMATS,
    Format,
    ComplexOutput,
)
from pywps.app.Common import Metadata
from pywps.app.exceptions import ProcessError



class NAMEProcessInputFactory:
    """
    Factory class for returning a list of WPS Input objects.
    These are wrapped in methods so that they only get evaluated
    if they are required. This avoids error checking for inputs
    that are not used by some sub-classes.
    """

    def __init__(self, dset_info):
        self.DSET_INFO = dset_info

    def get_inputs(self, input_keys):
        inputs = [self._lookup(key) for key in input_keys]
        return inputs

    def _lookup(self, key):
        method = getattr(self, f"_get_input_{key}")
        return method()

    def _get_input_dataset_version(self):
        return LiteralInput(
            "dataset_version",
            "Dataset Version",
            abstract="The dataset to subset",
            data_type="string",
            allowed_values=list(self.DSET_INFO["input_datasets"].keys()),
            min_occurs=1,
            max_occurs=1,
        )

    def _get_input_variable(self):
        return LiteralInput(
            "variable",
            "Variable",
            abstract="The variable to subset",
            data_type="string",
            allowed_values=list(self.DSET_INFO["input_variables"].keys()),
            min_occurs=1,
        )

    def _get_input_frequency(self):
        return LiteralInput(
            "frequency",
            "Frequency",
            abstract="The temporal frequency to subset",
            data_type="string",
            allowed_values=list(self.DSET_INFO["input_frequencies"].keys()),
            min_occurs=1,
        )

    def _get_input_spatial_average(self):
        return LiteralInput(
            "spatial_average",
            "Spatial Average",
            abstract="The spatial average (resolution) to subset",
            data_type="string",
            allowed_values=list(self.DSET_INFO["input_spatial_averages"].keys()),
            min_occurs=1,
        )

    def _get_input_timeDateRange(self):
        return LiteralInput(
            "timeDateRange",
            "Time Period",
            abstract="The time period to subset over.",
            data_type="string",
            default=self.DSET_INFO["time_range"],
            min_occurs=0,
            max_occurs=1,
        )

    def _get_input_area(self):
        return BoundingBoxInput(
            "area",
            "Area",
            abstract="The area to subset over.",
            crss=["-180.0, -90.0, 180.0, 90.0,epsg:4326"],
            min_occurs=0,
            max_occurs=1,
        )

    def _get_input_output_type(self):
        return LiteralInput(
            "output_type",
            "Output Format",
            abstract="The file format required for you output data.",
            data_type="string",
            allowed_values=["netcdf", "csv"],
            min_occurs=1,
            max_occurs=1,
        )
    

class NAMEProcessBase(Process):

    # REQUIRED class properties:
    #  IDENTIFIER = str
    #  TITLE = str
    #  ABSTRACT = str
    #  KEYWORDS = [list]
    #  METALINK_ID = str
    #  DSET_INFO = str
    #  INPUTS_LIST = [list]
    #  PROCESS_METADATA = [list]

    def __init__(self):

        inputs = self._define_inputs()
        outputs = self._define_outputs()

        super(NAMEProcessBase, self).__init__(
            self._handler,
            identifier=self.IDENTIFIER,
            title=self.TITLE,
            abstract=self.ABSTRACT,
            keywords=self.KEYWORDS,
            metadata=self.PROCESS_METADATA,
            version="1.0.0",
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True,
        )

    def _define_inputs(self):
        inputs = NAMEProcessInputFactory(self.DSET_INFO).get_inputs(self.INPUTS_LIST)
        return inputs

    def _define_outputs(self):
        outputs = [
            ComplexOutput(
                "prov",
                "Provenance",
                abstract="Provenance document using W3C standard.",
                as_reference=True,
                supported_formats=[FORMATS.JSON],
            )
        ]

        return outputs

    def _get_collection(self, inputs):
        raise NotImplementedError()

    def _handler(self, request, response):
        return response

