
import json
import time
import base64
from typing import Literal
from reportlab.pdfgen.canvas import Canvas
from testing import account, contact, reports, forms
from testing.tracking import tabs, records, queues, items
from xenqu.models import Address, Contact
from xenqu import XenquAPI

client_id = "WKKXPxwS0UqGy0199MMA"
client_secret = "7BvzE387BoQOWWTOpQMLI8C88xhE9FkwQCCN2ZosBdw"
private_key = open('./privatekey.pem', 'rb').read()
subscriber = "5f3ed190c32e5f000186bb76"

api = XenquAPI(clientId=client_id, clientSecret=client_secret, pemPrivateKey=private_key, subscriber=subscriber, baseUrl='https://stage.xenqu.com')

##? Account Routes Testing
def accountTesting():
    print('~~ Account ~~')
    return (
        # '~~ Account ~~\n' +
        account.main(api=api) +
        '\n'
    )

##? Contact Routes Testing
def contactTesting():
    print('~~ Contact ~~')
    return (
        # '~~ Contact ~~\n' + 
        contact.main(api=api) + 
        '\n'
    )

##? [Tracking] -|- Tab
def trackingTabTesting():
    print('~~ [Tracking] | Tab ~~')
    return (
        # '~~ [Tracking] | Tab ~~\n' + 
        tabs.main(api=api) + 
        '\n'
    )

##? [Tracking] -|- Records
def trackingRecordTesting():
    print('~~ [Tracking] | Record ~~')
    return (
        records.main(api=api) + 
        '\n'
    )

##? [Tracking] -|- Queue
def trackingQueueTesting():
    print('~~ [Tracking] | Queue ~~')
    return (
        queues.main(api=api) + 
        '\n'
    )

##? [Tracking] -|- Item
def trackingItemTesting():
    print('~~ [Tracking] | Item ~~')
    return (
        items.main(api=api) + 
        '\n'
    )

##? Form Routes Testing
def formTesting():
    print('~~ Form ~~')
    return (
        forms.main(api=api) + 
        '\n'
    )

##? Report Routes Testing
def reportTesting():
    print('~~ Report ~~')
    return (
        reports.main(api=api) + 
        '\n'
    )

def generatePDFTesting(instanceId: int):
    pdfId = json.loads(api.forms.getInstance(instanceId=instanceId))["definition"]["pdf_id"]
    api.forms.generatePdf(instanceId=instanceId, signPdf=True, addInfoFooter=True)
    time.sleep(5.0)
    newPdfId = json.loads(api.forms.getInstance(instanceId=instanceId))["definition"]["pdf_id"]

    if (pdfId == newPdfId):
        return "Polling time was not long enough :/"
    
    tempHandleId = json.loads(api.forms.getFormFile(instanceId=instanceId, filesId=newPdfId))["_temp_handle_id"]
    file = api.files.download(tempHandleId=tempHandleId)
    pdf_path = './out.pdf'
    pdf_file = Canvas(pdf_path)
    with open(pdf_path, 'wb') as f:
        f.write(file)

def uploadFileTesting(fileBytes: bytes, fileType: Literal['pdf', 'jpeg', 'txt', 'png'] = 'pdf'):
    l = len(fileBytes)
    encoded_string = base64.b64encode(fileBytes).decode('utf-8')
    if fileType == 'pdf':
        r = api.files.upload(chunkData=f"data:appication/pdf;base64,{encoded_string}", chunkSeq=0, chunkStart=0, chunkEnd=l, chunkLimit=l, chunkSize=l, totalSize=l, totalChunks=1)
    elif fileType == 'txt':
        r = api.files.upload(chunkData=f"data:text/plain;base64,{encoded_string}", chunkSeq=0, chunkStart=0, chunkEnd=l, chunkLimit=l, chunkSize=l, totalSize=l, totalChunks=1)
    elif fileType == 'png':
        r = api.files.upload(chunkData=f"data:image/png;base64,{encoded_string}", chunkSeq=0, chunkStart=0, chunkEnd=l, chunkLimit=l, chunkSize=l, totalSize=l, totalChunks=1)
    else:
        r = api.files.upload(chunkData=f"data:image/jpeg;base64,{encoded_string}", chunkSeq=0, chunkStart=0, chunkEnd=l, chunkLimit=l, chunkSize=l, totalSize=l, totalChunks=1)

    with open('./encoded.txt', 'w+') as f:
        f.write(encoded_string)
    return r

def downloadAttachmentTesting(trackingId: int):
    data = json.loads(api.tracking.items.getListAttachments(trackingId=trackingId))
    attachmentId = data["_id"]
    filesId = data["files"][0]["files_id"]
    tempHandleId = json.loads(api.tracking.items.getDownloadAttachment(attachmentId=attachmentId, filesId=filesId))["_temp_handle_id"]
    file_bytes = api.files.download(tempHandleId=tempHandleId)
    with open('out.jpg', 'wb') as f:
        f.write(file_bytes)

def addAttachmentTesting(trackingId: int, contentType: str, fileName: str):
    data = json.loads(api.tracking.items.getListAttachments(trackingId=trackingId))
    attachmentId = data["_id"]
    with open('./text.txt', 'rb') as f:
        fileBytes = f.read()
    tempHandleId = json.loads(uploadFileTesting(fileBytes=fileBytes, fileType='txt'))["fileHandle"]
    r = api.tracking.items.addAttachment(trackingId=trackingId, tempHandleId=tempHandleId, attachmentId=attachmentId, contentType='text/plain', fileName='text.txt', order=0, filesId=None)
    return r

def addJpg(trackingId: int, fileName: str):
    data = json.loads(api.tracking.items.getListAttachments(trackingId=trackingId))
    attachmentId = data["_id"]
    with open(fileName, 'rb') as f:
        fileBytes = f.read()
    tempHandleId = json.loads(uploadFileTesting(fileBytes=fileBytes, fileType='jpeg'))["fileHandle"]
    r = api.tracking.items.addAttachment(trackingId=trackingId, tempHandleId=tempHandleId, attachmentId=attachmentId, contentType='image/jpeg', fileName=fileName, order=0, filesId=None)
    return r

    
def updateAttachmentTesting(trackingId: int):
    data = json.loads(api.tracking.items.getListAttachments(trackingId=trackingId))
    attachmentId = data["_id"]
    filesId = data["files"][0]["files_id"]
    tempHandleId = json.loads(uploadFileTesting(open('./pic.jpg', 'rb').read(), fileType='jpeg'))["fileHandle"]
    r = api.tracking.items.updateAttachment(trackingId=trackingId, attachmentId=attachmentId, filesId=filesId, contentType='image/jpeg', fileName='pic.jpg', order=0, tempHandleId=tempHandleId)
    return r

def deleteAttachmentTesting(trackingId: int):
    data = json.loads(api.tracking.items.getListAttachments(trackingId=trackingId))
    attachmentId = data["_id"]
    filesId = data["files"][0]["files_id"]
    r = api.tracking.items.deleteAttachment(attachmentId=attachmentId, filesId=filesId)
    return r


if __name__ == "__main__":
    # with open('./out.pdf', 'rb') as f:
    #     print(uploadFileTesting(fileBytes=f.read()))

    with open('./out.json', 'w+') as f:
        # f.write(contactTesting())
        # f.write(trackingTabTesting())
        # f.write(trackingRecordTesting())
        # f.write(trackingQueueTesting())
        f.write(trackingItemTesting())
        # f.write(formTesting())
        # f.write(reportTesting())

    # generatePDFTesting(instanceId=8415)

    # downloadAttachmentTesting(trackingId=13052)

    # print(addAttachmentTesting(trackingId=13052))
    # print(addJpg(trackingId=13052, fileName='pic.jpg'))

    # print(updateAttachmentTesting(trackingId=13052))

    # print(deleteAttachmentTesting(trackingId=13052))

    pass
