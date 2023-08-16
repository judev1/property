import asyncio
import aiohttp
import re
import zipfile
import time
import os
import io


class Scraper:

    @staticmethod
    async def _adownload(session, url, ofile, nfile, dir, tries=1, timeout=0.1):
        if os.path.exists(f'{dir}/{nfile}'):
            return f'{dir}/{nfile}'
        try:
            async with session.get(url) as response:
                data = await response.read()
                operationid = str(time.time()).replace('.', '_')
                if not os.path.exists('downloads'):
                    os.mkdir('downloads')
                if not os.path.exists('downloads/temp'):
                    os.mkdir('downloads/temp')
                os.mkdir(f'downloads/temp/{operationid}')
                with zipfile.ZipFile(io.BytesIO(data)) as zip:
                    zip.extractall(f'downloads/temp/{operationid}')
                if not os.path.exists(dir):
                    os.mkdir(dir)
                os.rename(f'downloads/temp/{operationid}/{ofile}', f'{dir}/{nfile}')
                for file in os.listdir(f'downloads/temp/{operationid}'):
                    os.remove(f'downloads/temp/{operationid}/{file}')
                os.rmdir(f'downloads/temp/{operationid}')
                return f'{dir}/{nfile}.gml'
        except zipfile.BadZipFile:
            os.rmdir(f'downloads/temp/{operationid}')
            print(f'Failed to unzip {nfile}, retrying... ({tries})')
            await asyncio.sleep(timeout*tries)
            return await INSPIRE._adownload(session, url, ofile, nfile, dir, tries+1)
        except Exception as e:
            print(f'Failed to download {nfile}, retrying... ({tries})')
            await asyncio.sleep(timeout*tries)
            return await INSPIRE._adownload(session, url, ofile, nfile, dir, tries+1)


class INSPIRE(Scraper):
    """ A class for downloading and managing index polygons spatial data (INSPIRE).

        https://use-land-property-data.service.gov.uk/datasets/inspire
    """

    @staticmethod
    async def afind():
        host = 'https://use-land-property-data.service.gov.uk'
        url = host + '/datasets/inspire/download'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                names = re.findall(r'govuk-!-width-four-fifths">\s*(.*?)\s*</', text)
                links = re.findall(r'<a class="govuk-link"\n\s*href="(.*?)"', text)
                return dict(zip(names, [host + link for link in links]))

    @staticmethod
    def find() -> dict:
        """ Returns a dictionary of index polygon names and their download links. """
        return asyncio.run(INSPIRE.afind())

    @staticmethod
    async def adownload(name, url):
        async with aiohttp.ClientSession() as session:
            ofile = 'Land_Registry_Cadastral_Parcels.gml'
            nfile = name + '.gml'
            dir = 'downloads/index_polygons'
            return await INSPIRE._adownload(session, url, ofile, nfile, dir)

    @staticmethod
    def download(name: str, url: str) -> str:
        """ Downloads the index polygon for the given name. """
        return asyncio.run(INSPIRE.adownload(name, url))

    @staticmethod
    async def adownload_all(urls):
        if urls is None:
            urls = await INSPIRE.afind()
        connector = aiohttp.TCPConnector(force_close=True)
        async with aiohttp.ClientSession(connector=connector) as session:
            ofile = 'Land_Registry_Cadastral_Parcels.gml'
            dir = 'downloads/index_polygons'
            return await asyncio.gather(
                *[INSPIRE._adownload(
                    session, urls[name], ofile, name + '.gml', dir
                ) for name in urls]
            )

    @staticmethod
    def download_all(urls: dict = None) -> list:
        """ Downloads all index polygons. """
        return asyncio.run(INSPIRE.adownload_all(urls))

    @staticmethod
    def get(name: str) -> str:
        """ Returns the path to the index polygon for the given name. """
        for file in os.listdir('downloads/index_polygons'):
            if name + '.gml' == file:
                return f'downloads/index_polygons/{file}'

    @staticmethod
    def get_all() -> list:
        """ Returns a list of paths to all index polygons. """
        files = list()
        for file in os.listdir('downloads/index_polygons'):
            if file.endswith('.gml'):
                files.append(f'downloads/index_polygons/{file}')
        return files