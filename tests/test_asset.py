import xarray as xr
import pytest
import nestsmart.Asset
import pendulum

#from .context import nestsmart


class TestCalculateEndingBalances():
        
    def mock_zero_income_tax(self,already_taxed_income,gross_marginal_income):
            return [0] * len(gross_marginal_income)

    def mock_constant_income_tax(self,already_taxed_income,gross_marginal_income):
            return [2] * len(gross_marginal_income)

    def mock_constant_income_tax_above_100(self,already_taxed_income,gross_marginal_income):
            mask = [1 if i>100 else 0 for i in already_taxed_income]
            return [2 * i for i in mask]
    
    def mock_constant_fees_2(self):
            return [2,2,2,2]

    @pytest.mark.parametrize(
            "kwargs,expected_balance_eop",
            [
                ({"initial_investment":100,
                    "cash_in":[0,0,0,0],
                    "after_tax_income":[0,0,0,0],
                    "returns":[0.1,0.05,0.02,0.01]},[100,110,115.5,117.81,118.988]),
                ({"initial_investment":0,
                    "cash_in":[0,0,0,0],
                    "after_tax_income":[0,0,0,0],
                    "returns":[0.1,0.05,0.02,0.01]},[0,0,0,0,0]),
                ({"initial_investment":0,
                    "cash_in":[10,5,2,1],
                    "after_tax_income":[0,0,0,0],
                    "returns":[0.1,0.05,0.02,0.01]},[0,11,16.8,19.176,20.3777]),
                ({"initial_investment":0,
                    "cash_in":[0,0,0,0],
                    "after_tax_income":[10,5,2,1],
                    "returns":[0.1,0.05,0.02,0.01]},[0,-11,-16.8,-19.176,-20.3777]),
                ({"initial_investment":100,
                    "cash_in":[10,5,2,1],
                    "after_tax_income":[2,2,1,1],
                    "returns":[0.1,0.05,0.02,0.01]},[100,118.8,127.89,131.467,132.782]),
                ({"initial_investment":100,
                    "cash_in":[10,5,2,1],
                    "after_tax_income":[2,2,1,1],
                    "returns":[0,0,0,0]},[100,108,111,112,112]),
                ({"initial_investment":100,
                    "cash_in":[10,5,2,1],
                    "after_tax_income":[2,2,1,1],
                    "returns":[-0.1,-0.05,-0.02,-0.01]},[100,97.2,95.19,94.266,93.323]),
            ]
    )
    def test_returns_calculated_correctly(self,kwargs,expected_balance_eop,monkeypatch):
        '''
            Note: Current expected_balance_eop assumes new inflows happen on day 1 of each period and income is taken on day 1 of each period 
        '''
        monkeypatch.setattr(nestsmart.Asset.Asset,"marginal_income_tax",self.mock_zero_income_tax)
        
        periods = [pendulum.datetime(i,1,1) for i in range(2023,2028)]

        expected_result = xr.DataArray(expected_balance_eop, coords={'period':periods})

        a = nestsmart.Asset.Asset(
                    **kwargs,
                    periods = periods
                 )

        result = a.balance_eop
    
        xr.testing.assert_allclose(result,expected_result)

    def test_income_tax_taken_as_cash_outflow(self, monkeypatch):
        '''
            Note: Current expected_balance_eop assumes outflows happen on day 1 of each period
        '''

        monkeypatch.setattr(nestsmart.Asset.Asset,"marginal_income_tax",self.mock_constant_income_tax)

        initial_investment = 100
        cash_in = [0,0,0,0]
        after_tax_income = [10,10,10,10]
        returns = [0,0,0,0]
        periods = [pendulum.datetime(i,1,1) for i in range(2023,2028)]

        expected_balance_eop = [100,88,76,64,52]

        expected_result = xr.DataArray(expected_balance_eop, coords={'period':periods})


        a = nestsmart.Asset.Asset(
                    initial_investment = initial_investment,
                    cash_in = cash_in,
                    after_tax_income = after_tax_income,
                    returns = returns,
                    periods = periods
                 )

        result = a.balance_eop
    
        xr.testing.assert_allclose(result,expected_result)

    
    
    @pytest.mark.parametrize(
            "already_taxed_income,expected_balance_eop",
            [([110,110,110,110],[100,88,76,64,52]),
             ([90,90,90,90],[100,90,80,70,60]),
            ]
    )

    def test_income_tax_calculated_on_marginal_income(self, already_taxed_income,expected_balance_eop,monkeypatch):
        '''
            Note: Current expected_balance_eop assumes outflows happen on day 1 of each period
        '''
        monkeypatch.setattr(nestsmart.Asset.Asset,"marginal_income_tax",self.mock_constant_income_tax_above_100)

        initial_investment = 100
        cash_in = [0,0,0,0]
        after_tax_income = [10,10,10,10]
        returns = [0,0,0,0]
        periods = [pendulum.datetime(i,1,1) for i in range(2023,2028)]

        expected_result = xr.DataArray(expected_balance_eop, coords={'period':periods})

        a = nestsmart.Asset.Asset(
                    initial_investment = initial_investment,
                    cash_in = cash_in,
                    after_tax_income = after_tax_income,
                    returns = returns,
                    periods = periods,
                    already_taxed_income = already_taxed_income 
                 )

        result = a.balance_eop
    
        xr.testing.assert_allclose(result,expected_result)

    def test_investment_fees_taken_as_cash_outflow(self, monkeypatch):
        '''
            Note: Current expected_balance_eop assumes fees are taken on day 1 of each period and calculated based on xxx
        '''
        monkeypatch.setattr(nestsmart.Asset.Asset,"marginal_income_tax",self.mock_zero_income_tax)
        monkeypatch.setattr(nestsmart.Asset.Asset,"investment_fees",self.mock_constant_fees_2)

        initial_investment = 100
        cash_in = [0,0,0,0]
        after_tax_income = [0,0,0,0]
        already_taxed_income = [0,0,0,0]
        returns = [0.1,0.1,0.1,0.1]
        periods = [pendulum.datetime(i,1,1) for i in range(2023,2028)]

        expected_result = xr.DataArray([100,107.8,116.38,125.818,136.1998], coords={'period':periods})

        a = nestsmart.Asset.Asset(
                    initial_investment = initial_investment,
                    cash_in = cash_in,
                    after_tax_income = after_tax_income,
                    returns = returns,
                    periods = periods,
                    already_taxed_income = already_taxed_income 
                 )

        result = a.balance_eop
    
        xr.testing.assert_allclose(result,expected_result)

