import geopandas as gp

from scraper import INSPIRE
import gml

name = 'London Borough of Islington'
# authorities = INSPIRE.find()
# filename = INSPIRE.download(name, authorities[name])
filename = INSPIRE.get(name)

gdf = gp.read_file(filename, driver="GML")
gml.view(gdf, display=lambda x: gdf['INSPIREID'][x])