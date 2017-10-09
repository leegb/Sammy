from collections import OrderedDict

ABOUT = 'A software monitoring tool for stock market investors using the <i>Flipping</i> method.'
RAW_RECORD = OrderedDict()
RECORD = []     # Stock list container for the stock monitoring table
COMPANIES = []  # User stock list holder

# main_window.py
SAMMY_TABLE_HEADERS = ['Company',
                       'Symbol',
                       'Market Price',
                       'Buy Below',
                       'Target Price',
                       'Action',
                       'Remarks']

PSE_SYM = ['FGEN', 'MEG', 'COSCO', 'MBT', 'CEB', 'MPI', 'ALI', 'MER']