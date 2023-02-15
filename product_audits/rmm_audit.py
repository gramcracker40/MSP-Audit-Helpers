# for the DeviceInventoryReport.csv you must go to n-able rmm and in the north pane, select Reports-->Device Inventory Report-->CSV Export
# place the file as DeviceInventoryReport.csv in the RMM-Audit-Data for the devices used in this script to be up to date.
import csv

def parse_csv(file):
    '''
    parses a csv file into a list of objects, the objects being individual rows.
    The headers will be used as keys for each value in each row
    '''
    reader = csv.reader(open(file, "r"))
    headers = [x for x in next(reader)]

    objects = []
    for each_row in reader:
        row = [x for x in each_row]
        obj = {headers[count]:y for count, y in enumerate(row)}
        objects.append(obj)

    return objects

def rmm_audit(msp_additions):
    ###################################################
    ###  Retrieiving Data
    ###################################################
    # pulling list of rmm devices 
    rmm_devices = parse_csv("RMM-Audit-Data/DeviceInventoryReport.csv")
    additions = msp_additions

    ###################################################
    ### Parsing data
    ###################################################
    company_inventory = {}
    for addition in additions:
        for each in addition[1]:
            try:
                if addition[0] not in company_inventory:
                    company_inventory[addition[0]] = {
                        'cw_info' : {  
                            each['product']['identifier']: each['quantity']
                        }
                    }
                    #print(addition[0])
                else:
                    company_inventory[addition[0]]['cw_info'][each['product']['identifier']] = each['quantity']
            except KeyError as err:
                print(err)

    for device in rmm_devices:
        client = device['Client'].replace(";", ",")
        
        
        try:
            company_inventory[client][device['Type']] += 1
        except KeyError as err:
            if client not in company_inventory:
                company_inventory[client] = {device['Type'] : 1}
            else:
                company_inventory[client][device['Type']] = 1

    # below dumps compiled data for each company as a check of validity
    # company_inv_file = open("quantities_check.json", "w")
    # company_check = json.dump(company_inventory, company_inv_file, indent=2)

    ###################################################
    ### Performing RMM check - Discrepancies
    ###################################################
    # productID's --> WFMSP RMM Workstation  --> WFMSP RMM Server 

    rmm_ws_products = ['WFMSP RMM Workstation', 'WFMSP Slvr Wkst', 'WFMSP Gold Wkst', 'WFMSP PLAT Wkst']
    rmm_server_products = ['WFMSP RMM Server', 'WFMSP Slvr Svr' , 'WFMSP Gold Svr', 'WFMSP Plat Svr']
    discrepancies = {}

    for company in company_inventory:
        #print(company)
        discrepancies[company] = []
        try:
            server_quantity = [x for x in company_inventory[company]['cw_info'] if x in rmm_server_products]
            server_quantity = float(company_inventory[company]['cw_info'][server_quantity[0]])
            #print(f"Servers : {server_quantity}")
            if server_quantity != company_inventory[company]['server']:
                discrepancies[company].append(f"RMM: Incorrect quantities: Servers: CW addition={server_quantity} " +
                    f"| RMM Dashboard={company_inventory[company]['server']}")
                
        except (TypeError, IndexError):
            try:
                if company_inventory[company]['server']:
                    discrepancies[company].append(f"RMM: No Addition: Server: RMM Dashboard has {company_inventory[company]['server']} servers")
            except KeyError:
                #means there is no agreement for rmm and there is no servers in rmm
                pass
        
        except KeyError as err:
            try:
                if "cw_info" in str(err) and company_inventory[company]['server']:
                    discrepancies[company].append(f"RMM: No Addition: Servers: RMM Dashboard has {company_inventory[company]['server']} servers")
            except KeyError as err:
                pass

    for org in company_inventory:
        #print(org)
        try:
            ws_quantity = [x for x in company_inventory[org]['cw_info'] if x in rmm_ws_products]
            #print(ws_quantity)
            ws_quantity = float(company_inventory[org]['cw_info'][ws_quantity[0]])
            #print(f"Workstations : {ws_quantity}")
            if ws_quantity != company_inventory[org]['workstation']:
                discrepancies[org].append(f"RMM: Incorrect quantities: Workstations: CW addition={ws_quantity} " +
                    f"| RMM Dashboard={company_inventory[org]['workstation']}")
        
        except (TypeError, IndexError):
            try:
                if company_inventory[org]['workstation']:
                    discrepancies[org].append(f"RMM: No Addition: Workstations: RMM Dashboard has {company_inventory[org]['workstation']} workstations")
            except KeyError:
                #means there is no agreement for rmm and there is no workstations in rmm
                pass


        except KeyError as err:
            # throws KeyError if there is no agreements 
            try:
                if "cw_info" in str(err) and company_inventory[org]['workstation']:
                    discrepancies[org].append(f"RMM: No Addition: Workstations: RMM Dashboard has {company_inventory[org]['workstation']} workstations")
            # only throws if there are no workstations in RMM, which is fine. pass
            except KeyError as err:
                pass
    
    #print(json.dumps(discrepancies, indent=2))

    discrepancies = {x:discrepancies[x] for x in discrepancies if discrepancies[x]}

    csv_file = open("Discrepancies/discrepancies_rmm.csv", "w", newline="")
    csv_fields = ['Company', 'Product', 'Discrepancy Type', 'Device Type', 'Discrepancy Info']

    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_fields)

    for company in discrepancies:
        for each in discrepancies[company]:
            excel = each.split(":")
            csv_writer.writerow(
                [company, excel[0].strip(), excel[1].strip(), excel[2].strip(), excel[3].strip()]
            )
        







