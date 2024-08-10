# budget-parser
A tool to help me do my budget faster by parsing bank statements and grouping transactions into categories.

| Bank                | Supported?          |
| --------------------| --------------------|
| Discover            | ✅                  |
| Chase               | ✅                  |
| Venmo               | In Progress         |
| Capital One         | In Progress         |
| Charles Schwab      | In Progress         |

## Setup
`python3 -m venv .venv`    
`source .venv/bin/activate`  
`pip3 install -r requirements.txt`

## Usage
1. In the root directory of this project, create a folder named "statements".
2. Add all bank statements you'd like to parse to this folder.
3. Rename each bank statement to the name of the bank it's from. Supported statement names are `discover.pdf`, `chase.pdf`, `venmo.csv` (venmo statements are only in CSV format), `capitalone.pdf`, or `charlesschwab.pdf`.
4. Run `python3 parse.py`.
