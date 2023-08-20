import asyncio
import aiohttp
import re
import zipfile
import random
import os
import io

import geopandas as gp
from matplotlib import pyplot as plt
from shapely.geometry import Point


class INSPIRE:
    """ A class for downloading, managing, and interacting with index polygons spatial data (INSPIRE).

        https://use-land-property-data.service.gov.uk/datasets/inspire
    """

    FILE = 'Land_Registry_Cadastral_Parcels.gml'
    URL = 'https://use-land-property-data.service.gov.uk/datasets/inspire/download/{}.zip'

    async def _adownload(self, session, name, tries=1, timeout=0.1):

        filename = name.replace(' ', '_')
        if os.path.exists(f'downloads/index_polygons/{filename}.gml'):
            return f'downloads/index_polygons/{filename}.gml'

        if not os.path.exists('downloads'):
            os.mkdir('downloads')
        if not os.path.exists('downloads/temp'):
            os.mkdir('downloads/temp')
        if not os.path.exists('downloads/index_polygons'):
            os.mkdir('downloads/index_polygons')
        operationid = str(random.random())[2:]
        while os.path.exists(f'downloads/temp/{operationid}'):
            operationid = str(random.random())[2:]
        os.mkdir(f'downloads/temp/{operationid}')

        try:
            async with session.get(self.URL.format(filename)) as response:
                data = await response.read()
            with zipfile.ZipFile(io.BytesIO(data)) as zip:
                zip.extractall(f'downloads/temp/{operationid}')
        except zipfile.BadZipFile:
            os.rmdir(f'downloads/temp/{operationid}')
            print(f'Failed to unzip {name}, retrying... ({tries})')
            await asyncio.sleep(timeout*tries)
            return await self._adownload(session, name, tries+1)
        except Exception as e:
            print(f'Failed to download {name}, retrying... ({tries})')
            await asyncio.sleep(timeout*tries)
            return await self._adownload(session, name, tries+1)

        dir = f'downloads/temp/{operationid}'
        os.rename(f'{dir}/{self.FILE}', f'downloads/index_polygons/{filename}.gml')
        os.remove(f'{dir}/INSPIRE Download Licence.pdf')
        os.rmdir(dir)
        return f'downloads/index_polygons/{filename}.gml'

    async def afind(self):
        host = 'https://use-land-property-data.service.gov.uk'
        url = host + '/datasets/inspire/download'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                return re.findall(r'govuk-!-width-four-fifths">\s*(.*?)\s*</', text)

    def find(self) -> list:
        """ Returns a list of names of all index polygons. """
        return asyncio.run(self.afind())

    async def adownload(self, name):
        async with aiohttp.ClientSession() as session:
            return await self._adownload(session, name)

    def download(self, name: str) -> str:
        """ Downloads the index polygon for the given name and returns the path to the file. """
        return asyncio.run(self.adownload(name))

    async def adownload_all(self, names):
        if names is None:
            names = await self.afind()
        connector = aiohttp.TCPConnector(force_close=True)
        async with aiohttp.ClientSession(connector=connector) as session:
            return await asyncio.gather(*[self._adownload(session, name) for name in names])

    def download_all(self, urls: dict = None) -> list:
        """ Downloads all index polygons and returns a list of paths to the files. """
        return asyncio.run(self.adownload_all(urls))

    def get(self, name: str) -> str:
        """ Returns the path to the index polygon for the given name. """
        for file in os.listdir('downloads/index_polygons'):
            if name + '.gml' == file:
                return f'downloads/index_polygons/{file}'

    def get_all(self) -> list:
        """ Returns a list of paths to all index polygon files. """
        files = list()
        for file in os.listdir('downloads/index_polygons'):
            if file.endswith('.gml'):
                files.append(f'downloads/index_polygons/{file}')
        return files

    def open(self, path: str) -> gp.GeoDataFrame:
        """ Opens the given index polygon file and returns a GeoDataFrame. """
        return gp.read_file(path, driver="GML")

    def view(self, gdf, display=lambda i: str(i)) -> None:
        """ Displays the given GeoDataFrame in a matplotlib plot. """

        ax = gdf.boundary.plot()
        fig = ax.get_figure()

        info = ax.annotate(
            '', xy=(0,0), xytext=(20,20),
            textcoords='offset points',
            bbox=dict(boxstyle='round', fc='w'),
            arrowprops=dict(arrowstyle='->')
        )
        info.set_visible(False)

        def hover(event):
            visible = info.get_visible()
            if event.inaxes == ax:
                point = Point(event.xdata, event.ydata)
                polygons = gdf['geometry'].contains(point)
                for i, polygon in enumerate(polygons):
                    if polygon:
                        if visible and info.get_text() == str(i):
                            return
                        info.xy = gdf['geometry'][i].centroid.coords[0]
                        info.set_text(display(i))
                        info.set_visible(True)
                        fig.canvas.draw_idle()
                        return
            if visible:
                info.set_visible(False)
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', hover)
        plt.show()