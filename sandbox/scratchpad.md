### Next steps


### Potential ideas

- Add possibility to calculate capital gains tax too - Similar approach to income tax
- Change quantities from float to a type that has units and can convert between units (try to remember the library)
- Add flag to invest uniformly during the period
         - One option to make it so that they are spread uniformly across the period divide the returns by 2 - But only the returns on the new investment of that period
- Add incorrect and edge cases to test for generic asset class
- Add possibility of calculating IRR pre and post costs
- Create a portfolio class that orchestrates a series of assets (This class would mantain a list of assets, have a lot of the same methods and return the sum of calling that method for all of its assets, orchestrating for already payed income tax, capital gains tax, etc.)
- Review fees calculation functions so that you only pay fees on what is actually invested and not on balance bop or eop 
