from .wps_say_hello import SayHello
from .wps_run_name_trajectory import RunNAMETrajectory
from .wps_extract_met_data import ExtractMetData
from .wps_general_forward_run import GenForwardRun

processes = [
    SayHello(),
    RunNAMETrajectory(),
    ExtractMetData(),
    GenForwardRun(),
]
