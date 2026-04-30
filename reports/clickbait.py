from reports.base_report import BaseReportCsv


class ClickbaitReportCsv(BaseReportCsv):
	"""
	Provides logic for filtering clickbait report data based on specified thresholds.

	This class inherits from BaseReportCsv and provides a specific filtering mechanism for
	rows of data that meet certain criteria related to click-through rate (CTR) and
	retention rate. If the conditions are met, it extracts and returns relevant fields
	from the data row. Otherwise, it discards the row.
	"""
	def filter_logic(self, row: dict):
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
