import csv
from settings import METRICS_FILES_PATH


class ClickbaitReportCsv:
	def __init__(self, files_path: list):
		self.files_path = files_path

	def exist_file(self, file: str):
		full_path_file = METRICS_FILES_PATH.joinpath(file)
		if not full_path_file.exists():
			raise FileNotFoundError(f"File {file} not found")
		return full_path_file

	def generate_report(self):
		all_report_data = []
		for file in self.files_path:
			all_report_data.extend(self.processing_file(file))

		all_report_data.sort(key=lambda x: x['ctr'], reverse=True)
		return all_report_data

	def processing_file(self, file: str):
		processed_rows = []
		full_path_file = self.exist_file(file)

		with full_path_file.open("r", encoding="utf-8") as f:
			csv_file = csv.DictReader(f)
			for row in csv_file:
				filtered_data = self.filter_by_ctr_and_retention(row)
				if filtered_data:
					processed_rows.append(filtered_data)
		return processed_rows

	def filter_by_ctr_and_retention(self, row: dict):
		try:
			ctr = float(row.get("ctr", 0))
			retention = float(row.get("retention_rate", 0))

			if ctr > 15 and retention < 40:
				return {
					"title": row.get("title"),
					"ctr": ctr,
					"retention_rate": retention
				}
		except (ValueError, TypeError):
			return None

		return None
