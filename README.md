# budget-parser
A tool to help me do my budget faster by parsing bank statements and grouping transactions into categories.

| Bank                | Supported?          | Required File Name   |
| --------------------| --------------------| ---------------------|
| Discover            | ✅                  | `discover.pdf`       |
| Chase               | ✅                  | `chase.pdf`          |
| Venmo               | ✅                  | `venmo.csv`          |
| Capital One         | ✅                  | `capitalone.pdf`     |
| Bank of America     | ✅                  | `bofa.pdf`           |
| Charles Schwab      | In Progress         | N/A                  |

## Setup
`python3 -m venv .venv`    
`source .venv/bin/activate`  
`pip3 install -r requirements.txt`

## Usage
1. In the root directory of this project, create a folder named "statements". Add all bank statements you'd like to parse to this folder.
3. Rename each bank statement to the file name specified in the table above. 
4. Run `python3 parse.py`.
