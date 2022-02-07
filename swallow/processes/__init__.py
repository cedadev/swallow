from .wps_say_hello import SayHello
from .wps_run_name_trajectory import RunNAMETrajectory

processes = [
    SayHello(),
    RunNAMETrajectory(),
]
