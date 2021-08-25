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
    indexToObject2 = string_event.find("AWS.VMCLAB")
    deletedBy = string_event[indexToObject2 : string_event.find("] [SDDC-Datacenter]")]
    dataExtracted = {'Deleted VM': vmName, 'Deleted By': deletedBy}
    
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