"""Tax Bracket Calculator

Here is the break-down on how much a US citizen's income was
taxed in 2019

      $0 - $9,700   10%
  $9,701 - $39,475  12%
 $39,476 - $84,200  22%
 $84,201 - $160,725 24%
$160,726 - $204,100 32%
$204,101 - $510,300 35%
$510,301 +          37%

For example someone earning $40,000 would
pay $4,658.50, not $40,000 x 22% = $8,800!

    9,700.00 x 0.10 =       970.00
   29,775.00 x 0.12 =     3,573.00
      525.00 x 0.22 =       115.50
----------------------------------
              Total =     4,658.50

More detail can be found here:
https://www.nerdwallet.com/blog/taxes/federal-income-tax-brackets/

Sample output from running the code in the if/main clause:

          Summary Report
==================================
 Taxable Income:        40,000.00
     Taxes Owed:         4,658.50
       Tax Rate:           11.65%

         Taxes Breakdown
==================================
    9,700.00 x 0.10 =       970.00
   29,775.00 x 0.12 =     3,573.00
      525.00 x 0.22 =       115.50
----------------------------------
              Total =     4,658.50
"""
from dataclasses import dataclass, field
from typing import List, NamedTuple

Bracket = NamedTuple("Bracket", [("end", int), ("rate", float)])
Taxed = NamedTuple("Taxed", [("amount", float), ("rate", float), ("tax", float)])
BRACKETS = [
    Bracket(9_700, 0.1),
    Bracket(39_475, 0.12),
    Bracket(84_200, 0.22),
    Bracket(160_725, 0.24),
    Bracket(204_100, 0.32),
    Bracket(510_300, 0.35),
    Bracket(510_301, 0.37),
]

@dataclass
class Taxes:
    """Taxes class

    Given a taxable income and optional tax bracket, it will
    calculate how much taxes are owed to Uncle Sam.

    """
    income: float
    bracket: List[Bracket] = field(default_factory=lambda: BRACKETS)
    
    REPORT_LINE_LENGTH = 34

    def __str__(self) -> str:
        """Summary Report

        Returns:
            str -- Summary report

            Example:

                      Summary Report          
            ==================================
             Taxable Income:        40,000.00
                 Taxes Owed:         4,658.50
                   Tax Rate:           11.65%
        """
        LEFT_LENGTH = 16
        RIGHT_LENGTH = 17

        summary = (
            f'{"Summary Report":^{self.REPORT_LINE_LENGTH}}\n'
            f'{"=" * self.REPORT_LINE_LENGTH}\n'
            f'{"Taxable Income:":>{LEFT_LENGTH}}{self.income:>{RIGHT_LENGTH},.2f}\n'
            f'{"Taxes Owed:":>{LEFT_LENGTH}}{self.total:>{RIGHT_LENGTH},.2f}\n'
            f'{"Tax Rate:":>{LEFT_LENGTH}}{self.tax_rate:>{RIGHT_LENGTH-1},.2f}%'
        )
        return summary

    def report(self):
        """Prints taxes breakdown report"""
        print(self)
        print()

        """
                 Taxes Breakdown
        ==================================
            9,700.00 x 0.10 =       970.00
           29,775.00 x 0.12 =     3,573.00
              525.00 x 0.22 =       115.50
        ----------------------------------
                      Total =     4,658.50
        """
        print(f'{"Taxes Breakdown":^{self.REPORT_LINE_LENGTH}}')
        print('=' * self.REPORT_LINE_LENGTH)
        total = self.taxes  # calculate taxes
        for tax in self.tax_amounts:
            print(f'{tax.amount:>12,.2f} x {tax.rate:.2f} = {tax.tax:>12,.2f}')
        print('-' * self.REPORT_LINE_LENGTH)
        print(f'{"Total":>19} = {total:>12,.2f}')


    @property
    def taxes(self) -> float:
        """Calculates the taxes owed

        As it's calculating the taxes, it is also populating the tax_amounts list
        which stores the Taxed named tuples.

        Returns:
            float -- The amount of taxes owed
        """
        def _get_taxed_for_bracket(idx: int) -> Taxed:
            bracket = self.bracket[idx]
            amound_diff_between_brackets = bracket.end - (0 if idx == 0 else self.bracket[idx-1].end)

            if idx < len(self.bracket)-1:
                amount_in_bracket = min(amound_diff_between_brackets, amount)
            else:
                amount_in_bracket = amount
            tax_for_bracket = bracket.rate * amount_in_bracket
            return Taxed(amount=amount_in_bracket, rate=bracket.rate, tax=tax_for_bracket)

        tax_total = 0
        self.tax_amounts = []
        bracket_idx = 0
        amount = self.income
        while amount != 0:
            taxed = _get_taxed_for_bracket(bracket_idx)
            self.tax_amounts.append(taxed)
            amount -= taxed.amount
            tax_total += taxed.tax
            bracket_idx += 1
        return tax_total

    @property
    def total(self) -> float:
        """Calculates total taxes owed

        Returns:
            float -- Total taxes owed
        """
        return self.taxes

    @property
    def tax_rate(self) -> float:
        """Calculates the actual tax rate

        Returns:
            float -- Tax rate
        """
        return round(self.taxes / self.income * 100, 2)


if __name__ == "__main__":
    salary = 40_000
    t = Taxes(salary)
    t.report()