
def _val_to_str(val, labels, digits=3):
    if val >= 0:
        return f'{round(val,digits)}{labels[0]}'
    else:
        return f'{-round(val,digits)}{labels[1]}'
        
def lon_to_str(longitude, **kwargs):
    return _val_to_str(longitude, 'EW', **kwargs)

def lat_to_str(latitude, **kwargs):
    return _val_to_str(latitude, 'NS', **kwargs)
