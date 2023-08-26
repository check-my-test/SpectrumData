import unittest
from parser.router_parser import do_parse
from unittest import TestCase, mock

from mongomock_motor import AsyncMongoMockClient
from starlette.testclient import TestClient

from app import app
from tests.mock_data import FIRST_DOCUMENT
from tests.mock_functions import mock_parser


class TestParser(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = AsyncMongoMockClient()
        self.db = self.client.get_database("test_parser_db")
        self.app = TestClient(app)

    async def asyncTearDown(self):
        await self.db.htmls.drop()
        self.client.close()

    async def test_parser_default_params(self):
        patch_parser = mock.patch(
            "parser.parser_logic.parser",
            mock_parser,
        )

        patch_parser.start()

        result = await do_parse()

        patch_parser.stop()

        # await self.db.htmls.insert_one({"9": 2, "3": 4})
        # print(await self.db.htmls.find().to_list(length=2))
        # print(await self.db.get_collection("htmls").find().to_list(length=2))
        # print(await htmls.count_documents({}))
        TestCase().assertEqual(result.status_code, 201)
        list_documents = await self.db.htmls.find().to_list(length=None)
        cleaned_docs = [{"url": item["url"], "title": item["title"], "html": item["html"]} for item in list_documents]
        TestCase().assertEqual(cleaned_docs, [FIRST_DOCUMENT])


if __name__ == "__main__":
    unittest.main()
