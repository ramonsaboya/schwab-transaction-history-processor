# Schwab Transaction History Processor

## Description

This project is designed to process your Schwab statements. It extracts all sell and vest events and formats the data for calculating Capital Gains Tax (CGT) using the calculator available at http://www.cgtcalculator.com/calculator.aspx.

## Installation

Follow these steps to install the project:

1. Clone the repository: `git clone https://github.com/yourusername/schwab-transaction-history-processor.git`
2. Navigate to the project directory: `cd schwab-transaction-history-processor`
3. Install the necessary dependencies: `pip install PyPDF2`

## Usage

To run the project, you need to provide the directory of the statements PDF as an argument:

1. Run the script: `python schwab.py /path/to/your/pdf/directory`
2. The script will output a `transactions.csv` file. This file contains the string that you can paste into the CGT calculator.

## Requirements

This project requires Python 3.8 or above and PyPDF2.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.