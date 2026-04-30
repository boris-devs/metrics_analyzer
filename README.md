# Metrics Analyzer

CLI-приложение для анализа CSV-файлов с метриками YouTube-видео.

Проект читает один или несколько CSV-файлов из директории `metrics/`, фильтрует данные по выбранному типу отчёта и выводит результат в виде таблицы в консоль.
## Требования

- Python `3.12+`
- `uv` 

Зависимости проекта:

- `tabulate`
- `pytest`
- `ruff`
- ## Установка

Склонируйте репозиторий и перейдите в директорию проекта:
- `git clone https://github.com/boris-devs/metrics_analyzer.git`
- `cd metrics-analyzer`
- `uv sync`

## Формат входных данных
Передаются файлы через аргументы: `--files stats1.csv stats2.csv`.
Тип репорта: `--report clickbait`.
CSV-файлы должны находиться в директории `metrics/`.

Минимально необходимые колонки:
csv title,ctr,retention_rate