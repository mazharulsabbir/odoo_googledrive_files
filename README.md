## Upload Files to Google Drive

To create a service account on Google Cloud Console and enable Drive API, follow these steps:

1. Go to the Google Cloud Console (https://console.cloud.google.com/) and select the project for which you want to create a service account.

2. Click on the "Navigation Menu" button (☰) in the top-left corner of the console and select "IAM & admin" > "Service accounts".

3. Click on the "Create Service Account" button.

4. Enter a name and description for the service account and click "Create".

5. In the "Role" section, select the appropriate roles for the service account. If you want to enable the Drive API, you can select the "Project" > "Editor" role or create a custom role that includes the "Drive API" permissions.

6. Click "Continue" and then "Done" to create the service account.

7. Once the service account is created, click on the three dots next to the service account and select "Create Key".

8. Select the key type as JSON and click "Create". This will download a JSON file containing the private key that you will need to authenticate your application.

9. To enable the Drive API, go to the Google Cloud Console (https://console.cloud.google.com/), click on the "Navigation Menu" button (☰) in the top-left corner of the console and select "APIs & Services" > "Dashboard".

10. Click on the "Enable APIs and Services" button and search for "Google Drive API". Select the API and click "Enable".

11. You can now use the service account and the JSON file to authenticate your application and make requests to the Drive API.
