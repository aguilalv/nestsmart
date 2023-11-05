import numpy as np
import xarray as xr

class Asset:

    # Will probably need a list of dates for which the levels, payments, etc. correspond (Check pendulum)
    
    def __init__(self,initial_investment,cash_in,cash_out, returns, years):
        self.initial_investment = initial_investment
        self.inflows = cash_in
        self.outflows = cash_out
        self.returns = returns
        self.years = years
        self.balance_eop = self._calculate_balances()
 

    def _calculate_balances (self):
    
        ### IMPORTANT NOTE: This calculation assumes infows happen at the begining of the year (to make it so that they are spread uniformly across the year divide the returns by 2 - But only the returns on the new investment of that year-)
        
        initial_investment = self.initial_investment
        cash_in = self.inflows
        cash_out = self.outflows
        returns = self.returns
        years = self.years
        
        
        initial_balance = initial_investment
    
        return_pct = xr.DataArray(np.concatenate([[np.nan],returns]), 
                               coords={"year": years},
                               attrs = {'long_name':'Investment return','units':'%'}
                              )
        inflows = xr.DataArray(np.concatenate([[np.nan],cash_in]), 
                               coords={"year": years},
                               #attrs = {'long_name':'Cash inflows','units':currency}
                              )
        outflows = xr.DataArray(np.concatenate([[np.nan],cash_out]), 
                               coords={"year": years},
                               #attrs = {'long_name':'Cash outflows','units':currency}
                              )
        
        balance_eop_tmp = xr.DataArray(np.zeros(len(years)), 
                                       coords={"year": years},
                                       #attrs = {'long_name':'Balance at end of period','units':currency}
                                      )
    
        all_cashflows = inflows.copy()
        all_cashflows.loc[years[0]] = initial_balance
        with xr.set_options(arithmetic_join="outer"):
            all_cashflows += outflows.fillna(0)
    
    
        for (i,year) in enumerate(years):
            years_left = len(years) - i
            tmp = xr.DataArray(np.ones(years_left) * all_cashflows.loc[year].values, 
                               coords={"year": years[i:]},
                               #attrs = {'long_name':'Balance at end of period','units':currency}
                              )
        
            with xr.set_options(arithmetic_join="outer"):
                cum_ret = xr.concat([return_pct[:i]*0,(return_pct[i:]+1).cumprod()],'year')
                tmp = tmp * cum_ret
                balance_eop_tmp = balance_eop_tmp + tmp.fillna(0)
    
        return balance_eop_tmp