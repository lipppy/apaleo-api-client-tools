import asyncio
import os

from dotenv import load_dotenv

from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider
from apaleoapi.apaleo.core.v1.inventory import PropertyListParams

# Load from specific .env* file for this test
load_dotenv(".env.client_credentials")


async def main() -> None:
    # Create a token provider with your API credentials
    token_provider = OAuth2ClientCredentialsProvider(
        client_id=os.getenv("APALEO_API_CLIENT_ID"),
        client_secret=os.getenv("APALEO_API_CLIENT_SECRET"),
        service="Flexible Request Inputs Example - README.md",
    )

    # Create an instance of the client
    client = ApaleoAPIClient(token_provider=token_provider)

    # Typed params
    params_typed = PropertyListParams(
        country_code=["DE", "AT"], include_archived=False
    )
    properties_1 = await client.core.v1.inventory.list_properties(
        params=params_typed
    )
    print("Found properties (typed params):", len(properties_1.items))
    # > Found properties (typed params): N>

    # Equivalent dict params with snake_case keys
    params_dict = {"country_code": ["DE", "AT"], "include_archived": False}
    properties_2 = await client.core.v1.inventory.list_properties(
        params=params_dict
    )
    print("Found properties (dict params):", len(properties_2.items))
    # > Found properties (dict params): N>

    # Equivalent dict params with alias keys (Apaleo API uses camelCase)
    params_alias = {"countryCode": ["DE", "AT"], "includeArchived": False}
    properties_3 = await client.core.v1.inventory.list_properties(
        params=params_alias
    )
    print("Found properties (alias params):", len(properties_3.items))
    # > Found properties (alias params): N>

    # You can also mix snake_case and camelCase keys if you like,
    # the client will handle the conversion
    params_mixed = {"country_code": ["DE", "AT"], "includeArchived": False}
    properties_4 = await client.core.v1.inventory.list_properties(
        params=params_mixed
    )
    print("Found properties (mixed params):", len(properties_4.items))
    # > Found properties (mixed params): N>

    # All four calls should yield the same result
    assert properties_1 == properties_2 == properties_3 == properties_4

    # Close the client when done to clean up resources
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
