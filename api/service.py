import re


async def create_query(url: str, title: str, combine: bool = True) -> dict:
    temp = {"url": url, "title": title}
    subquery = {}
    for field, data in temp.items():
        if data is not None:
            subquery[field] = {"$regex": re.compile(data, re.IGNORECASE)}
    if len(subquery) == 1:
        return subquery
    option = "$and" if combine else "$or"
    total_query = {
        option: [
            {"url": subquery["url"]},
            {"title": subquery["title"]},
        ]
    }
    return total_query
