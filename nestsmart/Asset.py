import numpy as np
import xarray as xr

class Asset:

    # Function calculates the absolute amount of taxes that need to be paid for marginal income assuming some income has already been taxed
    # signature has to be def marginal_income_tax(self,already_taxed_income,gross_marginal_income):
    marginal_income_tax = None 


    def __init__(self,initial_investment,cash_in,after_tax_income, returns, periods,already_taxed_income=None):
        self.initial_investment = initial_investment
        self.periods = periods
        self.inflows = cash_in
        
        if already_taxed_income == None:
            self.already_taxed_income = [0] * (len(periods)-1)
        else:
            self.already_taxed_income = already_taxed_income
        self.outflows = np.array([-1*i for i in  after_tax_income])
        self.outflows -= np.array(self.marginal_income_tax(self.already_taxed_income,[after_tax_income]))
        self.outflows -= np.array(self.investment_fees())

        self.returns = returns
        self.balance_eop = self._calculate_balances()
 

#    def marginal_income_tax(self,already_taxed_income,gross_marginal_income):
#        '''
#        This function calculates the absolute amount of taxes that need to be paid for marginal income assuming some income has already been taxed
#        '''
#        pass
        #return [0] * len(gross_marginal_income)

    def investment_fees(self):
        return [0] * (len(self.periods)-1)

    def _calculate_balances (self):
        '''
            This calculation assumes:
                - inflows happen in day 1 of each period
                - all income for the year is taken in day 1 of the period (outflow)
                - all income taxes for the year are paid on day 1 of the period (outflow)
                - all fees are paid on day 1 of the period
        '''
        
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
