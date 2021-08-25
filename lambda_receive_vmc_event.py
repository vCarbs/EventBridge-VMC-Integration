import json, boto3

client = boto3.client('events')

#Global Variables
source = "vmc.sddc"
detailType = ""
eventBus = ""


def lambda_handler(event, context):
    print("Received event: " + str(event))
    string_event = str(event)
    if string_event.find('vim.event.VmCreatedEvent') == -1:
        indexToObject = string_event.find("Removed ")
        vmName = string_event[indexToObject + 8 : string_event.find(" on", indexToObject)]
        print(vmName)
        indexToObject2 = string_event.find("AWS.VMCLAB")
        deletedBy = string_event[indexToObject2 + 12 : string_event.find("] [SDDC-Datacenter]")]
        dataExtracted = {'Deleted VM': vmName, 'Deleted By': deletedBy}
        detailType = "VM Deleted"
    else:
        indexToObject = string_event.find("Created virtual machine ")
        vmName = string_event[indexToObject + 24 : string_event.find(" on", indexToObject)]
        print(vmName)
        indexToObject2 = string_event.find("AWS.VMCLAB")
        createdBy = string_event[indexToObject2 + 12 : string_event.find("] [SDDC-Datacenter]")]
        dataExtracted = {'Created VM': vmName, 'Created By': createdBy}
        detailType = "VM Created"
    
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