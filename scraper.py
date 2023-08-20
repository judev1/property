import asyncio
import aiohttp
import re
import zipfile
import random
import os
import io


class INSPIRE:
    """ A class for downloading and managing index polygons spatial data (INSPIRE).

        https://use-land-property-data.service.gov.uk/datasets/inspire
    """

    FILE = 'Land_Registry_Cadastral_Parcels.gml'
    URL = 'https://use-land-property-data.service.gov.uk/datasets/inspire/download/{}.zip'

    @staticmethod
    async def _adownload(session, name, tries=1, timeout=0.1):

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
            async with session.get(INSPIRE.URL.format(filename)) as response:
                data = await response.read()
            with zipfile.ZipFile(io.BytesIO(data)) as zip:
                zip.extractall(f'downloads/temp/{operationid}')
        except zipfile.BadZipFile:
            os.rmdir(f'downloads/temp/{operationid}')
            print(f'Failed to unzip {name}, retrying... ({tries})')
            await asyncio.sleep(timeout*tries)
            return await INSPIRE._adownload(session, name, tries+1)
        except Exception as e:
            print(f'Failed to download {name}, retrying... ({tries})')
            await asyncio.sleep(timeout*tries)
            return await INSPIRE._adownload(session, name, tries+1)

        dir = f'downloads/temp/{operationid}'
        os.rename(f'{dir}/{INSPIRE.FILE}', f'downloads/index_polygons/{filename}.gml')
        os.remove(f'{dir}/INSPIRE Download Licence.pdf')
        os.rmdir(dir)
        return f'downloads/index_polygons/{filename}.gml'

    @staticmethod
    async def afind():
        host = 'https://use-land-property-data.service.gov.uk'
        url = host + '/datasets/inspire/download'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                return re.findall(r'govuk-!-width-four-fifths">\s*(.*?)\s*</', text)

    @staticmethod
    def find() -> list:
        """ Returns a list of names of all index polygons. """
        return asyncio.run(INSPIRE.afind())

    @staticmethod
    async def adownload(name):
        async with aiohttp.ClientSession() as session:
            return await INSPIRE._adownload(session, name)

    @staticmethod
    def download(name: str) -> str:
        """ Downloads the index polygon for the given name and returns the path to the file. """
        return asyncio.run(INSPIRE.adownload(name))

    @staticmethod
    async def adownload_all(names):
        if names is None:
            names = await INSPIRE.afind()
        connector = aiohttp.TCPConnector(force_close=True)
        async with aiohttp.ClientSession(connector=connector) as session:
            return await asyncio.gather(*[INSPIRE._adownload(session, name) for name in names])

    @staticmethod
    def download_all(urls: dict = None) -> list:
        """ Downloads all index polygons and returns a list of paths to the files. """
        return asyncio.run(INSPIRE.adownload_all(urls))

    @staticmethod
    def get(name: str) -> str:
        """ Returns the path to the index polygon for the given name. """
        for file in os.listdir('downloads/index_polygons'):
            if name + '.gml' == file:
                return f'downloads/index_polygons/{file}'

    @staticmethod
    def get_all() -> list:
        """ Returns a list of paths to all index polygon files. """
        files = list()
        for file in os.listdir('downloads/index_polygons'):
            if file.endswith('.gml'):
                files.append(f'downloads/index_polygons/{file}')
        return files