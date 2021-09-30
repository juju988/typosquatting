import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import Optional


async def get_project_summary(package: str) -> Optional[str]:
    url = f'https://pypi.org/project/{package}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
    soup = BeautifulSoup(response, "html.parser")
    if soup.find("p", class_='package-description__summary'):
        return soup.find("p", class_='package-description__summary').getText()
    else:
        return None

