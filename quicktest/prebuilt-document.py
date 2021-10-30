"""
This code sample shows Prebuilt Document operations with the Azure Form Recognizer client library. 
The async versions of the samples require Python 3.6 or later.

To learn more, please visit the documentation - Quickstart: Form Recognizer Python client library SDKs v3.0
https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/quickstarts/try-v3-python-sdk
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

endpoint = "YOUR_FORM_RECOGNIZER_ENDPOINT"
key = "YOUR_FORM_RECOGNIZER_SUBSCRIPTION_KEY"

formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"

document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-document", formUrl)
result = poller.result()

print("----Key-value pairs found in document----")
for kv_pair in result.key_value_pairs:
    if kv_pair.key and kv_pair.value:
        print("Key '{}': Value: '{}'".format(kv_pair.key.content, kv_pair.value.content))
    else:
        print("Key '{}': Value:".format(kv_pair.key.content))
            
print("\n----Entities found in document----")
for entity in result.entities:
    print("Category '{}': Sub-category: '{}': Content: '{}'".format(entity.category, entity.sub_category,entity.content))

print("----------------------------------------")
