# Setting up Google Calendar API for IntrAgenda

This tutorial will guide you through the process of configuring Google Calendar API for your GitHub project with illustrative images.

## Step 1: Access the Google Console page

![Step 1](/.github/assets/1.png)

- Go to [the Google Console page](https://console.cloud.google.com/projectselector2/apis/credentials).
- Accept the terms of use if prompted and create a new project.

## Step 2: Create a project

![Step 2](/.github/assets/2.png)

- Set a name for your project, for example, "IntrAgenda", and create the project.

## Step 3: Access the OAuth Consent Screen page

![Step 3](/.github/assets/3.png)

- Next, go to the [OAuth consent screen](https://console.cloud.google.com/apis/credentials/consent).
- Choose the "External" option and click on "Create."

## Step 4: Configure the consent screen

![Step 4](/.github/assets/4.png)

- Enter the name "IntrAgenda."
- Select your email address below.
- At the bottom of the page, re-enter your Google email and save.

## Step 5: Continue the consent process

![Step 5](/.github/assets/5.png)

- Click on "Save and continue" for the next two pages.

## Step 6: Return to the dashboard

![Step 6](/.github/assets/6.png)

- Once on the Summary page, press "Return to dashboard."

## Step 7: Publish the application

![Step 7](/.github/assets/7.png)

- Click on "Publish the app" and confirm.

## Step 8: Enable Google Calendar API

![Step 8](/.github/assets/8.png)

- Go to [Google Calendar API](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com) and click on "Enable."

## Step 9: Create OAuth credentials

![Step 9](/.github/assets/9.png)

- Then, visit [Credentials](https://console.cloud.google.com/apis/credentials), create new credentials, and select 'OAuth client ID.'

## Step 10: Configure OAuth client ID

![Step 10](/.github/assets/10.png)

- Choose "Desktop App" with the name "IntrAgenda" and create.

## Step 11: Download the credentials.json file

![Step 11](/.github/assets/11.png)

- A popup will appear, allowing you to download the .json file.
- Rename the downloaded file to 'credentials.json' and place it at the root of your repo.

You have now successfully configured Google Calendar API for IntrAgenda.
