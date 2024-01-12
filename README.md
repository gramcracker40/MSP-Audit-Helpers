### Project Summary: MSP Audit Helpers

#### Overview
The MSP Audit Helpers project is designed to enhance and automate the auditing process for managed service providers (MSPs). This system focuses on analyzing various aspects of service delivery, including profit margins, service quantities, and overall costs associated with individual clients. By automating these audits, MSPs can improve their financial standing, ensure accurate service delivery, and identify any inconsistencies or errors in their accounts.
  Utilizes APIs from Liongard, Huntress, Connectwise and even SentinelOne to gather endpoint installation data surrounding the SaaS products. 

#### Components
1. **additions_audit.py**
   - **Dependencies**: Requires two files in the `Additions-Audit-Data` folder.
   - **Functionality**: Analyzes 'managed service' products, calculating total profit, cost, and margin for each. Outputs two files: 
     - `clean_additions_individuals.csv`: Details each managed service addition with the company and related calculations.
     - `clean_additions_totals.csv`: Summarizes totals for each product, aggregating individual additions.
   - **Purpose**: Provides insights into profits and costs associated with managed service agreements.

2. **products_audit.py**
   - **Dependencies**: Needs `DeviceInventoryReport.csv` from `rmm_audit.py` in `RMM-Audit-Data`.
   - **Functionality**: Integrates four scripts to track and verify the service counts of products (RMM, Cove, Huntress, Sentinel One) against client agreements. Highlights discrepancies in respective CSV files (e.g., `discrepancies_rmm.csv`).
   - **Purpose**: Ensures delivery of services as per client agreements, highlighting any over or under-servicing.

#### Usage Guide

1. **Setup**
   - Ensure all prerequisite files and folders are in place as per the dependencies of each script.
   - Review the information at the top of each script file for specific setup instructions.

2. **Running the Scripts**
   - Execute `additions_audit.py` to generate reports on individual and total managed service products.
   - Run `products_audit.py` after generating `DeviceInventoryReport.csv` via `rmm_audit.py`. This will audit the counts of various serviced products.

3. **Analyzing Outputs**
   - For `additions_audit.py`, examine `clean_additions_individuals.csv` for detailed insights and `clean_additions_totals.csv` for aggregated data.
   - For `products_audit.py`, refer to the generated CSV files (like `discrepancies_rmm.csv`) to identify and address any service count discrepancies.

4. **Action Steps**
   - Use the insights from `additions_audit.py` to optimize financials and product delivery.
   - Resolve discrepancies highlighted by `products_audit.py` to align actual service delivery with client agreements.



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
