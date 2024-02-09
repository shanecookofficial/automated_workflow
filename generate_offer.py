import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv(input(r"Filepath: ").replace('"',''))
df['TCG Marketplace Price'] = df['TCG Low Price With Shipping'] - 1

sales_price = df['TCG Marketplace Price'].sum()
margins = [.25,.225,.2]
offers = []

for margin in margins:
    offers.append(round(-1 * ((margin * sales_price) - sales_price) - (sales_price * .1275), 2))

for offer in range(len(offers)):
    offers[offer] = (offers[offer], f'{round((offers[offer]/sales_price) * 100, 2)}%')

print(round(sales_price, 2))
print(offers)