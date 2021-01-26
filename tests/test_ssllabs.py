from unittest.mock import patch

import pytest
from dacite import from_dict

from ssllabs import Ssllabs
from ssllabs.data.info import InfoData
from ssllabs.data.status_codes import StatusCodesData

try:
    from unittest.mock import AsyncMock
except ImportError:
    from asynctest import CoroutineMock as AsyncMock


class TestSsllabs:

    @pytest.mark.asyncio
    async def test_root_certs(self, request):
        with patch("ssllabs.api.root_certs_raw.RootCertsRaw.get",
                   new=AsyncMock(return_value=request.cls.root_certs["rootCerts"])):
            ssllabs = Ssllabs()
            root_certs = await ssllabs.root_certs()
            assert root_certs == request.cls.root_certs["rootCerts"]

    @pytest.mark.asyncio
    async def test_root_certs_value_error(self):
        with pytest.raises(ValueError):
            ssllabs = Ssllabs()
            await ssllabs.root_certs(trust_store=6)

    @pytest.mark.asyncio
    async def test_status_codes(self, request):
        with patch("ssllabs.api.status_codes.StatusCodes.get",
                   new=AsyncMock(return_value=from_dict(data_class=StatusCodesData,
                                                        data=request.cls.status_details))):
            ssllabs = Ssllabs()
            status_codes = await ssllabs.status_codes()
            assert status_codes.statusDetails == request.cls.status_details["statusDetails"]

    @pytest.mark.asyncio
    async def test_availability(self, request):
        with patch("ssllabs.api.info.Info.get",
                   new=AsyncMock(return_Value=from_dict(data_class=InfoData,
                                                        data=request.cls.api_info))):
            ssllabs = Ssllabs()
            assert await ssllabs.availability()

    @pytest.mark.asyncio
    async def test_availability_http_error(self):
        from httpx import Request, Response
        req = Request("GET", "")
        with patch("httpx._client.AsyncClient.get", new=AsyncMock(return_value=Response(401, request=req))):
            ssllabs = Ssllabs()
            assert not await ssllabs.availability()
