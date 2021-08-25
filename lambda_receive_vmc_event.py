import json, boto3

client = boto3.client('events')

#Global Variables
source = "vmc.sddc"
detailType = ""
eventBus = ""


def lambda_handler(event, context):
    print("Received event: " + str(event))
    string_event = str(event)
    indexToObject = string_event.find("Removed ")
    vmName = string_event[indexToObject + 8 : string_event.find(" on", indexToObject)]
    print(vmName)
    dataExtracted = {'Deleted VM': vmName}
    
    response = client.put_events(
        Entries=[
            {
                'Source': source,
                'DetailType': detailType,
                'Detail': json.dumps(dataExtracted),
                'EventBusName': eventBus
            },
    ]
)