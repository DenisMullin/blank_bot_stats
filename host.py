from webApps.bot.gateway import gateway
import asyncio


if __name__ == "__main__":
    asyncio.run(gateway.host())