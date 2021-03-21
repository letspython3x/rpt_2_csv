import csv
import os
from argparse import ArgumentParser
from pathlib import Path

spaces_2 = "  "
VALID_EXT = ["rpt", "txt"]


class Rpt2Csv:
    """
    RPT 2 CSV files.
    """

    def __init__(self, inputDir, outputDir):
        self.inputDir = inputDir
        self.outputDir = outputDir

    def parse_filedata(self, lines):
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
                data = self.split_row_by_text(data, text='dr')
                data = self.split_row_by_text(data, text='cr')
                rows.append(data)
        return rows

    def split_row_by_text(self, row, text):
        if not isinstance(row, list):
            return row
        text = text.lower()
        myRow = row.copy()
        for pos, item in enumerate(myRow):
            # print(item)
            if text and item.lower().endswith(text) and item.lower() != text:
                row[pos] = item.lower().split(text)[0]
                row.insert(pos + 1, text)
        return row

    def check_out_dir(self):
        """Checks nd create the output directory if doesn't exists"""
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
        print(f"\t CSV file created: {outputFile}")

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
                    if filename.lower()[-3:] in VALID_EXT]
        # print(reqFiles)

        for pos, (filename, filepath) in enumerate(reqFiles):
            print(f"{pos + 1}) Input filename: {filepath}")
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
    parser.add_argument('-ip', '--inputDir', default="./finacleFiles",
                        help="Input folder path for RPT files.")

    parser.add_argument('-op', '--outputDir', dest='outputDir',
                        default="./finacle2csvFiles",
                        help="Optional Output folder path for CSV files.")

    args = parser.parse_args()
    return args


def main():
    args = parse_cmdline()
    rpt2csv = Rpt2Csv(inputDir=args.inputDir, outputDir=args.outputDir)
    rpt2csv.execute()


if __name__ == "__main__":
    main()
