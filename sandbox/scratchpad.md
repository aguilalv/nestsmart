### Next steps

- Change Asset so that outfows is not an input but is calculated (Income + Taxes)
	- In order to do this the asset constructor will need
		- Input of after tax income required from it
		- Income already receivd in that year from other sources (to apply marginal tax rates)
		- Function to calculate income tax (by default assume no income tax)

### Potential ideas

- Change quantities from float to a type that has units and can convert between units (try to remember the library)
- Add flag to invest uniformly during the period
- Add incorrect and edge cases to test for generic asset class
- Add taxes calculations to asset
	- Generic asset always assumes no taxes and sub-classes introduce taxes?
- Add possibility of adding investment costs (at sub-class level?)
- Add possibility of calculating IRR pre and post costs 
