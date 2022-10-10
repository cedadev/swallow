from .wps_run_name_trajectory import RunNAMETrajectory
from .wps_extract_met_data import ExtractMetData
from .wps_general_forward_run import GenForwardRun
from .wps_air_history_run import AirHistoryRun

processes = [
    RunNAMETrajectory(),
    ExtractMetData(),
    GenForwardRun(),
    AirHistoryRun(),
]
