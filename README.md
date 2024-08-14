# budget-parser
A tool to help me do my budget faster by parsing bank statements and grouping transactions into categories.

| Bank                | Supported?          | Required File Name   |
| --------------------| --------------------| ---------------------|
| Discover            | ✅                  | `discover.pdf`       |
| Chase               | ✅                  | `chase.pdf`          |
| Venmo               | ✅                  | `venmo.csv`          |
| Capital One         | ✅                  | `capitalone.pdf`     |
| Bank of America     | ✅                  | `bofa.pdf`           |
| Charles Schwab      | ✅                  | `schwab.csv`         |

## Setup
`python3 -m venv .venv`    
`source .venv/bin/activate`  
`pip3 install -r requirements.txt`

## Usage
1. In the root directory of this project, create a folder named "statements". Add all bank statements you'd like to parse to this folder.
2. Rename each bank statement to the file name specified in the table above. 
3. Run `python3 parse.py` and follow the instructions in the terminal. Note: it helps to create an "Ignore" category to put budget items that you don't want to count, such as paying off credit cards and such.
