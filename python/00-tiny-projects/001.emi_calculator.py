import pandas as pd
import jinja2
principal = int(input("Principal Amount: "))
rate = float(input("Interest Rate (%): "))
emi = int(input("EMI: "))
print("\nP - Personal Loan\nH - Home Loan\n")
loan_type_pre = input("Loan Type: ")
loan_type = loan_type_pre.lower()
opening_balance = principal
closing_balance = principal
rate_per_month = (rate / 100)/12
months = 1
opening_balance_list = []
rate_per_month_list = []
principal_paid_list = []
interest_paid_list = []
total_emi_list = []
closing_balance_list = []
if loan_type == "h":
    while emi < closing_balance:
        opening_balance_list.append(int(opening_balance))
        interest = opening_balance * rate_per_month
        interest_paid_list.append(int(interest))
        principal_paid = emi - interest
        principal_paid_list.append(int(principal_paid))
        total_emi_list.append(int(principal_paid + interest))
        closing_balance = closing_balance - principal_paid
        closing_balance_list.append(int(closing_balance))
        opening_balance = closing_balance
        rate_per_month_list.append(rate_per_month)

    # Final EMI
    opening_balance_list.append(int(opening_balance))
    rate_per_month_list.append(rate_per_month)
    interest_paid_list.append(int(opening_balance * rate_per_month))
    principal_paid_list.append(int(opening_balance))
    total_emi_list.append(int(opening_balance + interest))
    closing_balance = 0
    closing_balance_list.append(int(closing_balance))

else:
    print("Try Again !!!!!")

df = pd.DataFrame(list(zip(opening_balance_list,rate_per_month_list, principal_paid_list, interest_paid_list, total_emi_list, closing_balance_list)), columns=['Opening Bal', 'Rate', 'Principal Paid', 'Interest', 'EMI', 'Closing Bal'])
blankIndex=[''] * len(df)
df.index=blankIndex
print(df)
print("\n\nOverview\n")
print("Loan Amount: ", principal)
print("Principal Paid:", sum(principal_paid_list))
print("Interest:", sum(interest_paid_list))
years = int(len(principal_paid_list))/12
print("Months:", len(principal_paid_list), f"\nYears: {years:.2f}")
