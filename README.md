# property
This project aggregates data from the UK government's [use land property data](https://use-land-property-data.service.gov.uk/) service. The program is modular with the intention to port the datapoints later to a model of some description. Currently, only functionality to scrape, download, and view the INSPIRE polygons has been implemented.

## INSPIRE polygons

Get a list of available authorities

```py
from scraper import INSPIRE

authorities = INSPIRE.find()
```

Download INSPIRE polygons for a specific authority

```py
from scraper import INSPIRE

name = 'London Borough of Islington'
authorities = INSPIRE.find()
file = INSPIRE.download(name, authorities[name])
```

Download the INSPIRE POLYGONS for all available authorities

```py
from scraper import INSPIRE

INSPIRE.download_all()
```

Get the locally stored file for an authority and view it

```py
import geopandas as gp

from scraper import INSPIRE
import gml

file = INSPIRE.get('London Borough of Islington')
gdf = gp.read_file(file, driver="GML")
gml.view(gdf, display=lambda x: gdf['INSPIREID'][x])
```

## Notice

This project uses data from index polygons spatial data (INSPIRE) dataset, which is protected under the (Open Government Licence)[https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/] which grants the user "a worldwide, royalty-free, perpetual, non-exclusive licence to use the Information," on the condition that when reusing the data, an acknowledgement of the source of the data is made:

> This information is subject to Crown copyright and database rights [year of supply or date of publication] and is reproduced with the permission of HM Land Registry.

And when resuing the polygons, the following Ordnance Survey attributing statement be displayed:

> The polygons (including the associated geometry, namely x, y co-ordinates) are subject to Crown copyright and database rights [year of supply or date of publication] Ordnance Survey 100026316.