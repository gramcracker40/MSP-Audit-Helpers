import requests, json, base64
from dotenv import dotenv_values
from liongardAPI import LiongardAPI

config = dotenv_values(".env")

# CW instance info
cw_id = config["CW_ID"]
cw_url = config["CW_URL"]

# Linking current connectwise codebase to the module
codebase_req = requests.get(f"https://{cw_url}/login/companyinfo/{cw_id}")
codebase_obj = json.loads(codebase_req.text)
accept_codebase = codebase_obj['VersionCode'].strip('v')

cw_base_url = f"https://{cw_url}/{codebase_obj['Codebase']}apis/3.0"

# CW credentials
clientId = config["CW_CLIENT_ID"]
cw_public = config["CW_PUBLIC"]
cw_private = config["CW_PRIVATE"]

# Packaging authentication headers {cw_id}
authorization_key = base64.b64encode(bytes(f"{cw_id}+{cw_public}:{cw_private}", 'utf-8'))

cw_headers = {
    "clientId": clientId,
    "Authorization":f"Basic {authorization_key.decode()}",
    "Accept": f"application/vnd.connectwise.com+json; version={accept_codebase}"
}

# Liongard credentials
lg_public = config["LG_PUBLIC"]
lg_private = config["LG_PRIVATE"]
lg_instance = config["LG_INSTANCE"]

# Liongard controller
liongard_controller = LiongardAPI(lg_instance, lg_private, lg_public)

# Huntress API credentials
huntress_public = config['HUNTRESS_PUBLIC']
huntress_private = config['HUNTRESS_PRIVATE']


def get_msp_additions(companies_ver=False):
    '''
    returns: list of tuples [('company_name', [all_msp_additions])]
    '''
    a_url = cw_base_url + "/finance/agreements?pageSize=1000"
    agreements = json.loads(requests.get(a_url, headers=cw_headers).text)
    msp_agreements = [x for x in agreements if x['type']['name'] == "Managed Services"]

    # Pulling all additions for each agreement and storing them in a tuple with the company name
    additions = []
    companies = {}
    for agreement in msp_agreements:
        url = cw_base_url + f"/finance/agreements/{agreement['id']}/additions"
        req = requests.get(url, headers=cw_headers)
        all = json.loads(req.text)
        
        additions.append((agreement['company']['name'], all))

        if agreement['company']['name'] not in companies:
            companies[agreement['company']['name']] = [all]
        else:
            companies[agreement['company']['name']].append(all)

    if companies_ver:
        return companies

    return additions

