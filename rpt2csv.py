import csv
import os
from argparse import ArgumentParser
from pathlib import Path

DEFAULT_OUTPUT_DIR = "./rpt2csvFiles"
spaces_2 = "  "


class Rpt2Csv:
    """
    RPT 2 CSV files.
    """
    def __init__(self, inputDir, outputDir=None):
        self.inputDir = inputDir
        self.outputDir = outputDir or DEFAULT_OUTPUT_DIR

    @staticmethod
    def parse_filedata(lines):
        """
        returns a list of lists after splitting lines on the delimiters
        viz: |, spaces_2
        :param lines: list
        :return: list of lists
        """
        rows = []
        for line in lines:
            line_data = []
            if '|' in line:
                line_data = line.split('|')
            elif spaces_2 in line:
                line_data = line.split(spaces_2)
            line_data = [datum.strip() for datum in line_data if datum.strip()]
            data = line_data or line
            if data:
                rows.append(data)
        return rows

    def check_out_dir(self):
        Path(self.outputDir).mkdir(parents=True, exist_ok=True)

    def write_to_csv(self, filename, rows):
        """
        Write the data rows to the output file.
        :param filename: string of name for outputFile.
        :param rows: list of lists
        :return: None
        """
        self.check_out_dir()
        outputFile = f"{self.outputDir}/{os.path.splitext(filename)[0]}.csv"

        with open(outputFile, 'w') as fout:
            writer = csv.writer(fout, delimiter=',')
            writer.writerows(rows)
        print(f">>> CSV file created: {outputFile}")

    def execute(self):
        """
        Execute the operations.
        Traverse over the input folder to fetch all the rpt files.
        and then process each of them one by one.
        :return:
        """

        reqFiles = [(filename, os.path.join(root, filename))
                    for root, _, files in os.walk(self.inputDir)
                    for filename in files
                    if filename.lower().endswith('rpt')]

        for filename, filepath in reqFiles:
            print(f"Working on filename: {filepath}")
            with open(filepath, encoding='utf-8-sig') as fin:
                reader = fin.readlines()
                # Remove Unwanted Lines
                lines = [line for line in reader
                         if line and not line.startswith('----')]
                rows = self.parse_filedata(lines)
                self.write_to_csv(filename, rows)


def parse_cmdline():
    """
    Parse the command lines options passed by user.
    :return: user arguments
    """
    parser = ArgumentParser(description='Convert RPT files to CSV.')
    parser.add_argument('inputDir',
                        help="Input folder path for RPT files.")

    parser.add_argument('-op', '--outputDir', dest='outputDir',
                        help="Optional Output folder path for CSV files.")

    args = parser.parse_args()
    return args


def main():
    args = parse_cmdline()
    rpt2csv = Rpt2Csv(inputDir=args.inputDir, outputDir=args.outputDir)
    rpt2csv.execute()


if __name__ == "__main__":
    main()
