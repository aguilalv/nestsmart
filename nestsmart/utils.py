import Asset

def uqpy_wrapper_balances_eop(input, **kwargs):
    ''' This utility function should know how to interpret the input generated by 
        UQPy and unpack it into a more manageable xarray structure
    '''
    initial_investment = kwargs['initial_investment']
    inflows = kwargs['inflows']
    outflows = kwargs['outflows']
    years = kwargs['years']
    
    asset = Asset.Asset(initial_investment=initial_investment,
                  cash_in = inflows,
                  cash_out = outflows,
                  returns = input[0],
                  years = years)
                
    return asset.balance_eop
