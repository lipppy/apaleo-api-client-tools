import asyncio
import os

from dotenv import load_dotenv

from apaleoapi import ApaleoAPIClient, OAuth2ClientCredentialsProvider

# Load from specific .env* file for this test
load_dotenv(".env.client_credentials")


async def main() -> None:
    # Create a token provider with your API credentials
    token_provider = OAuth2ClientCredentialsProvider(
        client_id=os.getenv("APALEO_API_CLIENT_ID"),
        client_secret=os.getenv("APALEO_API_CLIENT_SECRET"),
        service="Concurrent Fetching Example - README.md",
    )

    # Create an instance of the client
    client = ApaleoAPIClient(token_provider=token_provider, max_concurrent=3)

    # List properties concurrently with simple dict params
    # Typed params and alias keys are also supported
    properties = await client.core.v1.inventory.list_properties(
        params={
            "include_archived": False,
            "batch_size": 1,
            "is_concurrently": True,
        }
    )
    # 2026-05-02 11:05:16,010 |    DEBUG | Fetched page 1 with 1 items.
    # 2026-05-02 11:05:16,010 |    DEBUG | Total count to fetch: 6
    # 2026-05-02 11:05:16,010 |    DEBUG | Acquired semaphore for page 1.
    # 2026-05-02 11:05:16,011 |    DEBUG | Acquired semaphore for page 2.
    # 2026-05-02 11:05:16,012 |    DEBUG | Acquired semaphore for page 3.
    # 2026-05-02 11:05:16,108 |    DEBUG | Released semaphore for page 1.
    # 2026-05-02 11:05:16,108 |    DEBUG | Acquired semaphore for page 4.
    # 2026-05-02 11:05:16,227 |    DEBUG | Released semaphore for page 4.
    # 2026-05-02 11:05:16,227 |    DEBUG | Acquired semaphore for page 5.
    # 2026-05-02 11:05:16,301 |    DEBUG | Released semaphore for page 2.
    # 2026-05-02 11:05:16,301 |    DEBUG | Acquired semaphore for page 6.
    # 2026-05-02 11:05:16,305 |    DEBUG | Released semaphore for page 3.
    # 2026-05-02 11:05:16,318 |    DEBUG | Released semaphore for page 5.
    # 2026-05-02 11:05:16,397 |    DEBUG | Released semaphore for page 6.
    print("Found properties:", len(properties.items))
    # > Found properties: 6>

    # Close the client when done to clean up resources
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
