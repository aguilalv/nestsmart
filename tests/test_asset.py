import xarray as xr
import pytest
import nestsmart.Asset
import pendulum

#from .context import nestsmart


class TestCalculateEndingBalances():

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
#                  cash_out = outf,
#                  returns = returns,
#                  periods = periods
#                 )
    
    @pytest.mark.parametrize(
            "kwargs,expected_balance_eop",
            [
                ({"initial_investment":100,
                    "cash_in":[0,0,0,0],
                    "cash_out":[0,0,0,0],
                    "returns":[0.1,0.05,0.02,0.01]},[100,110,115.5,117.81,118.988]),
                ({"initial_investment":0,
                    "cash_in":[0,0,0,0],
                    "cash_out":[0,0,0,0],
                    "returns":[0.1,0.05,0.02,0.01]},[0,0,0,0,0]),
                ({"initial_investment":0,
                    "cash_in":[10,5,2,1],
                    "cash_out":[0,0,0,0],
                    "returns":[0.1,0.05,0.02,0.01]},[0,11,16.8,19.176,20.3777]),
                ({"initial_investment":0,
                    "cash_in":[0,0,0,0],
                    "cash_out":[-10,-5,-2,-1],
                    "returns":[0.1,0.05,0.02,0.01]},[0,-11,-16.8,-19.176,-20.3777]),
                ({"initial_investment":100,
                    "cash_in":[10,5,2,1],
                    "cash_out":[-2,-2,-1,-1],
                    "returns":[0.1,0.05,0.02,0.01]},[100,118.8,127.89,131.467,132.782]),
                ({"initial_investment":100,
                    "cash_in":[10,5,2,1],
                    "cash_out":[-2,-2,-1,-1],
                    "returns":[0,0,0,0]},[100,108,111,112,112]),
                ({"initial_investment":100,
                    "cash_in":[10,5,2,1],
                    "cash_out":[-2,-2,-1,-1],
                    "returns":[-0.1,-0.05,-0.02,-0.01]},[100,97.2,95.19,94.266,93.323]),
            ]
    )
    def test_returns_calculated_correctly(self,kwargs,expected_balance_eop):
        periods = [pendulum.datetime(i,1,1) for i in range(2023,2028)]

        expected_result = xr.DataArray(expected_balance_eop, coords={'period':periods})

        a = nestsmart.Asset.Asset(
                    **kwargs,
                    periods = periods
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
#                  cash_out = outf,
#                  returns = returns,
#                  periods = periods,
#                  cashflow_timing='uniform'
#                 )
#
#        result = a.balance_eop
#    
#        xr.testing.assert_allclose(result,expected_result)
#
