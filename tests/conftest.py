from ocpi_pydantic.v221.enum import OcpiAuthMethodEnum, OcpiReservationRestrictionTypeEnum, OcpiConnectorTypeEnum, OcpiTokenTypeEnum, OcpiWhitelistTypeEnum, OcpiConnectorFormatEnum, OcpiPowerTypeEnum, OcpiCdrDimensionTypeEnum, OcpiSessionStatusEnum, OcpiTariffDimensionTypeEnum, OcpiTariffTypeEnum, OcpiDayOfWeekEnum, OcpiStatusCodeEnum, OcpiPartyRoleEnum
from ocpi_client.models import OcpiParty
import pytest_asyncio





@pytest_asyncio.fixture
async def party_fixture():
    return OcpiParty(
        country_code='TW',
        party_id=...,
        party_roles=[OcpiPartyRoleEnum.EMSP, OcpiPartyRoleEnum.CPO],
        versions_url=...,
        credentials_token_for_receiving_request_from_party=...,

        credentials_token_for_sending_register_to_party=...,
        credentials_token_for_sending_request_to_party=...,
        
        v221_endpoints=[],
    )
