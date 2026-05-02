import asyncio
import os

from dotenv import load_dotenv

from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider
from apaleoapi.apaleo.common import Operation, OperationOp

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
    property_id = "BER"
    property_berlin_before = await client.core.v1.inventory.get_property(
        property_id=property_id
    )
    property_description_before = (
        property_berlin_before.description.get("en", "")
        if property_berlin_before.description
        else ""
    )
    print(
        "Property description (before update):",
        property_description_before or "<no description>",
    )
    # > Property description (before update): <no description>

    property_description_after = "Added description for Berlin property"
    # Using JSON Patch operations for the update,
    # which allows for flexible request inputs
    # Do not forget to use list of operations as payload for the update method,
    # even if you have just one operation to perform
    operations_params = [
        Operation(
            op=OperationOp.ADD,
            path="/description/en",
            value=property_description_after,
        )
    ]
    _ = await client.core.v1.inventory.update_property(
        property_id=property_id, payload=operations_params
    )
    property_berlin_after = await client.core.v1.inventory.get_property(
        property_id=property_id
    )
    property_description_after = (
        property_berlin_after.description.get("en", "")
        if property_berlin_after.description
        else ""
    )
    print(
        "Property description (after update):",
        property_description_after or "<no description>",
    )
    # > Property description (after update): Added description for Berlin ...>

    # Revert the change to keep the test idempotent, use dict payload for that
    revert_operations_params = [{"op": "remove", "path": "/description/en"}]
    _ = await client.core.v1.inventory.update_property(
        property_id=property_id, payload=revert_operations_params
    )
    property_berlin_after_revert = await client.core.v1.inventory.get_property(
        property_id=property_id
    )
    property_description_after_revert = (
        property_berlin_after_revert.description.get("en", "")
        if property_berlin_after_revert.description
        else ""
    )
    print(
        "Property description (after revert):",
        property_description_after_revert or "<no description>",
    )
    # > Property description (after revert): <no description>

    # Close the client when done to clean up resources
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
