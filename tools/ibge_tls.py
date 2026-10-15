"""TLS context for servicodados.ibge.gov.br.

WORKAROUND(IBGE incomplete chain): the IBGE server sends only its leaf
certificate and omits the Sectigo DV R36 intermediate, so a default context
fails with CERTIFICATE_VERIFY_FAILED. We add that intermediate (vendored in
certs/, fetched from the AIA URL of the leaf) on top of the system roots, so
verification stays on. Remove when
`openssl s_client -connect servicodados.ibge.gov.br:443` verifies without it.
"""
from __future__ import annotations

import ssl
from pathlib import Path

INTERMEDIATE = (
    Path(__file__).resolve().parent
    / "certs"
    / "sectigo-public-server-authentication-ca-dv-r36.pem"
)


def ibge_ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    context.load_verify_locations(cafile=INTERMEDIATE)
    return context
