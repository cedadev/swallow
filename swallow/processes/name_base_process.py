from pywps import Process

_stations = {
    'Auchencorth Moss': (-3.347222328, 55.88333511),
    'BT Tower (150m)': (-0.13888, 51.5215),
    'Bachok: (Malaysia)': (102.425, 6.009),
    'Beijing Pinggu': (117.0406996, 40.1659),
    'Beijing Tower': (116.377, 39.975),
    'Cape Fuguei (Taiwan)': (121.538, 25.297),
    'Cape Verde': (-24.867222, 16.863611),
    'Chilbolton Observatory': (-1.438228000, 51.14961700),
    'Coyhaique': (-72.049977,  -45.578936),
    'Delhi (Kashmere gate)': (77.23184, 28.6644),
    'Halley': (26.16667, -75.58333),
    'Hanoi (Vietnam)': (105.4902, 21.0024),
    'Harwell': (-1.326666594, 51.57110977),
    'Ho Chi Minh City (Vietnam)': (106.4057, 10.4544),
    'Mace Head': (-9.938888550, 53.41388702),
    'North Kensington': (-0.213333338, 51.52111053),
    'Penlee (PML)': (-4.1931, 50.3189),
    'Weybourne': (1.1219, 52.9503)
}


class NAMEBaseProcess(Process):
    
    _stations = _stations  # add as class variable

        
    def _get_request_internal_id(self):
        # FIXME: is there any kind of request ID in the request? 
        # (I didn't find one.)
        return f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{os.getpid()}'


    def _get_input(self, request, key, multi=False, default=None):

        inputs = request.inputs.get(key)

        if inputs == None:
            return default
        
        if multi:
            return [inp.data for inp in inputs]
        else:
            inp, = inputs
            return inp.data
