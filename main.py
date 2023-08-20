# from datapoints.inspire import INSPIRE

# inspire = INSPIRE()
# filename = inspire.download('Birmingham')

# gdf = inspire.open(filename)
# inspire.view(gdf, lambda x: gdf['INSPIREID'][x])

from datapoints.price_paid_data import PricePaidData

ppd = PricePaidData()
path = ppd.download()
data = ppd.open(path)


for row in data[:100]:

    price = int(row[ppd.PRICE])
    if price >= 1000000:
        price = f'{price/1000000:.2f}m'
    elif price >= 1000:
        price = f'{price/1000:.0f}k'

    address = row[ppd.PAON]
    if row[ppd.STREET] != '':
        address += f' {row[ppd.STREET]}'
    if row[ppd.SAON] != '':
        address += f' ({row[ppd.SAON]})'
    area = row[ppd.DISTRICT]
    if area != row[ppd.TOWN]:
        area += f', {row[ppd.TOWN]}'
    if row[ppd.POSTCODE] != '':
        area += f', {row[ppd.POSTCODE]}'
    else:
        area += f', {row[ppd.COUNTY]}'

    print(f'{address}, {area}, sold for £{price}')