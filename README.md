### MSP Audit Helpers

## Purpose
--- Our auditing system is meant to give us insight to the products we are currently providing. 
    This may include profit margins, quantity mishaps across the dashboards/agreements, how much
    an individual addition is costing us, how much total cost is associated with a single client, 
    etc. With this now automated we can use the data gathered to improve our position amongst
    our clients financially, ensure our clients are being provided the agreed upon amounts, and 
    find any loopholes or discrepancies across the accounts. 

# additions_audit.py
--- NOTE: This file needs two files to run properly placed within Additions-Audit-Data, 
    please read the info at the top of the file to see how to set it up. 

    Functionality: this script will sort through all of our additions and calculate the total profit,
    cost, and margin for each individual product marked 'managed service'. It will produce two files
    the first being clean_additions_individuals.csv. This file will show each and every managed service addition 
    along with the company, and calculations mentioned above. The second being clean_additions_totals.csv, this 
    one will show the totals for each product. Adding up each individual additions for the unique products.

    Purpose: to give us insight into the current profit/costs associated with our managed service agreements.

# products_audit.py
--- NOTE: This file only needs one pre-requisite to function properly. In the rmm_audit.py there is
    a file that needs to be generated in RMM-Audit-Data called DeviceInventoryReport.csv. Please navigate to 
    products_audits/rmm_audit.py and read the top two lines describing how to generate this report. 

    Functionality: This program utilizes the innerworkings of 4 seperate scripts to accurately represent the
    counts of each product serviced (RMM, Cove, Huntress, Sentinel One). If a client is paying for 24 rmm 
    workstations in connectwise, it will utilize rmm_audit to go out and check the dashboard and ensure the proper
    amounts are being serviced. When there is a discrepancy between connectwise and one of the dashboards it will
    represent it in a csv file called "discrepancies_product.csv" in the case of RMM it will be 
    discrepancies_rmm.csv. Simply load these csv files into your excel app and start fixing the errors as they
    come up. 

    Purpose: To ensure we are delivering the agreed upon amount. Nothing more, nothing less.