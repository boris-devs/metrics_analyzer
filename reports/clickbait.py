from reports.base_report import BaseReportCsv


class ClickbaitReportCsv(BaseReportCsv):

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
