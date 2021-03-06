import json, boto3

client = boto3.client('events')

#Global Variables
source = "vmc.sddc"
eventBus = ""


def lambda_handler(event, context):
    print("Received event: " + str(event))
    string_event = str(event)
    if string_event.find('vim.event.VmRemovedEvent') > -1:
        indexToObject = string_event.find("Removed ")
        vmName = string_event[indexToObject + 8 : string_event.find(" on", indexToObject)]
        print(vmName)
        indexToObject2 = string_event.find("[info]")
        deletedBy = string_event[indexToObject2 + 8 : string_event.find("] [SDDC-Datacenter]")]
        dataExtracted = {'Deleted VM': vmName, 'Deleted By': deletedBy}
        detailType = "VM Deleted"
        
    elif string_event.find('vim.event.VmDeployedEvent') > -1:
        indexToObject = string_event.find("deployed to ")
        vmName = string_event[indexToObject + 12 : string_event.find(" on", indexToObject)]
        print(vmName)
        indexToObject2 = string_event.find("Template ")
        templateName = string_event[indexToObject2 + 9 : string_event.find(" deployed to", indexToObject2)]
        indexToObject3 = string_event.find("[info]")
        createdBy = string_event[indexToObject3 + 8 : string_event.find("] [SDDC-Datacenter]")]
        dataExtracted = {'Created VM': vmName, 'Template Used': templateName, 'Created By': createdBy}
        detailType = "VM created from template"
        
    elif string_event.find('vim.event.VmBeingClonedEvent') > -1:
        indexToObject = string_event.find("SDDC-Datacenter to ")
        vmName = string_event[indexToObject + 19 : string_event.find(" on", indexToObject)]
        print(vmName)
        indexToObject2 = string_event.find("Cloning ")
        templateName = string_event[indexToObject2 + 8 : string_event.find(" on", indexToObject2)]
        dataExtracted = {'Created VM': vmName, 'Cloned From': templateName}
        detailType = "VM cloned from template"
        
    else:
        indexToObject = string_event.find("Created virtual machine ")
        vmName = string_event[indexToObject + 24 : string_event.find(" on", indexToObject)]
        print(vmName)
        indexToObject2 = string_event.find("[info]")
        createdBy = string_event[indexToObject2 + 8 : string_event.find("] [SDDC-Datacenter]")]
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