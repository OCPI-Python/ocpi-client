from ocpi_pydantic.v221.enum import OcpiAuthMethodEnum, OcpiReservationRestrictionTypeEnum, OcpiConnectorTypeEnum, OcpiTokenTypeEnum, OcpiWhitelistTypeEnum, OcpiConnectorFormatEnum, OcpiPowerTypeEnum, OcpiCdrDimensionTypeEnum, OcpiSessionStatusEnum, OcpiTariffDimensionTypeEnum, OcpiTariffTypeEnum, OcpiDayOfWeekEnum, OcpiStatusCodeEnum, OcpiPartyRoleEnum
from ocpi_pydantic.v221.versions import OcpiEndpoint
from ocpi_client.models import OcpiParty
import pytest_asyncio





@pytest_asyncio.fixture
async def party_fixture():
    return OcpiParty(
        country_code='TW',
        party_id='EVO',
        party_roles=[OcpiPartyRoleEnum.EMSP, OcpiPartyRoleEnum.CPO],
        versions_url='https://api.evo.net/ocpi/versions',
        credentials_token_for_receiving_request_from_party='aaa',

        credentials_token_for_sending_register_to_party='bbb',
        credentials_token_for_sending_request_to_party='ccc',
        
        v221_endpoints=[],
    )
