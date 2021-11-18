# coding: utf-8

import os
import pandas as pd

endpoint = os.environ["AZURE_LANGUAGE_ENDPOINT"]
key = os.environ["AZURE_LANGUAGE_KEY"]

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Example method for summarizing text
def extractive_summarization(client, document):
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import (
        TextAnalyticsClient,
        ExtractSummaryAction
    ) 

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractSummaryAction(MaxSentenceCount=4)
        ],
    )

    document_results = poller.result()
    for result in document_results:
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            print("...Is an error with code '{}' and message '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else:
            print("Summary extracted: \n{}".format(
                " ".join([sentence.text for sentence in extract_summary_result.sentences]))
            )




if __name__ == "__main__":
    document = [
    "The extractive summarization feature uses natural language processing techniques to locate key sentences in an unstructured text document. "
    "These sentences collectively convey the main idea of the document. This feature is provided as an API for developers. " 
    "They can use it to build intelligent solutions based on the relevant information extracted to support various use cases. "
    "In the public preview, extractive summarization supports several languages. It is based on pretrained multilingual transformer models, part of our quest for holistic representations. "
    "It draws its strength from transfer learning across monolingual and harness the shared nature of languages to produce models of improved quality and efficiency. "
    ]

    document = [
        """GROSS:
A: Left simple mastectomy specimen. There is a well-defined but irregularly-shaped tumour mass in the
upper inner quadrant of the breast. The tumour, measuring 1.8cm in its greatest dimension, is located about
2.0cm below the skin. A piece of the muscles beneath the tumour is excised en bloc. There is no obvious
tumour invasion of the muscles. The tumour tissue is tan-white and firm to hard in consistency. There is a
large but poorly-outlined area of indurated retroareolar breast tissue. Patchy yellowish specks are found in
the tissue.
Blocks 1-3 : Representative sections of the breast tumour with deep surgical margin (muscles).
Block 4 : Representative section of the nipple.
Block 5 : Representative sections of the retroareolar breast tissue.
B: Left axillary lymph node dissection specimen. A few hard nodes are identified in the fat, the largest of
which measures 1.0cm. The nodes are submitted in 4 blocks.
C: Specimen consists of a lymph node, 0.7cm, covered by fat labelled lateral node. Bissected and submitted
entirely in one block.
HISTOLOGY:
A: Sections of the tumour show infiltration in the fibrous stroma by irregularly-shaped clusters of cells
arranged in sheets. Duct formation is scanty (<10%). Nuclear atypia of the tumour cells is severe. The
nuclei are large, vesicular and markedly pleomorphic. Nucleoli are prominent. Cytoplasm is moderately
abundant. Mitotic count is >20 per 10hpf. Necrosis is noted in some clusters of tumour cells. Foci of high-
grade DCIS are seen at the periphery of the tumour. Perineural and lymphovasular tumour cell invasion is
observed. No evidence of invasion of the muscles at the deep surgical margin. Sections of the indurated
retroareolar breast tissue show extensive and widespread foci of high-grade DCIS (comedo-type). An area
of invasive carcinoma, about 1.0cm in its greatest dimension, is identified among the DCIS. The histology
of the invasive malignancy is similar to the main tumour described above. No Paget's disease of nipple.
Breast Cancer Profile
Estrogen receptor: Negative expression.
Progesterone receptor: Negative expression.
c-erbB-2: Positive expression (70%; 2+ - 3+; IHC).
Ki67 index: 60%.
B: Sections show two of 20 lymph nodes examined are infiltrated by tumour cells. Focal perinodal invasion
is observed.
C: Sections of the lymph node do not show metastatic malignancy.
INTERPRETATION:
A, B: Left simple mastectomy specimen and left axillary lymph node dissection specimen:
"""
    ]

    extractive_summarization(client, document)
