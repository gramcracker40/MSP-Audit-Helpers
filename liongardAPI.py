import requests
import json
from base64 import b64encode


class LiongardAPI():
    '''
    Based off of the Liongard V2/V1 endpoints, found here, 
    URL: https://docs.liongard.com/reference/developer-guide

    Note:
        Liongard is consistently making changes to their API, if any of the URL's become deprecated 
        some parts of this class will lose functionality. 

    Purpose: 
        To effectively and easily manage information regarding your Liongard environments
        programatically and have class LiongardAPI handle it for you. 
    Usage:
        Simply pass through your instance_url found in the url of your Liongard instance --> example: 'us9'

        Generate a public and private api key from your Liongard account and place them in the constructor, this class
        will handle all of the work to set up the connections. 

        The methods are self explanitory and have comments to help you use them. 

    List of Methods: 
        def __init__(self, instance_url="example", private_api_key="example", public_api_key="example")
        def get_environment_count(self)
        def get_environments(self)
        def get_single_environment(self, organizationID)
        def get_name_and_ID(self, file="")
        def single_post_environment(self, payload)
        def bulk_post_environments(self, list_envs)
        def update_single_environment(self, organizationID, payload)
        def bulk_update_environments(self, list_envs)
        def delete_single_environment(self, organizationID)
        def get_related_entities(self, organizationID, file="")
        def get_metrics(self, file="")
        def get_metric_data(self, systemID, metricUUID, file="")
        def system_count(self)
        def get_systems(self)
        def get_system_detail_view(self, systemID)
        def get_system_name_ID(self, file="")
        def search_systems(self, keywords)
        def alert_count(self)
        def get_alerts(self, file="", json="")
        def get_single_alert(self, TaskID, json="")
        def detections_count(self)
        def get_detections(self, file="", json="")
        def get_single_detection(self, DetectionID, json="")
        def get_detections_by_inspectorID(self, inspectorID, json="")
        def get_inspectors(self, file="", json="")
        def get_inspector_versions(self, inspectorID, json="")
        def agent_count(self)
        def get_agents(self, file="", json="")
        def get_single_agent(self, agentID, json="")
        def flush_agent_job_queue(self, agentID)
        def delete_agent(self, agentID)
        def user_count(self)
        def get_users(self, file="", json="")
        def get_single_user(self, UserID, json="")
        def get_groups(self, json="")
        def get_launchpoints_count(self)
        def get_launchpoints(self, file="", json="")
        def get_single_launchpoint(self, LaunchpointID, json="")
        def get_single_launchpoint_log(self, launchpointID, timelineID, json="")
        def run_single_launchpoint(self, launchpointID)
        def bulk_run_launchpoints(self, launchpointIDs=[0])
        def get_timeline_count(self)
        def get_timelines(self, file="", json="")
        def get_single_timeline(self, timelineID)
        def get_timeline_detail(self, timelineID)
    '''


    def __init__(self, instance_url="example", private_api_key="example", public_api_key="example"):
        '''
        Please pass through the 'instance_url', 'private_api_key', 'public_api_key' through in the constructor
        the above are the param names for the constructor. 
        See: https://docs.liongard.com/reference/  for information regarding what those are

        
        '''

        self.public_api_key = public_api_key
        self.private_api_key = private_api_key
        
        self.instance_url = instance_url

        self.passable_key = f"{self.public_api_key}:{self.private_api_key}".encode()
        
        self.passable_key = b64encode(self.passable_key)

        self.headers = {
            "Accept": "application/json",
            "X-ROAR-API-KEY": self.passable_key
        }

        self.sec_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-ROAR-API-KEY": self.passable_key
        }


    @classmethod
    def get_json(self, url, headers):
        '''
        Simply a helper method, repetivive action
        '''
        
        response = requests.get(url, headers=headers)
        obj = json.loads(response.text)
        
        return obj


    @classmethod
    def data_checker(self, data):
        '''
        checks the data returned, if it is empty it will return back that it received nothing and 
        end the function, if there is data it will give the green light for everything beneath it to keep running
        '''
        if not data:
            print("data_checker: the data returned is invalid\n"
                  "Please check constructor info and ensure the keys have been properly typed\n"
                  "Additionally, please ensure any values passed through the parameter set are correct and accurate")
            return 0
        else:
            return data

    
    @classmethod
    def dump_json(self, data, file):
        '''
        Helper function: dumps json to user specified file
        '''
        if file == "":
            return 0
        else:
            dumper = open(f"{file}.json", 'w')
            json.dump(data, dumper)


    def environment_count(self):
        '''
        Grabs the total count of your Liongard Environments
        return an integer number of your environment count
        '''
        
        count_request = requests.get(f"https://{self.instance_url}.app.liongard.com/api/v2/environments/count", headers=self.headers)
        count = json.loads(count_request.content)

        if count['Success'] == False:
            print(f"error occured while posting data\nmessage: {count['Message']}")
            return count['Success']

        return count['Data']


    def get_environments(self):    
        '''
        Grabs a list of the environments in the Liongard instance for the keys passed through.
        it will return an easily parseable JSON object. 
        '''

        environments_request = requests.get(f"https://{self.instance_url}.app.liongard.com/api/v2/environments/", headers=self.headers)
        environments_json = json.loads(environments_request.content)

        if environments_json['Success'] == False:
            print(f"error occured while posting data\nmessage: {environments_json['Message']}")
            return environments_json['Success']

        return environments_json['Data']


    def get_single_environment(self, organizationID):
        '''
        Simply pass the organization ID of the environment you are trying to get info on

        Returns: environment JSON object specific to the ID passed through
        '''


        url = f"https://{self.instance_url}.app.liongard.com/api/v2/environments/{organizationID}"
        single_get = requests.get(url, headers=self.headers)

        single_env = json.loads(single_get.text)

        if single_env['Success'] == False:
            print(f"error occured while posting data\nmessage: {single_env['Message']}")
            return single_env['Success']

        return single_env['Data']


    def get_name_and_ID(self, file=""):
        '''
        Returns dictionary object containing the environment ID as the key and the Name as the value:
        simply leave the file field blank

        ---> Printing to File (Optional):
        Specify the file name you would like the environments ID's and Names to be outputted to.
        specify like so -> (file="environment_ID")
        Will simply create a .txt file in your current directory with the name you pass
        and list off the environment name and their Liongard API ID. --- 
        
        Please note: 
        .txt is added automatically so simply specify the name as a string 
        '''
        
        environments = self.get_environments()
        key_value = {}

        if file != "":
            output_file = open(f"{file}.txt", 'w')


        for env in environments:
            if file == "":
                key_value[env['ID']] = env['Name']
            else:
                output_file.write(f"{env['ID']} : {env['Name']}\n")
                key_value[env['ID']] = env['Name']
        
        return key_value
    

    def single_post_environment(self, payload):
        '''
        Below is an example of the format the data you are posting needs to be in for this function to run properly
        payload = {
            "Name": "new env",
            "Description": "im a new environment (Test)",
            "Parent": "big man company",
            "ShortName": "N.E",
            "Tier": "Core"
        }
        '''
        
        url = f"https://{self.instance_url}.app.liongard.com/api/v2/environments/"        
        single_post = requests.get(url, headers=self.sec_headers)

        single_response = json.loads(single_post.text)
        
        if single_response['Success'] == False:
            print(f"error occured while posting data\nmessage: {single_response['Message']}")
            return single_response['Success']

        return single_response['Data']



    def bulk_post_environments(self, list_envs):
        '''
        'list_envs' --- must be in the format provided below 

        payload = [{
            "Name": "test company",
            "Description": "a very basic company indeed",
            "Tier": "Core",
            "Parent": "parent company", --) (Must be a legitimate company in Liongard already)
            "ShortName": "very basic , inc"
        },
        {
            "Name": "nice company man"
            "Description": "a very basic company indeed",
            "Tier": "Core",
            "Parent": "parent company", --) (Must be a legitimate company in Liongard already)
            "ShortName": "very basic , inc"
        }
        ]

        Please format the data needing to be posted in to Liongard properly according
        to the provided example and more details
        '''

        bulk_post = requests.post(f"https://{self.instance_url}.app.liongard.com/api/v2/environments/bulk", json=list_envs, headers=self.sec_headers)

        bulk_response = json.loads(bulk_post.text)
    
        if bulk_response['Success'] == False:
            print(f"error occured while posting data\nmessage: {bulk_response['Message']}")

        return f"Successful: {bulk_response['Success']}"


    def bulk_update_environments(self, list_envs):
        '''
        example acceptable input, please ensure you are passing the proper environment ID's
        any fields you pass will be updated

        payload = [
            {
                "environmentId": "9754",
                "Name": "now im test company",
                "Description": "coolest test",
                "Tier": "Core"
            },
            {
                "environmentId": "9755",
                "Name": "the nicest company",
                "Description": "i have become nice",
                "Tier": "Core"
            }
        ]
        
        '''

        bulk_update = requests.put(f"https://{self.instance_url}.app.liongard.com/api/v2/environments/", json=list_envs, headers=self.sec_headers)

        bulk_response = json.loads(bulk_update.text)
    
        if bulk_response['Success'] == False:
            print(f"error occured while posting data\nmessage: {bulk_response['Message']}")

        return f"Successful: {bulk_response['Success']}"


    def update_single_environment(self, organizationID, payload):
        '''
        example of an acceptable payload to pass through to 'payload'

        payload = {
            "Name": "im clearly testing this",
            "Description": "clearly",
            "Parent": "big boss environment", --> ensure this is a environment in the Liongard instance
            "ShortName": "bbe",
            "Tier": "Core"
        }

        organizationID --- please pass the ID of the environment you are trying to change the details for
            as a string

        '''
        
        url = f"https://{self.instance_url}.app.liongard.com/api/v2/environments/{organizationID}"

        single_update = requests.put(url, json=payload, headers=self.sec_headers)

        single_response = json.loads(single_update.text)

        if single_response['Success'] == False:
            print(f"error occured while posting data\nmessage: {single_response['Message']}")

        return f"Successful: {single_response['Success']}"


    def delete_single_environment(self, organizationID):
        '''
        When successful this method will simply return the ID you passed through

        Please enter a valid organization ID
        '''
        
        url = f"https://{self.instance_url}.app.liongard.com/api/v2/environments/{organizationID}"

        single_delete = requests.delete(url, headers=self.headers)

        delete_response = json.loads(single_delete.content)

        if delete_response['Success'] == False:
            print(f"error occured while posting data\nmessage: {delete_response['Message']}")
            return delete_response['Success']

        return delete_response['Data']


    def get_related_entities(self, organizationID, file=""):
        '''
        Grabs all the related entities to the environment referenced by organizationID in the params
         and return the 'ID' , 'Alias', 'SystemID', 'InspectorID', 'InspectorName', 'Enabled', and its 'Status'

        If you would like the related items neatly outputted to a file for later reference please specify the 
         file name as such --> file="output"  ---> .txt will be added automatically
        '''
        
        url = f"https://{self.instance_url}.app.liongard.com/api/v2/environments/{organizationID}/relatedEntities"

        related_request = requests.get(url, headers=self.headers)

        related_response = json.loads(related_request.text)
        
        if related_response['Success'] == False:
            print(f"error occured while posting data\nmessage: {related_response['Message']}")
            return related_response['Success']

        if file != "":
            outputF = open(f"{file}.txt", 'w')

            for item in related_response['Data']['LaunchPoints']:
                outputF.write(f"Name: {item['Alias']}, ID: {item['ID']}, InspectorID: {item['InspectorID']}, SystemID: {item['SystemID']}, Inspector Name: {item['InspectorName']}, Status: {item['Status']}, Enabled: {item['Enabled']} \n")

        return related_response['Data']['LaunchPoints']

    
    def get_metrics(self, file=""):
        '''
        Grabs and returns list of all the metrics in the Liongard instance
        these metrics will be individual dictionaries that will be easily filtered
        Contains all necessary field --- ID, SystemID, Name, etc.

        File: 
            to use, simply specify the name you want the file to be called, this function
            will write every single metric into the file neatly to be filtered through
            ex: (file="output")
        '''
        
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/metrics"

        metrics_request = requests.get(url, headers=self.headers)
        metrics_response = json.loads(metrics_request.text)

        # if metrics_response['Success'] == False:
        #     print(f"error occured while posting data\nmessage: {metrics_response['Message']}")
        #     return metrics_response['Success']
        

        if file != "":
            outputF = open(f"{file}.txt", 'w')

            for metric in metrics_response:
                outputF.write(f"Name: {metric['Name']}, ID: {metric['ID']}, UUID: {metric['UUID']}, UCK: {metric['UCK']}, Metric Display: {metric['MetricDisplay']}\n")

        return metrics_response


    # def create_metric(self, name="", InspectorID=0, queries):
    #     '''
    #     example usage:
    #     payload = {"Queries": [
    #         {
    #             "Query": "length(Computers)",
    #             "InspectorVersionID": 1353
    #         }
    #     ]}
    #     '''
    #     pass
    # TODO --> implement create, update and delete methods for metrics 

    def get_metric_data(self, systemID=0, metricUUID="", metricID=0, file=""):
        '''
        INFO: Can only pass through 10 seperate system ID's to parse at a time
                Can only pass through 10 seperate metricID's to parse at a time

        systemID --> Please pass either a single system ID or a list of system ID's no more than 10
        metricUUID --> Please pass through a string for the metricUUID of the metric you wish to see values for
        metricID --> (int) Can be a list of integers or a single integer. 
        
        Please choose either metricUUID or metricID to grab the metric data. Do not use both
        this is not how the api was designed and it is not needed. Simply choose one
        
        '''

        #initial parsing to create system_string to pass through to the URL
        system_string = ""
        if type(systemID) == list:
            for num in systemID:
                system_string += f"{str(num)},"

        elif type(systemID) == int or type(systemID) == str:
            system_string = f"{systemID},"
        else:
            print("Error Occurred: did not pass 'int', 'str', or 'list' of system ID's")    
            return 0


        #initial parsing to create metric_string to pass through to the URL
        metric_string = ""
        if type(metricUUID) == list and metricUUID != "":
            for num in metricUUID:
                metric_string += f"{num},"
        elif type(metricUUID) == str and metricUUID != "":
            metric_string = f"{metricUUID},"
        elif type(metricUUID) == int:
            metric_string = f"{metricUUID},"

        if type(metricID) == list and metricID != 0:
            for num in metricID:
                metric_string += f"{num},"
        elif type(metricID) == str and metricID != 0:
            metric_string = f"{metricID},"
        elif type(metricID) == int:
            metric_string = f"{metricID},"

        #taking off the last comma
        system_string = system_string[:-1]
        metric_string = metric_string[:-1]
        
        #passing through to the url 
        if metricUUID != "":    
            #creating the URL to pass through to the API
            url = f"https://{self.instance_url}.app.liongard.com/api/v1/metrics/bulk?uuid={metric_string}&systems={system_string}"
        if metricID != 0:
            url = f"https://{self.instance_url}.app.liongard.com/api/v1/metrics/bulk?metrics={metric_string}&systems={system_string}"

        data_request = requests.get(url, headers=self.sec_headers)
        data_obj = json.loads(data_request.text)

        # if data_obj['Success'] == False:
        #     print(f"error occured while posting data\nmessage: {data_obj['Message']}")
        #     return data_obj['Success']


        return data_obj

        # if file != "":
        #     outputF = open(f"{file}.txt", 'w')

        #     #for item in data_obj['Data']:
        #         #outputF.write(f"Name: {item['Alias']}, ID: {item['ID']}, InspectorID: {item['InspectorID']}, SystemID: {item['SystemID']}, Inspector Name: {item['InspectorName']}, Status: {item['Status']}, Enabled: {item['Enabled']} \n")


    def system_count(self):
        '''
        Grabs the total number of systems in the liongard instance

        Systems being the individual inspectors within the client environment

        returns: <int> --> number of systems
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/systems/count"

        systems_request = requests.get(url, headers=self.headers)
        systems_obj = systems_request.text

        return int(systems_obj)

    
    def get_systems(self):
        '''
        grabs a list of all the systems in the liongard environment

        specify what info you want to see 

        TODO implement the rest: https://docs.liongard.com/reference/systems
        '''
        
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/systems"

        systems_obj = LiongardAPI.get_json(url, headers=self.headers)

        return systems_obj


    def get_system_detail_view(self, systemID):
        '''
        Purpose:
            Grabs the data print of an inspector within your Liongard instance

        Usage:
            call whenever you want the full data print of a system for that day
            this method gives you access to the data that you can build JMESpath queries on
            in your instance

        systemID ---> must be an integer
        '''
        if type(systemID) != int:
            return f"System ID is not an integer: {type(systemID)}"
        
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/systems/{systemID}/view"

        data_print = LiongardAPI.get_json(url, self.headers)

        return data_print['raw']
    
    
    def get_system_name_ID(self, file=""):
        '''
        Grabs all the systems names and IDs and returns them in a dictionary

        file ---> use this by specifying just the file name -> ex: "systems_name_and_id"
            this option will create a txt file in your current directory and write all of 
            the systems names, ID's, and environments for you to look through easily which systems you want. 
        '''
        
        name_and_id = {}

        systems = LiongardAPI.get_systems(self)

        for system in systems:
            name_and_id[system['Name']] = system['ID']
            
        if file != "":
            output = open(f"{file}.txt", 'w')
            for item in systems:
                output.write(f"Name: {item['Name']}, ID: {item['ID']}, Environment: {item['Environment']['Name']}\n")

        return name_and_id


    def search_systems(self, keywords):
        '''
        This function will filter through all of your systems and search for keywords
        example: 'Sonicwall', 'sonicwall', 'SonicWall'

        you may pass multiple words to be searched if you would like but only one is required

        type(keywords) ---> Either a string or a list of strings

        '''
        systems = LiongardAPI.get_systems()

        matches = []
        
        for key in keywords:
            for system in systems:
                if key in system['Name'] and system not in matches:
                    matches.append(system)

        return matches


    def alert_count(self):
        '''
        Grabs the total number of alerts in the Liongard instance

        returns: (int)
        '''

        url = f"https://{self.instance_url}.app.liongard.com/api/v1/tasks/count"

        alert_req = requests.get(url, headers=self.headers)

        data = alert_req.text

        return data


    def get_alerts(self, file="", json=""):
        '''
        returns a list of alerts that you can loop through to grab key info pertaining
        to each individual alert

        use .keys() to see what fields you can access in each individual element
        
        file ---> specify the name of the output file you would like to use to output
            NAME, ENVIRONMENT, ID AND STATUS line by line to a .txt file
            ex: "output"
        '''

        url = f"https://{self.instance_url}.app.liongard.com/api/v1/tasks"

        data = LiongardAPI.get_json(url, self.headers)

        data = LiongardAPI.data_checker(data)

        LiongardAPI.dump_json(data, json)


        if file != "" and data != 0:
            output = open(f"{file}.txt", 'w')
            for item in data:
                output.write(f"Name: {item['Name']} : Environment: {item['Environment']['Name']} : ID: {item['ID']} : Status: {item['Status']['Name']}\n")
                

        return data

    
    def get_single_alert(self, TaskID, json=""):
        '''
        Grabs a single alert based on the TaskID passed through

        If an empty list is returned the TaskID is invalid, please grab a list of the alerts 
        and find a valid one. Liongards API does not provide error messaging for this endpoint
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/tasks/{TaskID}"

        data = LiongardAPI.get_json(url, self.headers)

        LiongardAPI.dump_json(data, json)

        return data


    def get_alerts_by_inspectorID(self, inspectorID):
        '''
        Grabs a list of alerts for a specific inspector based on the inspectorID
        passed through in the params

        return: JSON parceable object
        NOTE finish implementation
        '''
        pass


    def get_alerts_by_environmentID(self, environmentID):
        '''
        Grabs a list of alerts for a specific environment based on the environmentID
        passed through in the params

        return: JSON parceable object
        NOTE finish implementation
        '''
        pass


    def detections_count(self):
        '''
        Grabs the count of total detections in your Liongard instance and returns it as
        an integer
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/detections/count"

        data = LiongardAPI.get_json(url, self.headers)

        return data


    def get_detections(self, file="", json=""):
        '''
        Grabs a list of all the detections that have occurred within your Liongard instance
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/detections"

        data = LiongardAPI.get_json(url, self.headers)

        LiongardAPI.dump_json(data, json)

        if file != "":
            output = open(f"{file}.txt", 'w')
            for detection in data:
                output.write(f"Name: {detection['Name']} : DetectionID: {detection['ID']} : Environment: {detection['Environment']['Name']} : System: {detection['System']['Name']}\n")

        return data


    def get_single_detection(self, DetectionID, json=""):
        '''
        Grabs a specific detection based off of the ID you pass through in the parameter set
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/detections/{DetectionID}"

        data = LiongardAPI.get_json(url, self.headers)

        LiongardAPI.dump_json(data, json)

        if not data:
            print("Error: no data came back, please check the DetectionID passed through")
            return 0

        return data


    def get_detections_by_inspectorID(self, inspectorID, json=""):
        '''
        Grabs all detections for a specific inspector type

        inspectorID ---> please pass an accurate inspector ID, to get a list of those
                call the method get_inspectors()
        '''

        data = LiongardAPI.get_detections(self)

        detections = []
        for detection in data:
            if detection['Inspector']['ID'] == inspectorID:
                detections.append(detection)
        

        LiongardAPI.dump_json(detections, json)

        return detections


    def get_inspectors(self, file="", json=""):
        '''
        Grabs a list of available inspectors and all relative fields. Can be used in later methods
        for filtering the data and also seeing key info used for that inspector throughout the API
        
        file ---> parameter to be used to specify name of output file to send the info to. 
            ex: test.get_inspectors(file="output")
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/inspectors"

        data = LiongardAPI.get_json(url, self.headers)

        if not data:
            print("Please check the info in your constructor: No data exists")
            return 0

        if file != "":
            output = open(f"{file}.txt", 'w')
            for item in data:
                output.write(f"Name: {item['Name']} , InspectorID: {item['ID']} , Alias: {item['Alias']}\n")

        LiongardAPI.dump_json(data, json)

        return data


    def get_inspector_versions(self, inspectorID, json=""):
        '''
        grabs a list of inspector versions and their ID based off of the inspectorID
        passed through in the parameters

        required to be able to post new metrics using the API
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/inspector/{inspectorID}/versions"

        data = LiongardAPI.get_json(url, self.headers)

        if not data:
            print("Info wrong: please check the inspectorID passed to the method")
            return 0

        LiongardAPI.dump_json(data, json)

        return data


    def agent_count(self):
        '''
        Grabs the total number of agents in the Liongard instance

        returns --> integer
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/agents/count"

        data = LiongardAPI.get_json(url, self.headers)

        return data


    def get_agents(self, file="", json=""):
        '''
        Grabs a list of all the agents in the Liongard instance

        returns -> list of dictionaries (Agents)

        file ---> use this to display key agent info into a file to have each
            agent ID/UID easily viewable. 
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/agents"

    
        data = LiongardAPI.get_json(url, self.headers)

        if not data:
            print("No data exists, please check information in constructor")
            return 0

        if file != "":
            output = open(f"{file}.txt", 'w')
            for item in data:
                output.write(f"Agent name: {item['Name']}, Agent ID: {item['ID']}, UID: {item['UID']}\n")

        LiongardAPI.dump_json(data, json)

        return data

    def get_single_agent(self, agentID, json=""):
        '''
        grabs a single agent based off of the agentID passed through

        returns --> json parceable object
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/agents/{agentID}"

        data = LiongardAPI.get_json(url, self.headers)

        if not data:
            print("Agent does not exist: try another ID")
            return 0

        LiongardAPI.dump_json(data, json)

        return data


    def flush_agent_job_queue(self, agentID):
        '''
        Flushes the job queue of the agent associated to the agentID passed 
        through

        will return failed to purge agents queue if the agent does not have
        any jobs 
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/agents/{agentID}/flush"

        req = requests.post(url, headers=self.headers)

        return req.text
    

    def delete_agent(self, agentID):
        '''
        Deletes an agent based off of the agentID passed through to it.

        Warning: Deleted agents can not be recovered 
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/agents/{agentID}"

        response = requests.delete(url, headers=self.headers)

        return response.text

    '''
    NOTE implement updating agents
    '''

    def user_count(self):
        '''
        Grabs the number of unique users in the Liongard instance

        returns --> (int) number of users
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/users/count"

        data = LiongardAPI.get_json(url, self.headers)

        return data


    def get_users(self, file="", json=""):
        '''
        Grabs a list of users from the Liongard instance
        
        file ---> used to place all user Names and IDs on a txt file to easily reference
                names with their ID's

        returns ---> (list) users
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/users"

        data = LiongardAPI.get_json(url, self.headers)

        if not data:
            print("Please check constructor info and ensure the keys have been properly typed")
            return 0
        
        if file != "":
            output = open(f"{file}.txt", 'w')
            for item in data:
                output.write(f"Name: {item['FirstName']} {item['LastName']}, UserID: {item['ID']}\n")

        LiongardAPI.dump_json(data, json)

        return data


    def get_single_user(self, UserID, json=""):
        '''
        Grabs a single user specified by the UserID passed through in the params

        returns a JSON object pertaining to that user
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/users/{UserID}"

        data = LiongardAPI.get_json(url, self.headers)

        if not data:
            print("error: no data was returned (check constructor)")
            return 0

        LiongardAPI.dump_json(data, json)

        return data


    #TODO --- IMPLEMENT create_user delete_user update_user
    #def create_user(self, )


    def get_groups(self, json=""):
        '''
        Grabs a list of all the groups in the Liongard instance 

        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/groups"

        data = LiongardAPI.get_json(url, self.headers)

        if not data:
            print("error: no data returned (check constructor details)")
            return 0

        LiongardAPI.dump_json(data, json)

        return data


    def get_launchpoints_count(self):
        '''
        Grabs the total count of launchpoints within the Liongard instance

        returns: <int>
        '''

        url = f"https://{self.instance_url}.app.liongard.com/api/v1/launchpoints/count"

        data = LiongardAPI.get_json(url, self.headers)

        data = LiongardAPI.data_checker(data)

        if data == 0:
            print("No data was returned, check the constructor info")
            return 0

        return data

    
    def get_launchpoints(self, file="", json=""):
        '''
        Grabs all of the launchpoints and returns them as a list of dictionaries
        see: https://docs.liongard.com/reference/getlaunchpoints for more info.

        returns: <list>

        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/launchpoints"

        data = LiongardAPI.get_json(url, self.headers)

        data = LiongardAPI.data_checker(data)

        if data == 0:
            return 0

        if file != "":
            output = open(f"{file}.txt", 'w')
            for launchpoint in data:
                output.write(f"Name: {launchpoint['Alias']}, ID: {launchpoint['ID']}, Inspector Type: {launchpoint['Inspector']['Name']}\n")

        LiongardAPI.dump_json(data, json)

        return data

    
    def get_single_launchpoint(self, LaunchpointID, json=""):
        '''
        Grabs a single launchpoint by their LaunchpointID 
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/launchpoints/{LaunchpointID}"

        data = LiongardAPI.get_json(url, self.headers)

        data = LiongardAPI.data_checker(data)

        if data == 0:
            return 0

        LiongardAPI.dump_json(data, json)

        return data

            
    #NOTE implement adding, deleting, and editing launchpoints

    def get_single_launchpoint_log(self, launchpointID, timelineID, json=""):
        '''
        built to grab a specific log for any launchpoint at any timeline id


        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/logs?launchpoint={launchpointID}&timeline={timelineID}"

        data = LiongardAPI.get_json(url, self.headers)

        data = LiongardAPI.data_checker(data)

        if data == 0:
            return 0

        LiongardAPI.dump_json(data, json)

        return data

    
    def run_single_launchpoint(self, launchpointID):
        '''
        Simply pass the ID of the launchpoint you want to run and this function will go and force run it
          your Liongard instance. 

          returns a callback confirming the ID that ran
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/launchpoints/{launchpointID}/run"

        data = LiongardAPI.get_json(url, self.headers)

        data = LiongardAPI.data_checker(data)

        if data == 0:
            return 0

        return data


    def bulk_run_launchpoints(self, launchpointIDs=[0]):
        '''
        description:
            runs multiple inspections based off of the ID's passed through 
        
        LaunchpointIDs --> must be a list of actual launchpoint IDs to run --- <int>

        returns:  a list of all the ones that ran, and all the ones that errored
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/launchpoints/run"

        payload = {"LaunchPoints": launchpointIDs}

        response = requests.post(url, json=payload, headers=self.headers)

        return response.text

    
    def get_timeline_count(self):
        '''
        description:
            grabs the total number of timelines in your Liongard instance

        returns: <int>
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/timeline/count"

        data = LiongardAPI.get_json(url, self.headers)

        data = LiongardAPI.data_checker(data)

        if data == 0:
            return 0

        return data

    def get_timelines(self, file="", json=""):
        '''
        description:
            grabs a list of all the timeline entries in your liongard instance

        returns:
            list of all timelines
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/timeline"

        data = LiongardAPI.get_json(url, self.headers)

        data = LiongardAPI.data_checker(data)

        if data == 0:
            return 0

        if file != "":
            output = open(f"{file}.txt", 'w')
            for timeline in data:
                output.write(f"ID: {timeline['ID']}, Launchpoint: {timeline['Launchpoint']['Alias']}, Change Detections: {timeline['ChangeDetections']}\n")

        LiongardAPI.dump_json(data, json)

        return data


    def get_single_timeline(self, timelineID):
        '''
        description:
            grabs a single timeline based on the TimelineID you pass through
        
        returns:
            single timeline object
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/timeline/{timelineID}"

        data = LiongardAPI.get_json(url, self.headers)

        data = LiongardAPI.data_checker(data)

        if data == 0:
            return 0

        return data

    def get_timeline_detail(self, timelineID):
        '''
        description:
            grabs the details of the timelines and returns them
        '''
        url = f"https://{self.instance_url}.app.liongard.com/api/v1/timeline/{timelineID}/detail"

        data = LiongardAPI.get_json(url, self.headers)

        data = LiongardAPI.data_checker(data)

        if data == 0:
            return 0

        return data


# test = LiongardAPI("instance_url", "private_key", "public_key")
