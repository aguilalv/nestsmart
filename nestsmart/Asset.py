import numpy as np
import xarray as xr

class Asset:

    # Will probably need a list of dates for which the levels, payments, etc. correspond (Check pendulum)
    
    def __init__(self,initial_investment,cash_in,cash_out, returns, periods):
        self.initial_investment = initial_investment
        self.inflows = cash_in
        self.outflows = cash_out
        self.returns = returns
        self.periods = periods
        self.balance_eop = self._calculate_balances()
 

    def _calculate_balances (self):
    
        ### IMPORTANT NOTE: This calculation assumes infows happen at the begining of the period (to make it so that they are spread uniformly across the period divide the returns by 2 - But only the returns on the new investment of that period-)
        
        initial_investment = self.initial_investment
        cash_in = self.inflows
        cash_out = self.outflows
        returns = self.returns
        periods = self.periods
        
        
        initial_balance = initial_investment
    
        return_pct = xr.DataArray(np.concatenate([[np.nan],returns]), 
                               coords={"period": periods},
                               attrs = {'long_name':'Investment return','units':'%'}
                              )
        inflows = xr.DataArray(np.concatenate([[np.nan],cash_in]), 
                               coords={"period": periods},
                               #attrs = {'long_name':'Cash inflows','units':currency}
                              )
        outflows = xr.DataArray(np.concatenate([[np.nan],cash_out]), 
                               coords={"period": periods},
                               #attrs = {'long_name':'Cash outflows','units':currency}
                              )
        
        balance_eop_tmp = xr.DataArray(np.zeros(len(periods)), 
                                       coords={"period": periods},
                                       #attrs = {'long_name':'Balance at end of period','units':currency}
                                      )
    
        all_cashflows = inflows.copy()
        all_cashflows.loc[periods[0]] = initial_balance
        with xr.set_options(arithmetic_join="outer"):
            all_cashflows += outflows.fillna(0)
    
    
        for (i,period) in enumerate(periods):
            periods_left = len(periods) - i
            tmp = xr.DataArray(np.ones(periods_left) * all_cashflows.loc[period].values, 
                               coords={"period": periods[i:]},
                               #attrs = {'long_name':'Balance at end of period','units':currency}
                              )
        
            with xr.set_options(arithmetic_join="outer"):
                cum_ret = xr.concat([return_pct[:i]*0,(return_pct[i:]+1).cumprod()],'period')
                tmp = tmp * cum_ret
                balance_eop_tmp = balance_eop_tmp + tmp.fillna(0)
    
        return balance_eop_tmp