# budget-parser
A tool to help me do my budget faster by parsing bank statements and grouping transactions into categories.

| Bank                | Supported?          |
| --------------------| --------------------|
| Discover            | ✅                  |
| Chase               | ✅                  |
| Venmo               | In Progress         |
## Setup
`python3 -m venv .venv`    
`source .venv/bin/activate`  
`pip3 install -r requirements.txt`

## Usage
Put statement PDFs in the "statements" folder, rename them as appropriate.  
Run `python3 parse.py`