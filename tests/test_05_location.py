from datetime import UTC, datetime
from http import HTTPStatus

import httpx
from ocpi_pydantic.v221.base import OcpiBaseResponse
from ocpi_pydantic.v221.cdrs import OcpiCdr
from ocpi_pydantic.v221.enum import OcpiConnectorTypeEnum, OcpiConnectorFormatEnum, OcpiPowerTypeEnum, OcpiTariffTypeEnum, OcpiTariffDimensionTypeEnum, OcpiStatusEnum, OcpiStatusCodeEnum, OcpiSessionStatusEnum
from ocpi_pydantic.v221.locations.connector import OcpiConnector
from ocpi_pydantic.v221.locations.location import OcpiLocationResponse, OcpiLocation, OcpiGeoLocation
from ocpi_pydantic.v221.locations.evse import OcpiEvse, OcpiEvseResponse
from ocpi_pydantic.v221.sessions import OcpiSession
from ocpi_pydantic.v221.tariffs import OcpiTariff, OcpiTariffElement, OcpiPriceComponent
from ocpi_pydantic.v221.tokens import OcpiToken, OcpiLocationReferences, OcpiAuthorizationInfo, OcpiTokenListResponse
import pytest_asyncio
from respx import MockRouter
from ocpi_client import OcpiClient
import pytest



@pytest_asyncio.fixture
async def ocpi_connector():
    return OcpiConnector(
        id='1',
        standard=OcpiConnectorTypeEnum.IEC_62196_T2_COMBO,
        format=OcpiConnectorFormatEnum.CABLE,
        power_type=OcpiPowerTypeEnum.AC_2_PHASE,
        max_voltage=380,
        max_amperage=100,
        last_updated=datetime.now(UTC).replace(microsecond=0),
    )



@pytest_asyncio.fixture
async def ocpi_evse(ocpi_connector: OcpiConnector):
    return OcpiEvse(
        uid='uia1',
        evse_id='TW*WNC*uid1*1',
        status=OcpiStatusEnum.AVAILABLE,
        connectors=[ocpi_connector],
        last_updated=datetime.now(UTC).replace(microsecond=0),
    )



class TestOcpiClient:
    location: OcpiLocation
    evse: OcpiEvse
    connector: OcpiConnector
    tokens: list[OcpiToken]
    tariff: OcpiTariff
    session: OcpiSession
    cdr: OcpiCdr


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


    @pytest.mark.asyncio
    async def test_put_evse(self, ocpi_client: OcpiClient, ocpi_evse: OcpiEvse, respx_mock: MockRouter):
        ocpi_evse.floor_level = '1F'

        respx_mock.put('https://api.evo.net/ocpi/v221/locations/TW/WNC/L1/uia1').mock(
            return_value=httpx.Response(
                HTTPStatus.OK,
                json=OcpiBaseResponse(status_code=OcpiStatusCodeEnum.SUCCESS).model_dump(mode='json'),
            )
        )
        
        response = await ocpi_client.put_evse(ocpi_location_id='L1', ocpi_evse=ocpi_evse)
        assert response
