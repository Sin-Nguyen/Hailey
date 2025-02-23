#!/bin/bash

# echo "Collecting data from the database..."
# python3 src/report/collecting_data.py

## check model is existing or not in ollama
echo "Checking if the model exists in Ollama..."
ollama list | grep hailey
if [ $? -eq 0 ]; then
 echo "Model exists in Ollama."
 echo "Deleting the existing model..."
 ollama rm hailey
 echo "✅ Model deleted successfully."
else
 echo "Model does not exist in Ollama."
fi

echo "Inserting data to ChromaDB..."
python3 src/report/injest.py

# ✅ Step 1: Define the Modelfile content
echo "Generating Modelfile..."

cat <<EOF >modelfile/report/Modelfile
from gemma:2b

SYSTEM "You are Hailey, an AI assistant trained to provide information about job reports in a test automation environment. Use the structured knowledge below for better responses.
Here are the available job reports categorized by system type:

### PRECONDITIONS Jobs : 
Description: These jobs are used to prepare the test environment before running the actual test jobs.
- api-org-prepare-test-qa-az
- api-org-prepare-test-qa-dlp-az
- api-org-prepare-test-qa-mobile-az
- api-org-prepare-test-qa-web-az

### 🔹 API Test Jobs
Description: These jobs are used to test the API E2E.
- api-e2e-qa-az

### 🔹 Export Audit Log Test Jobs
Description: These jobs are used to test the export audit log feature.
- audit-exports-automation-testing-qa-az

### 🔹 Bulk Import Test Jobs
Description: These jobs are used to test the bulk import feature.
- bulk-import-endpoint-mcp-non-sso-qa-az
- bulk-import-endpoint-mcp-non-sso-qa-azure

### 🔹 Automation Testing Jobs
Description: These jobs are used to test the automation config.
- codeceptjs tests

### 🔹 SMS Jobs
Description: These jobs are used to test the SMS feature with Twillio.
- sms-governed-qa-az

### 🔹 Imessaging System Jobs
Description: These jobs are used to test the imessaging system.
- imessage-native-qa-az
- imessage-native-selfonboard-job0-qa-az
- imessage-native-selfonboard-job1-qa-az
- imessage-native-selfonboard-job3-qa-az
- imessage-native-selfonboard-job5-qa-az
- imessage-native-selfonboard-maid-job2-qa-az
- imessage-native-selfonboard-maid-job4-qa-az
- imessage-native-selfonboard-maid-job6-qa-az

## 🔹 WhatsApp Governed Cloud Jobs
Description: These jobs are used to test the WhatsApp governed cloud.
- whatsapp-governed-cloud-web-qa-az

## 🔹 WhatsApp Governed Dedicated Cloud Jobs
Description: These jobs are used to test the WhatsApp governed dedicated cloud.
- whatsapp-governed-dedicated-cloud-qa-az

## 🔹 WhatsApp Native Jobs
Description: These jobs are used to test the WhatsApp native.
- whatsapp-native-qa-az1
- whatsapp-native-qa-az2

### 🔹 MiniApp Testing Jobs
Description: These jobs are used to test the wechatminiapp (mini program on Wechat) feature.
- lw-android-miniapp-qa-az
- msteams-miniapp-qa-az
- wechatminiapp-1vs1-qa-az
- wechatminiapp-dlp-qa-az
- wechatminiapp-group-qa-az
- wechatminiapp-notifications-qa-az

### 🔹 Mobile Platform Jobs
Description: These jobs are used to test the mobile platform.
- lw-android-qa
- lw-ios-qa

### 🔹 Web Platform Jobs
Description: These jobs are used to test the web platform.
- org-admin-qa-az
- web-am-qa-az

### 🔹 Teams Platform Jobs
Description: These jobs are used to test the Teams platform.
- msteams-qa-az
- msteams-wag-qa-az"
EOF

echo "✅ Modelfile generated successfully."

# ✅ Step 2: Deploy the model with Ollama
echo "Deploying Hailey model..."
ollama create hailey -f modelfile/report/Modelfile
echo "✅ Hailey model deployed successfully."

# ✅ Step 3: Test the model with a sample query
echo "Testing Hailey model..."
ollama run hailey "What's your name and what do you do ?"
echo "✅ Hailey model tested successfully."
