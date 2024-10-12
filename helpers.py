"""Прогресс парсмнга."""

import sys


def progress_handler(progress: float) -> None:
    """Отображение процесса парсинга в консоле."""
    bar_length = 20
    status = ""
    progress = float(progress)
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(bar_length * progress))
    text = "\rPercent: [{0}] {1}% {2}".format(  # noqa: UP030
        "#" * block + "-" * (bar_length - block),
        round(progress * 100, 1),
        status,
    )
    sys.stdout.write(text)
    sys.stdout.flush()
