import xarray as xr
import pytest
import nestsmart.Asset
#from .context import nestsmart


class TestCalculateEndingBalances():

    def test_returns_from_initial_investment_calculated_correctly(self):
        initial_balance = 100
        years = [2023,2024,2025,2026,2027]
        inf = [0,0,0,0]
        outf = [0,0,0,0]
        returns = [0.1,0.05,0.02,0.01]

        expected_result = xr.DataArray([100,110,115.5,117.81,118.988], coords={'year':years})


        a = nestsmart.Asset.Asset(initial_investment = initial_balance,
                  cash_in = inf,
                  cash_out = outf,
                  returns = returns,
                  years = years
                 )

        result = a.balance_eop
    
        xr.testing.assert_allclose(result,expected_result)

    def test_returns_from_inflows_calculated_correctly(self):
        initial_balance = 0
        years = [2023,2024,2025,2026,2027]
        inf = [10,5,2,1]
        outf = [0,0,0,0]
        returns = [0.1,0.05,0.02,0.01]

        expected_result = xr.DataArray([0,11,16.8,19.176,20.3777], coords={'year':years})

        a = nestsmart.Asset.Asset(initial_investment = initial_balance,
                  cash_in = inf,
                  cash_out = outf,
                  returns = returns,
                  years = years
                 )

        result = a.balance_eop
    
        xr.testing.assert_allclose(result,expected_result)

    def test_returns_from_outflows_calculated_correctly(self):
        initial_balance = 0
        years = [2023,2024,2025,2026,2027]
        inf = [0,0,0,0]
        outf = [-10,-5,-2,-1]
        returns = [0.1,0.05,0.02,0.01]

        expected_result = xr.DataArray([0,-11,-16.8,-19.176,-20.3777], coords={'year':years})

        a = nestsmart.Asset.Asset(initial_investment = initial_balance,
                  cash_in = inf,
                  cash_out = outf,
                  returns = returns,
                  years = years
                 )

        result = a.balance_eop
    
        xr.testing.assert_allclose(result,expected_result)    

    def test_positive_returns_calculated_correctly(self):
        initial_balance = 100
        years = [2023,2024,2025,2026,2027]
        inf = [10,5,2,1]
        outf = [-2,-2,-1,-1]
        returns = [0.1,0.05,0.02,0.01]

        expected_result = xr.DataArray([100,118.8,127.89,131.467,132.782], coords={'year':years})

        a = nestsmart.Asset.Asset(initial_investment = initial_balance,
                  cash_in = inf,
                  cash_out = outf,
                  returns = returns,
                  years = years
                 )

        result = a.balance_eop
    
        xr.testing.assert_allclose(result,expected_result)

    def test_negative_returns_calculated_correctly(self):
        initial_balance = 100
        years = [2023,2024,2025,2026,2027]
        inf = [10,5,2,1]
        outf = [-2,-2,-1,-1]
        returns = [-0.1,-0.05,-0.02,-0.01]

        expected_result = xr.DataArray([100,97.2,95.19,94.266,93.323], coords={'year':years})

        a = nestsmart.Asset.Asset(initial_investment = initial_balance,
                  cash_in = inf,
                  cash_out = outf,
                  returns = returns,
                  years = years
                 )

        result = a.balance_eop
    
        xr.testing.assert_allclose(result,expected_result)

    def test_zero_returns_calculated_correctly(self):
        initial_balance = 100
        years = [2023,2024,2025,2026,2027]
        inf = [10,5,2,1]
        outf = [-2,-2,-1,-1]
        returns = [0,0,0,0]

        expected_result = xr.DataArray([100,108,111,112,112], coords={'year':years})

        a = nestsmart.Asset.Asset(initial_investment = initial_balance,
                  cash_in = inf,
                  cash_out = outf,
                  returns = returns,
                  years = years
                 )

        result = a.balance_eop
    
        xr.testing.assert_allclose(result,expected_result)
