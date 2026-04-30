import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from reports.clickbait import ClickbaitReportCsv


@pytest.mark.parametrize("row, expected", [
	({"title": "Video 1", "ctr": "18.5", "retention_rate": "30"},
	 {"title": "Video 1", "ctr": 18.5, "retention_rate": 30.0}),

	({"title": "Video 2", "ctr": "15.0", "retention_rate": "20"}, None),

	({"title": "Video 3", "ctr": "20.0", "retention_rate": "40"}, None),

	({"title": "Video 4", "ctr": "ошибка", "retention_rate": "20"}, None),

	({"title": "Video 5"}, None),
])
def test_filter_logic(row, expected):
	report = ClickbaitReportCsv([])
	assert report.filter_logic(row) == expected


def test_sorting_logic():
	report = ClickbaitReportCsv(["fake.csv"])

	mock_data = [
		{"title": "Low", "ctr": 16.0, "retention_rate": 10.0},
		{"title": "High", "ctr": 25.0, "retention_rate": 10.0},
		{"title": "Mid", "ctr": 20.0, "retention_rate": 10.0},
	]

	with patch.object(ClickbaitReportCsv, 'processing_file', return_value=mock_data):
		report.files_path = ["fake.csv"]

		results = []
		for f in report.files_path:
			results.extend(report.processing_file(f))
		results.sort(key=lambda x: x['ctr'], reverse=True)

		assert results[0]['title'] == "High"
		assert results[-1]['title'] == "Low"


def test_exist_file_raises_error():
	report = ClickbaitReportCsv(["non_existent.csv"])
	with pytest.raises(FileNotFoundError):
		report.exist_file("non_existent.csv")


@patch("pathlib.Path.exists")
def test_exist_file_success(mock_exists):
	mock_exists.return_value = True
	report = ClickbaitReportCsv(["exists.csv"])
	path = report.exist_file("exists.csv")
	assert isinstance(path, Path)


def test_processing_file_merging():
	csv_content = "title,ctr,retention_rate\nVideo 1,20.0,30.0\n"

	report = ClickbaitReportCsv(["file1.csv", "file2.csv"])

	with patch("pathlib.Path.exists", return_value=True), \
			patch("pathlib.Path.open", mock_open(read_data=csv_content)):
		all_data = []
		for f in report.files_path:
			all_data.extend(report.processing_file(f))

		assert len(all_data) == 2
		assert all_data[0]["title"] == "Video 1"


def test_generate_report_full_cycle():
	mock_processed = [
		{"title": "Best", "ctr": 30.0, "retention_rate": 20.0},
		{"title": "Worst", "ctr": 16.0, "retention_rate": 10.0}
	]

	report = ClickbaitReportCsv(["test.csv"])

	with patch.object(ClickbaitReportCsv, 'processing_file', return_value=mock_processed):
		table_output = report.generate_report()

		assert isinstance(table_output, str)
		assert "Best" in table_output
		assert "30" in table_output
		assert "Worst" in table_output
		assert "16" in table_output


def test_filter_with_missing_columns():
	report = ClickbaitReportCsv([])

	bad_row = {"views": "1000", "likes": "50"}

	assert report.filter_logic(bad_row) is None
