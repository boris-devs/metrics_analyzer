import csv
from abc import ABC, abstractmethod

from tabulate import tabulate

from settings import METRICS_FILES_PATH


class BaseReportCsv(ABC):
	"""
	Base class for generating CSV-based reports.

	This abstract base class provides functionality to process multiple CSV files,
	filter data based on custom criteria, and generate formatted reports.

	The class requires concrete implementations to define specific filtering
	logic for processing row-level data in CSV files.

	:ivar files_path: List of file paths to be processed for the report.
	:type files_path: list
	"""

	def __init__(self, files_path: list):
		self.files_path = files_path

	def exist_file(self, file: str):
		full_path_file = METRICS_FILES_PATH.joinpath(file)
		if not full_path_file.exists():
			raise FileNotFoundError(f"File {file} not found")
		return full_path_file

	def processing_file(self, file: str):
		processed_rows = []
		full_path_file = self.exist_file(file)
		with full_path_file.open("r", encoding="utf-8") as f:
			csv_file = csv.DictReader(f)
			for row in csv_file:
				filtered_data = self.filter_logic(row)
				if filtered_data:
					processed_rows.append(filtered_data)
		return processed_rows

	def generate_report(self):
		all_report_data = []
		for file in self.files_path:
			all_report_data.extend(self.processing_file(file))

		all_report_data.sort(key=lambda x: x['ctr'], reverse=True)
		return self.grid_format_report(all_report_data)

	def grid_format_report(self, data: list[dict]):
		return tabulate(data, headers="keys", tablefmt="grid")

	@abstractmethod
	def filter_logic(self, row: dict):
		pass
