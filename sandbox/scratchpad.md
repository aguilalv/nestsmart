### Next steps

***

### Potential ideas

- Add possibility to calculate capital gains tax too - Similar approach to income tax
- Change quantities from float to a type that has units and can convert between units (try to remember the library)
- Add flag to invest uniformly during the period
         - One option to make it so that they are spread uniformly across the period divide the returns by 2 - But only the returns on the new investment of that period
- Add incorrect and edge cases to test for generic asset class
- Add possibility of calculating IRR pre and post costs
- Create a portfolio class that orchestrates a series of assets (This class would mantain a list of assets, have a lot of the same methods and return the sum of calling that method for all of its assets, orchestrating for already payed income tax, capital gains tax, etc.)
- Review fees calculation functions so that you only pay fees on what is actually invested and not on balance bop or eop 

***

### Potential technologies / services to use

- Use PostHog to understand how users use the site/app, to run releases to selected groups, to run post usage surveys ...
- https://katalon.com/ for automated testing
- Use hotjar to understand onsite user behaviour
- https://posthog.com/tutorials

***

### Examples and explanations of how things work
- [Example of crystalissing pension](https://heritage-fp.co.uk/pensions/how-pension-drawdown-crystallisation-works/#:~:text=John%20decides%20to%20crystallise%20%C2%A3,pension%2C%20designated%20as%20crystallised%20funds.)
