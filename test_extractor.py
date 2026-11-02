import asyncio

from memory_extractor import extract_memory


async def main():

    message = """
    I earn ₹70,000 per month.
    I want to save ₹20,000 every month.
    My risk appetite is low.
    I spend ₹8,000 on food.
    """

    result = await extract_memory(message)

    print("Extracted Memory:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())