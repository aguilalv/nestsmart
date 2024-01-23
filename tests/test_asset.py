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
    

#    def test_initial_investment_is_required_argument(self):
#        initial_balance = 100
#        periods = [pendulum.datetime(i,1,1) for i in range(2023,2028)]
#        inf = [0,0,0,0]
#        outf = [0,0,0,0]
#        returns = [0.1,0.05,0.02,0.01]

#        expected_result = xr.DataArray([100,110,115.5,117.81,118.988], coords={'period':periods})

#        with pytest.raises(Exception,match=r"missing 1 required positional argument") as e_info:
#            a = nestsmart.Asset.Asset(
#                  #initial_investment = initial_balance,
#                  cash_in = inf,
#                  after_tax_income = outf,
#                  returns = returns,
#                  periods = periods
#                 )
    
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



#    def test_positive_returns_calculated_correctly_uniform_investment(self):
#        initial_balance = 100
#        #periods = [2023,2024,2025,2026,2027] 
#        periods = [pendulum.datetime(i,1,1) for i in range(2023,2028)]
#        inf = [10,10,5,5]
#        outf = [-2,-2,-1,-1]
#        returns = [0.1,0.05,0.02,0.01]
#
#        expected_result = xr.DataArray([100,118.4,132.52,139.2104,144.6225], coords={'period':periods})
#
#        a = nestsmart.Asset.Asset(initial_investment = initial_balance,
#                  cash_in = inf,
#                  after_tax_income = outf,
#                  returns = returns,
#                  periods = periods,
#                  cashflow_timing='uniform'
#                 )
#
#        result = a.balance_eop
#    
#        xr.testing.assert_allclose(result,expected_result)
#
