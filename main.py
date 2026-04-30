import argparse
from reports.clickbait import ClickbaitReportCsv

def main():
	parser = argparse.ArgumentParser(description="YouTube Metrics Processor.")
	parser.add_argument("--files", required=True, nargs="+", help="list of files to be processed")
	parser.add_argument("--report", required=True, help="type of report to generate")

	args = parser.parse_args()
	files = args.files
	type_report = args.report
	if type_report == "clickbait":
		clickbait = ClickbaitReportCsv(files)
		print(clickbait.generate_report())


if __name__ == "__main__":
	main()