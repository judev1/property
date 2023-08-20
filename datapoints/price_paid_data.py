import asyncio
import aiohttp
import os
import time
import csv


class PricePaidData:
    """ A class for downloading and managing with Price Paid Data.

        https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads
    """

    ID = 0
    PRICE = 1
    DATE = 2
    POSTCODE = 3
    PROPERTY_TYPE = 4
    NEW_TYPE = 5
    ESTATE_TYPE = 6
    PAON = 7 # Primary Addressable Object Name
    SAON = 8 # Secondary Addressable Object Name
    STREET = 9
    LOCALITY = 10
    TOWN = 11
    DISTRICT = 12
    COUNTY = 13
    TRANSACTION = 14
    RECORD_STATUS = 15

    PROPERTY_TYPES = {
        'D': 'Detached',
        'S': 'Semi-Detached',
        'T': 'Terraced',
        'F': 'Flat/Maisonette',
        'O': 'Other'
    }

    NEW_TYPES = {
        'Y': True, # New build
        'N': False # Old build
    }

    ESTATE_TYPES = {
        'F': 'Freehold',
        'L': 'Leasehold',
        'U': 'Unknown'
    }

    TRANSACTION_TYPES = {
        'A': 'Standard price paid transaction', # Single residential property sold for full market value to private individual
        'B': 'Additional price paid transaction' # Repossessions, Buy-to-lets and transfers of property sold to non-private individuals
    }

    RECORD_STATUSES = {
        'A': 'Added',
        'C': 'Changed',
        'D': 'Deleted'
    }

    URL = 'http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-{}.txt'

    async def adownload(self, version):

        if os.path.exists(f'downloads/price_paid_data/{version}.csv'):
            return f'downloads/price_paid_data/{version}.csv'

        if not os.path.exists('downloads'):
            os.mkdir('downloads')
        if not os.path.exists('downloads/price_paid_data'):
            os.mkdir('downloads/price_paid_data')

        async with aiohttp.ClientSession() as session:
            print(PricePaidData.URL.format(version))
            async with session.get(PricePaidData.URL.format(version)) as response:
                data = await response.read()
        with open(f'downloads/price_paid_data/{version}.csv', 'wb') as file:
            file.write(data)

        return f'downloads/price_paid_data/{version}.csv'

    def download(self) -> str:
        """ Downloads the monthly updated Price Paid Data and returns the path to the file. """
        return asyncio.run(self.adownload('monthly-update'))

    def download_complete(self) -> str:
        """ Downloads the complete Price Paid Data and returns the path to the file. """
        return asyncio.run(self.adownload('complete'))

    def download_year(self, year: int = None) -> str:
        """ Downloads the Price Paid Data for the given year and returns the path to the file. """
        if year is None:
            year = time.localtime().tm_year - 1
        return asyncio.run(self.adownload(year))

    def get(self, version: str = 'monthly-update') -> str:
        """ Returns the path to the Price Paid Data for the given version. """
        return f'downloads/price_paid_data/{version}.csv'

    def get_all(self) -> list:
        """ Returns a list of all Price Paid Data files. """
        return [f'downloads/price_paid_data/{file}' for file in os.listdir('downloads/price_paid_data')]

    def open(self, path) -> list:
        """ Returns a containing the Price Paid Data for the given version. """
        with open(path, 'r') as file:
            return list(csv.reader(file))