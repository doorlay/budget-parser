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


https://account.venmo.com/statement?accountType=personal&month=8&profileId=2843209252208640443&year=2024


https://account.venmo.com/api/statement/download?referer=%2Fstatement%3FaccountType%3Dpersonal%26month%3D7%26profileId%3D2843209252208640443%26year%3D2024&startDate=2024-07-01&endDate=2024-07-31&csv=true&profileId=2843209252208640443&accountType=personal