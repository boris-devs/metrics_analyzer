import argparse
from reports.clickbait import ClickbaitReportCsv


def main():
	parser = argparse.ArgumentParser(description="YouTube Metrics Processor.")
	parser.add_argument("--files", required=True, nargs="+", help="list of files to be processed")
	parser.add_argument("--report", required=True, help="type of report to generate")

	args = parser.parse_args()

	files = args.files
	type_report = args.report

	reports_map = {"clickbait": ClickbaitReportCsv}
	report_class = reports_map.get(type_report, None)
	if report_class is None:
		print("Invalid report type")

	try:
		report_instance = report_class(files)
		print(report_instance.generate_report())
	except FileNotFoundError as e:
		print(f"File Error: {e}")
	except Exception as e:
		print(f"Something went wrong during parsing: {e}")


if __name__ == "__main__":
	main()
