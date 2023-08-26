from tests.mock_data import FIRST_DOCUMENT


async def mock_parser(*args, **kwargs) -> None:
    items: dict = kwargs["items"]
    payload: dict = kwargs["payload"]
    url: str = payload.get("url", "")
    depth: int = payload.get("depth", 0)

    items.update({url: FIRST_DOCUMENT})

    if depth == 0:
        return None
