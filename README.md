# property
This project aggregates data from the UK government's [use land property data](https://use-land-property-data.service.gov.uk/) service. The program is modular with the intention to port the datapoints later to a model of some description. Currently, only functionality to scrape, download, and view the INSPIRE polygons and Price Paid Data has been implemented.

## INSPIRE polygons

Get a list of available authorities

```py
from datapoints.inspire import INSPIRE

authorities = INSPIRE().find()
```

Download INSPIRE polygons for a specific authority

```py
from datapoints.inspire import INSPIRE

name = 'London Borough of Islington'
path = INSPIRE().download(name)
```

Download the INSPIRE POLYGONS for all available authorities

```py
from datapoints.inspire import INSPIRE

paths = INSPIRE().download_all()
```

Get the locally stored file for an authority and view it

```py
from datapoints.inspire import INSPIRE

inspire = INSPIRE()
path = inspire.get('London Borough of Islington')

gdf = inspire.open(path)
inspire.view(gdf, lambda x: gdf['INSPIREID'][x])
```

## Price Paid Data

Download Price Paid Data for the last month (updated on the 20th buisness day of each month).

```py
from datapoints.price_paid_data import PricePaidData

path = PricePaidData().download()
```

Download Price Paid Data for a specific year (default last).

```py
from datapoints.price_paid_data import PricePaidData

path = PricePaidData().download_year(1996)
```

Get the locally stored file for the last month of Price Paid data and open it.

```py
from datapoints.price_paid_data import PricePaidData

ppd = PricePaidData()
data = ppd.open(ppd.get())
```

## Notice

This project uses data from index polygons spatial data (INSPIRE) dataset and the Price Paid Data dataset.

This data is protected under the (Open Government Licence)[https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/] which grants the user "a worldwide, royalty-free, perpetual, non-exclusive licence to use the Information."

> This information is subject to Crown copyright and database rights [year of supply or date of publication] and is reproduced with the permission of HM Land Registry.

> The polygons (including the associated geometry, namely x, y co-ordinates) are subject to Crown copyright and database rights [year of supply or date of publication] Ordnance Survey 100026316.

> Contains HM Land Registry data © Crown copyright and database right 2021. This data is licensed under the Open Government Licence v3.0.

Additionally, Price Paid Data contains address data processed against Ordnance Survey’s AddressBase Premium product, which incorporates Royal Mail’s PAF® database (Address Data).

Royal Mail and Ordnance Survey permits use of Address Data in the Price Paid Data:

> for personal and/or non-commercial use
> to display for the purpose of providing residential property price information services