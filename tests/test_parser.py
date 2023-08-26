import unittest
from parser.model import HTMLModel
from parser.router_parser import do_parse
from unittest import TestCase, mock

from mongomock_motor import AsyncMongoMockClient
from starlette.testclient import TestClient

from app import app
from database import db
from tests.mock_data import FIRST_DOCUMENT
from tests.mock_functions import mock_parser


class TestParser(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        app.client = AsyncMongoMockClient()
        app.db = app.client.get_database("test_parser_db")

    async def asyncSetUp(self):
        """Загружаем данные в базу"""
        self.client = TestClient(app)

    async def asyncTearDown(self):
        """Очищаем всю базу"""
        await db.htmls.drop()
        app.client.close()

    async def test_parser_default_params(self, response_model=list[HTMLModel]):
        patch_parser = mock.patch(
            "parser.parser_logic.parser",
            mock_parser,
        )

        patch_parser.start()

        result = await do_parse()

        patch_parser.stop()

        # await self.collection.insert_one({"9": 2, "3": 4})
        # print(await htmls.find().to_list(length=2))
        # print(await htmls.count_documents({}))
        TestCase().assertEqual(result.status_code, 201)
        list_documents = await db.htmls.find().to_list(length=None)
        cleaned_docs = [{"url": item["url"], "title": item["title"], "html": item["html"]} for item in list_documents]
        TestCase().assertEqual(cleaned_docs, [FIRST_DOCUMENT])


if __name__ == "__main__":
    unittest.main()
