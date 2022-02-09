import datetime
import os
import json


class GetMet:

    def __init__(self, met_lookup_file=None):

        if met_lookup_file == None:
            met_lookup_file = os.path.join(os.path.dirname(__file__),
                                           'mets.json')
        
        dicts = json.loads(open(met_lookup_file).read())
        self._met_lookup = [(datetime.datetime(*d['start']), d) for d in dicts]
        self._met_lookup.sort()


    def get_met(self, met_date):
        """
        get dictionary with met data description corresponding to particular date
        """
        met_info = None
        for start, dct in self._met_lookup:
            if met_date >= start:
                met_info = dct
            else:
                break
        if met_info == None:
            raise ValueError('date is before the earliest available Global met data')
        return met_info

    
    def get_met2(self, run_start_time, run_stop_time):
        """
        get met description dictionary for two dates, 
        also checking that they are both the same
        """
        run_start_met = self.get_met(run_start_time)
        run_stop_met = self.get_met(run_stop_time)
        if run_start_met['mk'] == run_stop_met['mk']:
            return run_start_met
        else:
            raise ValueError("start and stop times of the NAME run do not use the same 'Mk' Global met data")

