### Next steps

- Ask in Stack Overflow if it is possible to not pass an argument in parametrised test (The goal is to check all required arguments in check for required arguments)


- Change Asset so that outfows is not an input but is calculated (Income + Taxes)
	- A potentially simple way to do this is to maintain the current cash_out variable but instead of filling that directly with the value passed in the constructor, to interpre that value as "required income" and them calculate cash_out as required_income + taxes payable

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
