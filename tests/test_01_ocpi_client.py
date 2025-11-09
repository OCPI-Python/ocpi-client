from datetime import UTC, datetime
from decimal import Decimal
from http import HTTPStatus
from logging import Logger
import logging
from sys import stderr, stdout

import httpx
import loguru
from ocpi_pydantic.v221.cdrs import OcpiCdr
from ocpi_pydantic.v221.commands import OcpiCommandResult, OcpiCommandResultTypeEnum
from ocpi_pydantic.v221.locations.connector import OcpiConnector
from ocpi_pydantic.v221.locations.location import OcpiHours, OcpiLocation, OcpiGeoLocation
from ocpi_pydantic.v221.locations.evse import OcpiEvse
from ocpi_pydantic.v221.enum import OcpiConnectorTypeEnum, OcpiVersionNumberEnum, OcpiPowerTypeEnum, OcpiTariffTypeEnum, OcpiTariffDimensionTypeEnum, OcpiStatusEnum, OcpiStatusCodeEnum, OcpiSessionStatusEnum
from ocpi_pydantic.v221.sessions import OcpiSession
from ocpi_pydantic.v221.tariffs import OcpiTariff, OcpiTariffElement, OcpiPriceComponent
from ocpi_pydantic.v221.tokens import OcpiToken, OcpiLocationReferences, OcpiAuthorizationInfo, OcpiTokenListResponse
from ocpi_pydantic.v221.versions import OcpiVersion, OcpiVersionsResponse
from pytest_httpx import HTTPXMock
from ocpi_client import OcpiClient
from ocpi_client.models import OcpiParty
import pytest
import pytest_asyncio



_FROM_COUNTRY_CODE = 'TW'
_FROM_PARTY_ID = 'WNC'



@pytest_asyncio.fixture
async def logger_fixture():
    _format = ''.join([
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | ',
        '<level>{level: <8}</level> | ',
        '<magenta>{process.name}</magenta>:<yellow>{thread.name}</yellow> | ',
        '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'
    ])
    logger = loguru.logger
    logger.remove() # Remove pre-configured STDERR hanlder
    logger.add(stdout, level=logging.DEBUG, format=_format)
    logger.add(stderr, level=logging.WARNING, format=_format)
    return logger



@pytest_asyncio.fixture
async def ocpi_client(party_fixture: OcpiParty, logger_fixture: Logger):
    return OcpiClient(
        httpx_async_client=httpx.AsyncClient(),
        from_country_code=_FROM_COUNTRY_CODE,
        from_party_id=_FROM_PARTY_ID,
        to_party=party_fixture,
        logger=logger_fixture,
    )



class TestOcpiClient:
    location: OcpiLocation
    evse: OcpiEvse
    connector: OcpiConnector
    tokens: list[OcpiToken]
    tariff: OcpiTariff
    session: OcpiSession
    cdr: OcpiCdr


    @pytest.mark.asyncio
    async def test_get_versions(self, ocpi_client: OcpiClient, httpx_mock: HTTPXMock):
        response_model = OcpiVersionsResponse(
            data=[OcpiVersion(version=OcpiVersionNumberEnum.v221, url='https://api.evo.net/ocpi/v221')],
            status_code=OcpiStatusCodeEnum.SUCCESS,
        )
        httpx_mock.add_response(json=response_model.model_dump(mode='json'))
        versions = await ocpi_client.get_versions()
        assert versions
        assert not ocpi_client.client.is_closed


    @pytest.mark.asyncio
    async def test_post_command_result(self, ocpi_client: OcpiClient):
        response = await ocpi_client.post_command_result(
            response_url='https://0faa0d3b646847e3bee1e1122193c73d.api.mockbin.io/',
            result=OcpiCommandResult(result=OcpiCommandResultTypeEnum.ACCEPTED),
        )
        assert response
        assert response.status_code == HTTPStatus.OK
        ocpi_client.logger.debug(response)


    # @pytest.mark.asyncio
    # async def test_get_version_details(self, ocpi_client: OcpiClient):
    #     endpoints = await ocpi_client.get_version_details(version=OcpiVersionNumberEnum.v221)
    #     # logger.debug(endpoints)
    #     assert endpoints


    # @pytest.mark.asyncio
    # async def test_put_location(self, ocpi_client: OcpiClient, location: OcpiLocation) -> None:
    #     location.coordinates.latitude = '24.878'
    #     location.coordinates.longitude = '121.211'
    #     location.postal_code = '325'
    #     location.city = '桃園市'
    #     location.address = '龍潭區百年路 1 號'
    #     location.opening_times = OcpiHours(twentyfourseven=True)
    #     location.publish = True
    #     TestOcpiClient.location = location

    #     response = await ocpi_client.put_location(location=await TestOcpiClient.location)
    #     assert response


    # @pytest.mark.asyncio
    # async def test_get_location(self, ocpi_client: OcpiClient):
    #     location = await ocpi_client.get_location(location_id=TestOcpiClient.location.id)
    #     assert location
    #     assert location.id == TestOcpiClient.location.id


    # @pytest.mark.asyncio
    # async def test_put_evse(self, ocpi_client: OcpiClient, evse: OcpiEvse, connector: OcpiConnector):
    #     evse.floor_level = '1F'
    #     TestOcpiClient.evse = evse

    #     connector.standard = OcpiConnectorTypeEnum.IEC_62196_T2_COMBO
    #     connector.power_type = OcpiPowerTypeEnum.AC_2_PHASE
    #     connector.max_voltage = 380
    #     connector.max_amperage = 100
    #     TestOcpiClient.connector = connector
        
    #     response = await ocpi_client.put_evse(ocpi_location_id=TestOcpiClient.location.id, ocpi_evse=await TestOcpiClient.evse)
    #     assert response


    # @pytest.mark.asyncio
    # async def test_get_tokens(self, ocpi_client: OcpiClient):
    #     TestOcpiClient.tokens = await ocpi_client.get_tokens()
    #     assert TestOcpiClient.tokens


    # @pytest.mark.asyncio
    # async def test_put_tariff(self, ocpi_client: OcpiClient):
    #     now = datetime.now(UTC).replace(second=0, microsecond=0)
    #     TestOcpiClient.tariff = OcpiTariff(
    #         country_code=_FROM_COUNTRY_CODE,
    #         party_id=_FROM_PARTY_ID,
    #         id=f'TEST{now.strftime("%Y%m%d%H%M%S")}', # TEST20241012234343
    #         currency='TWD',
    #         type=OcpiTariffTypeEnum.PROFILE_FAST,
    #         elements=[OcpiTariffElement(price_components=[OcpiPriceComponent(
    #             type=OcpiTariffDimensionTypeEnum.ENERGY,
    #             price=Decimal('10'),
    #             vat=5,
    #             step_size=1,
    #         )])],
    #         last_updated=now,
    #     )
    #     response = await ocpi_client.put_tariff(tariff=TestOcpiClient.tariff)


    # @pytest.mark.asyncio
    # async def test_get_tariff(self, ocpi_client: OcpiClient):
    #     response = await ocpi_client.get_tariff(tariff_id=TestOcpiClient.tariff.id)
    #     assert response


    # @pytest.mark.asyncio
    # async def test_delete_tariff(self, ocpi_client: OcpiClient):
    #     response = await ocpi_client.delete_tariff(tariff_id=TestOcpiClient.tariff.id)
