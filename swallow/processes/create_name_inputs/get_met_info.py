import datetime
import os
import json

met_json_files = {
    'Global': 'mets_global.json',
    #'UK 1.5km': 'mets_uk.json',
    #'Global + UK 1.5km': 'mets_global+uk.json'
}
met_dataset_names = list(met_json_files.keys())


class GetMet:

    def __init__(self, met_dataset):

        met_lookup_file = self._get_met_lookup_file(met_dataset)
        
        dicts = json.loads(open(met_lookup_file).read())

        # convert the dates in each dictionary, and store them in a
        # dictionary (self._met_dicts) using the mark as the primary key
        for d in dicts:
            d['start'] = datetime.datetime(*d['start'])
            if 'end' in d:
                d['end'] = datetime.datetime(*d['end'])
            else:
                d['end'] = None

        self._met_dicts = {self._mark_key(d['mk']): d for d in dicts}
        if len(self._met_dicts) < len(dicts):
            raise ValueError('mk not unique in met info file')

        
    def _mark_key(self, val):
        """
        Convert the mark as given in the JSON file into something that can be used
        as a dictionary key.
        """
        if isinstance(val, list):
            return tuple(val)
        else:
            return val
        

    def _get_met_lookup_file(self, met_dataset):
        
        filename = met_json_files[met_dataset]
        return os.path.join(os.path.dirname(__file__), filename)

    
    def _is_in_time_range(self, met_date, d):
        """
        check if specified date is within the time range described by a 
        single met data description dictionary ; returns a boolean
        """
        if d['end'] == None:
            return d['start'] <= met_date
        else:
            return d['start'] <= met_date < d['end']


    def _get_met_marks_for_time(self, met_date):
        """
        return a set of all met marks for which a specified time is in range
        """
        return {mk for mk, d in self._met_dicts.items()
                if self._is_in_time_range(met_date, d)}
        
        
    def get_met(self, met_date, *extra_met_dates):
        """
        Get dictionary with met data description corresponding to particular date or dates.
        Must be a period which covers all the supplied dates.

        If there are more than one possible, then it will be the one with the highest mark
        """
        marks = self._get_met_marks_for_time(met_date)
        for date in extra_met_dates:
            marks &= self._get_met_marks_for_time(date)
        if not marks:
            raise ValueError('there is no single met data mark covering all requested dates')
        return self._met_dicts[max(marks)]


def get_met_files(params, paths, *times):
    """
    convenience function used by all of the run types, to get the files
    describing the met data that get used in the template
    """
    get_met = GetMet(params['met_data'])
    met_data = get_met.get_met(*times)
    met_decln_file = met_data['decln_filename'].replace('.txt', '.tmpl')
    met_defn_paths = [os.path.join(paths['met_defns_dir'], defn_filename)
                      for defn_filename in met_data['defn_filenames']]
    return met_decln_file, met_defn_paths


if __name__ == '__main__':

    dates = [
        datetime.datetime(2002, 8, 24),
        datetime.datetime(2010, 8, 24),
        datetime.datetime(2011, 8, 24),
        datetime.datetime(2015, 8, 24),
        datetime.datetime(2015, 8, 26),
        datetime.datetime(2015, 9, 24),
        datetime.datetime(2015, 10, 24),
        datetime.datetime(2020, 10, 24),
        datetime.datetime(2021, 10, 24)
    ]

    gm = GetMet()

    for d1 in dates:
        try:
            met_dict = gm.get_met(d1)
            met_info = (f'mk: {met_dict["mk"]} type: {met_dict["type"]} '
                        f'start: {met_dict["start"]} end: {met_dict["end"]}')
        except ValueError:
            met_info = '[none]'
        print(f'{d1} MET DATA {met_info}')
        
        
    for i, d1 in enumerate(dates):
        for d2 in dates[i + 1:]:
            try:
                met_dict = gm.get_met(d1, d2)
                met_info = (f'mk: {met_dict["mk"]} type: {met_dict["type"]} '
                            f'start: {met_dict["start"]} end: {met_dict["end"]}')
            except ValueError:
                met_info = '[none]'
            print(f'{d1} TO {d2} MET DATA {met_info}')
            
