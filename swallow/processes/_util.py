
def _val_to_str(val, labels):
    if val >= 0:
        return f'{val}{labels[0]}'
    else:
        return f'{-val}{labels[1]}'
        
def lon_to_str(longitude):
    return _val_to_str(longitude, 'EW')

def lat_to_str(latitude):
    return _val_to_str(latitude, 'NS')
