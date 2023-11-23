import Asset

def uqpy_wrapper_balances_eop(input, **kwargs):

    asset = Asset.Asset(initial_investment=100,
                  cash_in = [0,0,0],
                  cash_out = [0,0,0],
                  returns = input[0],
                  years = [2000,2001,2002,2003])
                
    return asset.balance_eop
