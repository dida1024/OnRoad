import asyncio

from app.core.telegram.providers.road_provider import OnRoadBot


async def main():
    async with OnRoadBot() as bot:
        await bot.send_message("我已经能在群组中说话了")



if __name__ == "__main__":
    asyncio.run(main())