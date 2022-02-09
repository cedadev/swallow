

def sanitise_name(name,
                  charset=('abcdefghijklmnopqrstuvwxyz'
                           'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                           '0123456789'
                           '_-.')):

    return ''.join(c if c in charset else '_'
                   for c in name)


def combine_dicts(*dicts):
    all = {}
    for d in dicts:
        all.update(d)
    return all


bool_to_yesno = lambda val: 'Yes' if val else 'No'
