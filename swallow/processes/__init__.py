from .wps_run_name import RunNAME
from .wps_run_name_preset import RunNamePreset
from .wps_plot_name import PlotNAME

processes = [
    RunNAME(),
    RunNamePreset(),
    PlotNAME(),
]
