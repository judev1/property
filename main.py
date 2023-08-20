import geopandas as gp

from scraper import INSPIRE
import gml

name = 'London Borough of Islington'
# filename = INSPIRE.download(name)
filename = INSPIRE.get(name)

gdf = gp.read_file(filename, driver="GML")
gml.view(gdf, display=lambda x: gdf['INSPIREID'][x])