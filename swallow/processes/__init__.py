from .wps_run_name import RunNAME
from .wps_run_name_preset import RunNAMEPreset
from .wps_plot_name import PlotNAME

processes = [
    RunNAME(),
    RunNAMEPreset(),
    PlotNAME(),
]
