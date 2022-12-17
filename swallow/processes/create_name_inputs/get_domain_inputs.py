from .util import is_approx_equal

def get_domain_inputs(params):
    xmin = params['Domain_Xmin']
    xmax = params['Domain_Xmax']
    ymin = params['Domain_Ymin']
    ymax = params['Domain_Ymax']

    is_global = (is_approx_equal(ymin, -90) and
                 is_approx_equal(ymax, 90) and
                 is_approx_equal(xmax - xmin, 360))

    if is_global:
        inputs = { 'UnboundedHorizontal': True }
    else:
        inputs = { 'UnboundedHorizontal': False,
                   'CompDom_Xmin': xmin,
                   'CompDom_Xmax': xmax,
                   'CompDom_Ymin': ymin,
                   'CompDom_Ymax': ymax }

    inputs['CompDom_Zmax'] = params['Domain_Zmax']

    return inputs
