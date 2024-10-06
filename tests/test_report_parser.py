"""Тестирование парсера логов."""

import logging
import os
import unittest
from unittest import mock

from report_manager import NginxReportManager
from tests.constants import TABLE_JSON


@mock.patch("report_manager.progress_handler", new=mock.Mock())
class TestReportParser(unittest.TestCase):
    """Тестирование парсера логов."""

    def setUp(self):
        """Определение переменных  для тестирования."""
        super(TestReportParser, self).setUp()
        logging.disable(logging.CRITICAL)
        self.config = {
            "REPORT_SIZE": 800,
            "REPORT_DIR": "./tests/data/reports",
            "TEMPLATES_DIR": "./tests/data/templates",
            "REPORT_TEMPLATE_FILE": "report.html",
            "LOG_DIR": "./tests/data/logs",
            "MAX_UNPARSED_LINES": 0.1,
        }
        self.test_report_file_name = "report-2018.06.30.html"
        file_names = os.listdir(self.config["REPORT_DIR"])
        for file_name in file_names:
            full_path = f'{self.config["REPORT_DIR"]}/{file_name}'
            os.remove(full_path)

    def tearDown(self):
        """Воссоздание начального состояния после каждого теста."""
        super(TestReportParser, self).tearDown()
        file_names = os.listdir(self.config["REPORT_DIR"])
        for file_name in file_names:
            full_path = f'{self.config["REPORT_DIR"]}/{file_name}'
            os.remove(full_path)

    @mock.patch("report_manager.Template.safe_substitute")
    def test_default_config(self, mock_safe_substitute):
        """Создание отчета из файла из переменной config по умолчанию."""
        mock_safe_substitute.return_value = "tests"
        report_manager = NginxReportManager(self.config)
        report_full_path = f'{self.config["REPORT_DIR"]}/{self.test_report_file_name}'
        self.assertFalse(os.path.exists(report_full_path))
        report_manager.prepare_and_save_report()
        self.assertEqual(
            TABLE_JSON,
            mock_safe_substitute.call_args[1],
        )
        self.assertTrue(os.path.exists(report_full_path))

    @mock.patch("report_manager.Template.safe_substitute")
    def test_change_config(self, mock_safe_substitute):
        """Создание отчета из другого файла с переопределением пути."""
        mock_safe_substitute.return_value = "tests"
        self.config["LOG_DIR"] = "./tests/data/gz_logs"
        report_manager = NginxReportManager(self.config)
        report_full_path = f'{self.config["REPORT_DIR"]}/{self.test_report_file_name}'
        self.assertFalse(os.path.exists(report_full_path))
        report_manager.prepare_and_save_report()
        self.assertEqual(
            TABLE_JSON,
            mock_safe_substitute.call_args[1],
        )
        self.assertTrue(os.path.exists(report_full_path))

    def test_report_already_exists(self):
        """Файл отчета уже существует."""
        report_manager = NginxReportManager(self.config)
        report_full_path = f'{self.config["REPORT_DIR"]}/{self.test_report_file_name}'
        os.mknod(report_full_path)
        self.assertTrue(os.path.exists(report_full_path))
        report_manager.prepare_and_save_report()

    def test_file_not_found_exception(self):
        """Тестирование генерации исключения при отсутствии шаблона в папке шаблонов."""
        self.config["TEMPLATES_DIR"] = "./wrong"
        with self.assertRaises(FileNotFoundError):
            NginxReportManager(self.config)

        self.config["LOG_DIR"] = "./wrong"
        with self.assertRaises(FileNotFoundError):
            NginxReportManager(self.config)

    def test_too_many_unparsed_exception(self):
        """Тестирование генерации исключения при слишком большом числе не распарсеных строк."""
        self.config["MAX_UNPARSED_LINES"] = 0.7
        report_manager = NginxReportManager(self.config)
        with self.assertRaises(Exception) as e:
            report_manager.prepare_and_save_report()
        self.assertEqual(("Too many lines unparsed.",), e.exception.args)
