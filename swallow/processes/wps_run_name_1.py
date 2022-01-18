from swallow.processes._wps_name_base import *


class RunNAME1(NAMEProcessBase):

    IDENTIFIER = "RunNAME1"
    TITLE = "Run NAME 1"
    ABSTRACT = "Extract a subset from the CRU Time Series data"
    KEYWORDS = ["subset", "climate", "research", "unit", "time", "series", "data"]
    METALINK_ID = "subset-cru-ts-result"

    DSET_INFO = {} #get_dset_info(IDENTIFIER)
#    INPUTS_LIST = ["dataset_version", "variable", "timeDateRange", "area", "output_type"]
    INPUTS_LIST = ["area", "output_type"]

    PROCESS_METADATA = [
        Metadata("CEDA WPS UI", "https://ceda-wps-ui.ceda.ac.uk"),
        Metadata("CEDA WPS", "https://ceda-wps.ceda.ac.uk"),
        Metadata("Disclaimer", "https://help.ceda.ac.uk/article/4642-disclaimer"),
    ] #+ [Metadata(name, url) for name, url in DSET_INFO["catalogue_records"].items()]

    def _get_collection(self, inputs):
        dataset_version = self.DSET_INFO["input_datasets"][
            parse_wps_input(inputs, "dataset_version", must_exist=True)
        ]
        variable = self.DSET_INFO["input_variables"][
            parse_wps_input(inputs, "variable", must_exist=True)
        ]

        return f"{dataset_version}.{variable}"

