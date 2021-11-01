# Document Intelligence POC

## Set up

```cmd
conda create -n cognitive-services python=3.7
conda activate cognitive-services
pip install azure-ai-formrecognizer --pre
pip install pandas
```

## How to run

Specify the local files to process.

- Copy `target_files.txt.dist` to `target_files.txt`.
- Replace the file path in the file. It can be outside of the project folder. `dir /s /b /a:-D` (list all files under current directory) can be useful to create one.

Set the environment variables with your own values before running the sample:

- Copy `run_test.cmd.dist` to `run_test.cmd`.
- Replace endpoint and key from the file.
  - AZURE_FORM_RECOGNIZER_ENDPOINT - the endpoint to your Cognitive Services resource.
  - AZURE_FORM_RECOGNIZER_KEY - your Form Recognizer API key
- Run `run_test.cmd` in Command Prompt.

## Acknowledgement

Original scripts are from: [Azure-SDK-For-Python](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/formrecognizer/azure-ai-formrecognizer/samples). A copy is at [reference](./reference).
