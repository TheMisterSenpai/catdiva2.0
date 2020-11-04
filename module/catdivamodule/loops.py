import time
import discord
import asyncio
from colorama import Style, Fore

class Loop:
    def __init__(self, client):
        self.bot = client

    async def none_loop(self):
        while True:
            try:
                await asyncio.sleep(5)

            except Exception as e:
                print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"В цикле MUTE_LOOP произошла следующая ошибка:")
                print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"\n{e}")
                print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"Цикл MUTE_LOOP продолжает свою работу!")

    def activator(self):
        loop = asyncio.get_event_loop()

        asyncio.ensure_future(self.none_loop())

        loop.run_forever()