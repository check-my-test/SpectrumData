import unittest
from parser.router_parser import do_parse
from unittest import TestCase, mock

from mongomock_motor import AsyncMongoMockClient
from starlette.testclient import TestClient

from app import app
from config.config import settings
from database import db
from tests.mock_data import FIRST_DOCUMENT
from tests.mock_functions import mock_parser


class TestParser(unittest.IsolatedAsyncioTestCase):
    client = AsyncMongoMockClient()
    db = client.get_database(settings.DB_NAME)
    app = TestClient(app)

    async def asyncSetUp(self):
        pass

    async def asyncTearDown(self):
        await db.htmls.drop()

    async def test_parser_default_params(self):
        """
        Проверка работы парсера с мок-данными о сайте, сохранением в тестовую базу
        :return:
        """
        patch_parser = mock.patch(
            "parser.parser_logic.parser",
            mock_parser,
        )

        patch_parser.start()

        result = await do_parse()

        patch_parser.stop()

        TestCase().assertEqual(result.status_code, 201)
        list_documents = await db.htmls.find().to_list(length=None)
        cleaned_docs = [{"url": item["url"], "title": item["title"], "html": item["html"]} for item in list_documents]
        TestCase().assertEqual(cleaned_docs, [FIRST_DOCUMENT])


if __name__ == "__main__":
    unittest.main()
