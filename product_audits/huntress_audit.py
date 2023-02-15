import base64, requests, json, csv
from env_var import get_msp_additions, huntress_private, huntress_public


org_url = "https://api.huntress.io/v1/organizations?limit=500"

def huntress_audit():
    full_key = base64.b64encode(f"{huntress_public}:{huntress_private}".encode())
    huntress_headers = {"Authorization" : f"Basic {full_key.decode()}"}

    org_req = requests.get(org_url, headers=huntress_headers)
    org_obj = json.loads(org_req.text)
    huntress_info = {x['name']: x['agents_count'] for x in org_obj['organizations']}

    huntress_identifiers = ["WFMSP MDR", "WFMSP Gold Svr", "WFMSP Gold Wkst",
                            "WFMSP Plat Svr", "WFMSP PLAT Wkst"]

    # Grabbing the company name and quantities for anything that can be deemed 'MDR' quantity
    msp_additions = get_msp_additions(companies_ver=True)
    huntress_additions = {each: sum([addition['quantity'] for agreement in msp_additions[each]
                            for addition in agreement 
                            if addition['product']['identifier'] in huntress_identifiers]) 
                            for each in msp_additions}
    huntress_additions = {x:huntress_additions[x] for x in huntress_additions 
                        if huntress_additions[x] != 0}

    discrepancies = {}
    huntress_cross_check = json.load(open("cross_checkers/huntress.json", "r"))
    for site in huntress_info:
        try: #cross check first
            print("here at the top")
            cw_quantity = int(huntress_additions[huntress_cross_check[site]])

            print(f"huntress={huntress_info[site]} {type(huntress_info[site])}, cw={cw_quantity} {type(cw_quantity)}")
            if huntress_info[site] != cw_quantity:
                discrepancies[huntress_cross_check[site]] = f"Non-Equal Quantities:{huntress_info[site]}:{cw_quantity}"
        
        except KeyError as err:
            try: # check with name in huntress
                cw_quantity = huntress_additions[site]

                if huntress_info != cw_quantity:
                    discrepancies[site] = f"Non-Equal Quantities:{huntress_info[site]}:{cw_quantity}"

            except KeyError as err: # neither check worked, agreement does not exist. Record Huntress quantities and site name as discrepancy
                discrepancies[site] = f"No active addition:{huntress_info[site]}"


    csv_fields = ["Company Name", "Discrepancy Type", "# Agents in Huntress", "# Paid agents in Connectwise"]
    csv_file = open("Discrepancies/discrepancies_huntress.csv", "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_fields)

    for company in discrepancies:
        split = discrepancies[company].split(":")
        try:
            csv_writer.writerow([company, split[0], split[1], split[2]])
        except IndexError:
            csv_writer.writerow([company, split[0], split[1]])


    print(json.dumps(huntress_additions, indent=2))
    print(json.dumps(huntress_info, indent=2))
    print(json.dumps(discrepancies, indent=2))
