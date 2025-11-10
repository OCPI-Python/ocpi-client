from ocpi_pydantic.v221.cdrs import OcpiCdr
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
import pytest



class TestVersions:
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
