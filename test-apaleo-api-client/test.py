import asyncio
import os

from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider
from apaleoapi.apaleo.identity.v1.identity import InvitationListParams
from dotenv import load_dotenv

load_dotenv(".env.client_credentials")  # Load from specific .env file for this test


async def main() -> None:
    token_provider = OAuth2ClientCredentialsProvider(
        client_id=os.getenv("APALEO_API_CLIENT_ID"),
        client_secret=os.getenv("APALEO_API_CLIENT_SECRET"),
        service="Identity Invitations Example",
    )

    client = ApaleoAPIClient(token_provider=token_provider)

    try:
        invitations = await client.identity.v1.identity.list_invitations(
            InvitationListParams(property_id="BER"),
        )
        print(f"Found {len(invitations.items)} invitation(s)")
        print(f"Found {invitations.count} invitation(s)")
        roles = await client.identity.v1.identity.list_roles()
        print(f"Found {len(roles.items)} role(s)")
        print(f"Found {roles.count} role(s)")
    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
