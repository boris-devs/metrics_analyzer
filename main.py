import argparse

from reports.clickbait import ClickbaitReportCsv


def main():
	"""
	Main function to handle YouTube metrics processing.

	This function serves as an entry point for the YouTube Metrics Processor script.
	It processes input arguments to determine the list of files for processing and the
	type of report to generate. Based on the specified report type, it instantiates
	the appropriate report generator and invokes its functionality to produce a report.

	:param --files: A required argument representing a list of file paths to process. This
	    accepts one or more file paths as input.
	:param --report: A required argument specifying the type of report to generate (e.g.,
	    "clickbait"). The processor dynamically maps this input to the correct report class
	    for execution.

	"""
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
