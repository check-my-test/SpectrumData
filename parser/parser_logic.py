import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


async def parser(items: dict, payload: dict) -> list | None:
    url = payload["url"]
    depth = payload["depth"]
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"Статус-код {resp.status}")
                    return
                html_doc = await resp.text()
                soup = BeautifulSoup(html_doc, 'html.parser')
                title = soup.title.string
                item = {url: {"url": url, "title": title, "html": html_doc}}
                items.update(item)

                depth -= 1
                if depth < 0:
                    return

                body = soup.find("body")
                links = body.find_all('a', href=True)
                new_urls = []

                for link in links:
                    href = link.get('href')
                    if href is None:
                        return
                    # Проверяем, является ли ссылка абсолютной. Если нет - преобразуем в абсолютную
                    absolute_url = href if urlparse(href).scheme else urljoin(url, href)
                    if absolute_url not in items and absolute_url.startswith("http"):
                        new_urls.append({"url": absolute_url, "depth": depth})

            return new_urls
        except Exception as e:
            print(f"Ошибка при обращении к {url}: {e}")


async def intermediate(queue: asyncio.Queue, items: dict) -> None:
    while not queue.empty():
        payload = await queue.get()
        new_urls_depth = await parser(
            items=items,
            payload=payload,
        )
        if new_urls_depth is not None:
            for new_url_depth in new_urls_depth:
                await queue.put(new_url_depth)
        queue.task_done()


async def run_coros(url: str, depth, count_loaders: int) -> dict:
    items = {}
    queue = asyncio.Queue()
    await queue.put({"url": url, "depth": depth})

    coros = [
        asyncio.create_task(intermediate(queue=queue, items=items)) for _ in range(count_loaders)
    ]

    await asyncio.gather(*coros, return_exceptions=True)

    # После того как очередь израсходована останавливаем задачи
    for task in coros:
        task.cancel()

    # Ждем, остановку задач
    await asyncio.gather(*coros, return_exceptions=True)

    return items
