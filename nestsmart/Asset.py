import numpy as np
import xarray as xr

class Asset:

    def __init__(self,initial_investment,cash_in,after_tax_income, returns, periods,already_taxed_income=None):
        self.initial_investment = initial_investment
        self.inflows = cash_in
        if already_taxed_income == None:
            self.already_taxed_income = [0] * (len(periods)-1)
        else:
            self.already_taxed_income = already_taxed_income
        self.outflows = np.array([-1*i for i in  after_tax_income])
        self.outflows -= np.array(self.marginal_income_tax(self.already_taxed_income,[after_tax_income]))
        self.returns = returns
        self.periods = periods
        self.balance_eop = self._calculate_balances()
 

    def marginal_income_tax(self,already_taxed_income,gross_marginal_income):
        '''
        This function calculates the absolute amount of taxes that need to be paid for marginal income assuming some income has already been taxed
        '''
        pass
        #return [0] * len(gross_marginal_income)

        

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
