from env_var import liongard_controller, get_msp_additions
import json, csv, logging #traceback --- debug in a try/except scenario

# setting up logger
logging.basicConfig(level=logging.DEBUG, filename="MSP_Audit.log", format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

s1_inspector_id = 70
s1_num_agents_metric_id = 2416

def s1_audit(systems, msp_additions):

    s1_systems_IDs = [(x['Environment']['Name'], x['ID'], x['Launchpoint']['Alias']) 
                    for x in systems if x['Inspector']['ID'] == s1_inspector_id]


    s1_identifiers = ["WFMSP EDR-Sentinel One", "WFMSP Slvr Wkst", "WFMSP Slvr Svr", 
                    "WFMSP PLAT Wkst", "WFMSP Plat Svr", "WFMSP Gold Wkst", "WFMSP Gold Svr"]
    # s1_additions = {company[0] : company[1][add_count] for company in cw_additions
    #                 for add_count, additions in enumerate(company[1])                 does not work when adding quantity, need server and workstation
    #                 if additions['product']['identifier'] in s1_identifiers}          count for aggregate total of sentinel one agents in case of packages
    s1_additions = {}                                                                       # Pretty cool tho
    for company in msp_additions:
        for add_count, additions in enumerate(company[1]):
            if additions['product']['identifier'] in s1_identifiers:
                if company[0] not in s1_additions:
                    s1_additions[company[0]] = {"quantity": additions['quantity']}
                else:
                    s1_additions[company[0]]["quantity"] += additions['quantity']


    systems_to_query = []
    company_values = {}
    for count, system in enumerate(s1_systems_IDs):
        systems_to_query.append(system[1])
        
        if system[1] not in company_values:
            if system[0] != "Single Client Environment  --- Check Inspector Name":
                company_values[system[1]] = {"company": system[0], "data": ""}
            else:
                company_values[system[1]] = {"company": system[2].split(" - ")[1], "data": ""}
        
        if (count + 1) % 10 == 0 or count == len(s1_systems_IDs) - 1:
            try:
                data = liongard_controller.get_metric_data(systemID=systems_to_query, metricID=s1_num_agents_metric_id)
                            
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
                logger.error(exc_info=True, msg=f"error = {err} line 57: s1_audit.py")


    discrepancies = {}
    single_client_checker = json.load(open("cross_checkers/single_client_cross_check.json", "r"))
    for values in company_values:
        discrepancies[company_values[values]['company']] = []
        try:
            s1_quantity = int(company_values[values]['data'])
            cw_quantity = int(s1_additions[company_values[values]['company']]['quantity'])

            if cw_quantity != s1_quantity:
                err = f"Sentinel One:Incorrect quantities:{s1_quantity}:{cw_quantity}"
                discrepancies[company_values[values]['company']].append(err)

        #simply means company_values[values]['data'] was never changed on line 
        except ValueError:
            pass
        
        except KeyError as err:
            if company_values[values]['company'] in str(err) and str(err).strip("'") not in single_client_checker:
                discrepancies[company_values[values]['company']].append(f"Sentinel One:No Addition:{s1_quantity}")

            # runs check for Liongard environment "Single Client Environment --- Check Friendly name" very very very special case
            elif str(err).strip("'") in single_client_checker:
                try:
                    #using the cw name associated with this specific single client environment to access the true quantity
                    cw_check = int(s1_additions[single_client_checker[str(err).strip("'")]]['quantity'])
                    s1_check = int(company_values[values]['data'])

                    if cw_check != s1_check:
                        err = f"Sentinel One: Incorrect quantities:{cw_check}:{s1_check}"
                        discrepancies[company_values[values]['company']].append(err)

                except KeyError as err:
                    logger.error(exc_info=True, msg=f"error = company does not exist in single_client_cross_check.json: line 92: s1_audit.py")
                    
            else:
                logger.error(exc_info=True, msg=f"error = {err} line 95: s1_audit.py")

    discrepancies = {x:discrepancies[x] for x in discrepancies if discrepancies[x]}

    #print(json.dumps(discrepancies, indent=2))

    #displaying discrepancies found in a CSV file that can be uploaded into an excel workbook. 
    csv_fields = ["Company Name", "Product", "Discrepancy Type", "# Agents in Sentinel One", "# Paid agents in Connectwise"]
    csv_file = open("Discrepancies/discrepancies_s1.csv", "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_fields)

    for company in discrepancies:
        split = discrepancies[company][0].split(":")
        try:
            csv_writer.writerow([company, split[0], split[1], split[2], split[3]])
        except IndexError:
            csv_writer.writerow([company, split[0], split[1], split[2]])


