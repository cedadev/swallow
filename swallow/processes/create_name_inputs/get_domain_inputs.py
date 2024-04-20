from .util import is_approx_equal

def get_domain_inputs(params):
    xmin = params['Domain_Xmin']
    xmax = params['Domain_Xmax']
    ymin = params['Domain_Ymin']
    ymax = params['Domain_Ymax']

    inputs = {}

    if is_approx_equal(min(xmax - xmin, 360), 360):
        inputs.update({'X_Unbounded': True})
    else:
        inputs.update({'X_Unbounded': False,
                       'CompDom_Xmin': xmin,
                       'CompDom_Xmax': xmax})
    
    if (is_approx_equal(ymin, -90) and
        is_approx_equal(ymax, 90)):
        inputs.update({'Y_Unbounded': True})
    else:
        inputs.update({'Y_Unbounded': False,
                       'CompDom_Ymin': ymin,
                       'CompDom_Ymax': ymax})

    inputs['CompDom_Zmax'] = params['Domain_Zmax']

    return inputs
