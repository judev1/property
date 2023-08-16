import geopandas as gp

from scraper import INSPIRE
import gml


# name = 'London Borough of Islington'
# authorities = INSPIRE.find()
# file = INSPIRE.download(name, authorities[name])

INSPIRE.download_all()
file = INSPIRE.get('London Borough of Islington')

gdf = gp.read_file(file, driver="GML")
gml.view(gdf, display=lambda x: gdf['INSPIREID'][x])