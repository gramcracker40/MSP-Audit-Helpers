from env_var import get_msp_additions, liongard_controller
import json, csv, logging
# Cove Data Product ID's in ConnectWise --> "WFMSP Cove Backup-Workstation", "WFMSP Gold Svr", "WFMSP Gold Wkst"
#                                       --> "WFMSP Plat Svr", "WFMSP PLAT Wkst", "WFMSP Slvr Svr", "WFMSP Slvr Wkst"
#                                       --> "WFMSP Cove Backup-Virtual Server", "WFMSP Cove B/U-Physical Server"
#                                       --> "WFMSP Cove Backup-Docs"
# Output: Key value pairs -> key: company, value: list of discrepancies with company's Cove agreements
#   
#
# Purpose: To pull all N-Able backup inspectors from Liongard and obtain the total backed up devices for each account
#          The script will then pull all MSP Additions within individual agreements related to Cove backups and obtain 
#          the agreed upon quantities It will then determine if there are any discrepancies, such as missed quantities
#          and no addition matching the in dashboard devices. 

# setting up logger
logging.basicConfig(level=logging.DEBUG, filename="MSP_Audit.log", format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

cove_inspector_id = 76
cove_number_devices_metric_id = 2417

def cove_audit(all_systems, msp_additions):

    cove_systems = [(x['Environment']['Name'], x['ID'], x['Launchpoint']['Alias']) 
                    for x in all_systems if x['Inspector']['ID'] == cove_inspector_id]


    cove_identifiers = ["WFMSP Cove Backup-Workstation", "WFMSP Gold Svr", "WFMSP Gold Wkst", 
                        "WFMSP Plat Svr", "WFMSP PLAT Wkst", "WFMSP Slvr Svr", "WFMSP Slvr Wkst",
                        "WFMSP Cove Backup-Virtual Server", "WFMSP Cove B/U-Physical Server", 
                        "WFMSP Cove Backup-Docs"]
    cove_additions = {}
    for company in msp_additions:
        for add_count, additions in enumerate(company[1]):
            if additions['product']['identifier'] in cove_identifiers:
                if company[0] not in cove_additions:
                    cove_additions[company[0]] = {"quantity": additions['quantity']}
                else:
                    cove_additions[company[0]]["quantity"] += additions['quantity']


    systems_to_query = []
    company_values = {}
    for count, system in enumerate(cove_systems):
        systems_to_query.append(system[1])
        
        if system[1] not in company_values:
            if system[0] != "Single Client Environment  --- Check Inspector Name":
                company_values[system[1]] = {"company": system[0], "data": ""}
            else:
                company_values[system[1]] = {"company": system[2].split(" - ")[1], "data": ""}
        
        if (count + 1) % 10 == 0 or count == len(cove_systems) - 1:
            try:
                data = liongard_controller.get_metric_data(systemID=systems_to_query, metricID=cove_number_devices_metric_id)
                            
                for key in data:
                    for metric_key in data[key]:
                        if (type(data[key][metric_key]['Metric']['err']) == None.__class__
                            and data[key][metric_key]["Metric"]["value"] != 0
                        ):
                            company_values[int(key)]["data"] = data[key][metric_key]["Metric"]["value"]
                        elif data[key][metric_key]["Metric"]["value"] == 0:
                            company_values.pop(int(key))

                systems_to_query.clear()
            except KeyError as err:
                logger.error(exc_info=True, msg=f"error = {err} line 68: cove_audit.py")


    discrepancies = {}
    single_client_checker = json.load(open("cross_checkers/single_client_cross_check.json", "r"))
    for values in company_values:
        discrepancies[company_values[values]['company']] = []
        try:
            cove_quantity = int(company_values[values]['data'])
            cw_quantity = int(cove_additions[company_values[values]['company']]['quantity'])

            if cw_quantity != cove_quantity:
                err = f"Cove Backups:Incorrect quantities:{cove_quantity}:{cw_quantity}"
                discrepancies[company_values[values]['company']].append(err)

        #simply means company_values[values]['data'] was never changed on line 
        except ValueError:
            pass
        
        except KeyError as err:
            if company_values[values]['company'] in str(err) and str(err).strip("'") not in single_client_checker:
                discrepancies[company_values[values]['company']].append(f"Cove Backups:No Addition:{cove_quantity}")

            # runs check for Liongard environment "Single Client Environment --- Check Friendly name" very very very special case
            elif str(err).strip("'") in single_client_checker:
                try:
                    #using the cw name associated with this specific single client environment to access the true quantity
                    cw_check = int(cove_additions[single_client_checker[str(err).strip("'")]]['quantity'])
                    cove_check = int(company_values[values]['data'])

                    if cw_check != cove_check:
                        err = f"Cove Backups: Incorrect quantities:{cw_check}:{cove_check}"
                        discrepancies[company_values[values]['company']].append(err)

                except KeyError as err:
                    logger.error(exc_info=True, msg=f"error = company does not exist in single_client_cross_check.json: line 103: cove_audit.py")
                    
            else:
                logger.error(exc_info=True, msg=f"error = {err} line 106: cove_audit.py")

    discrepancies = {x:discrepancies[x] for x in discrepancies if discrepancies[x]}
    #print(json.dumps(discrepancies, indent=2))


    csv_fields = ["Company Name", "Product", "Discrepancy Type", "# Devices in Cove", "# Paid devices in Connectwise"]
    csv_file = open("Discrepancies/discrepancies_cove.csv", "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_fields)

    for company in discrepancies:
        split = discrepancies[company][0].split(":")
        try:
            csv_writer.writerow([company, split[0], split[1], split[2], split[3]])
        except IndexError:
            csv_writer.writerow([company, split[0], split[1], split[2]])