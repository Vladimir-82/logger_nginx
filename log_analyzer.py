"""Основной файл."""

import argparse
import copy
import json
import logging
from json import JSONDecodeError

from report_manager import NginxReportManager

config = {
    'REPORT_SIZE': 1000,
    'REPORT_DIR': './reports',
    'TEMPLATES_DIR': './templates',
    'REPORT_TEMPLATE_FILE': 'report.html',
    'LOG_DIR': './log',
    'MAX_UNPARSED_LINES': 0.1,
}


def start_logging(parsed_config) -> None:
    """Запись логов."""
    logging.basicConfig(
        filename=parsed_config.get('LOG_PATH', None),
        format='[%(asctime)s] %(levelname).1s %(message)s', datefmt='%Y.%m.%d %H:%M:%S',
        level=logging.INFO,
    )


def get_config(file_name=None) -> dict:
    """Получение конфига."""
    result_config = copy.deepcopy(config)
    if file_name:
        try:
            with open(file_name, 'r') as config_file:
                parsed_config = json.load(config_file)
        except FileNotFoundError:
            logging.exception(f'Файл {file_name} не найден')
        except JSONDecodeError:
            logging.exception(f'Файл {file_name} не может быть декодирован')
            raise
        result_config.update(parsed_config)
    return result_config


def get_parsed_args() -> argparse.Namespace:
    """Получение аргументов для парсинга."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config', default='config.json', help='Path to the config file.')
    return arg_parser.parse_args()


def main() -> None:
    """Основной стек программы."""
    args = get_parsed_args()
    custom_config = get_config(args.config)

    start_logging(custom_config)

    logging.info('Initializing report manager.')
    report_manager = NginxReportManager(config)
    report_manager.prepare_and_save_report()


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, Exception):
        logging.exception('Unexpected error.')
