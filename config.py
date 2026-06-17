import os
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

COLOR_GREEN = 0x2ECC71
COLOR_RED = 0xE74C3C
COLOR_GOLD = 0xF1C40F
COLOR_PURPLE = 0x9B59B6
COLOR_BLUE = 0x3498DB