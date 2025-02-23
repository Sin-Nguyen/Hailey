list_job = [
  "api-e2e-qa-az",
  "api-org-prepare-test-qa-az",
  "api-org-prepare-test-qa-dlp-az",
  "api-org-prepare-test-qa-mobile-az",
  "api-org-prepare-test-qa-web-az",
  "audit-exports-automation-testing-qa-az",
  "bulk-import-endpoint-mcp-non-sso-qa-az",
  "bulk-import-endpoint-mcp-non-sso-qa-azure",
  "codeceptjs",
  "imessage-native-qa-az",
  "imessage-native-selfonboard-job0-qa-az",
  "imessage-native-selfonboard-job1-qa-az",
  "imessage-native-selfonboard-job3-qa-az",
  "imessage-native-selfonboard-job5-qa-az",
  "imessage-native-selfonboard-maid-job2-qa-az",
  "imessage-native-selfonboard-maid-job4-qa-az",
  "imessage-native-selfonboard-maid-job6-qa-az",
  "lw-android-miniapp-qa-az",
  "lw-android-qa",
  "lw-ios-qa",
  "msteams-miniapp-qa-az",
  "msteams-qa-az",
  "msteams-wag-qa-az",
  "org-admin-qa-az",
  "sms-governed-qa-az",
  "web-am-qa-az",
  "wechatminiapp-1vs1-qa-az",
  "wechatminiapp-dlp-qa-az",
  "wechatminiapp-group-qa-az",
  "wechatminiapp-notifications-qa-az",
  "whatsapp-governed-cloud-web-qa-az",
  "whatsapp-governed-dedicated-cloud-qa-az",
  "whatsapp-native-qa-az1",
  "whatsapp-native-qa-az2",
]

ignore_words = [
 "show", "display", "list", "get", "give", "provide", "me", "the", "results", "for", "job", "jobs", "test", "tests", "testcase",
]

newest_words = [
 "latest", "newest", "recent", "last"
]

failed_words = [
 "failed", "failing", "broken", "error", "issue"
]

passed_words = [
 "successful", "passed", "passing", "good", "ok"
]

interupt_words = [
  "interrupt", "stop", "cancel", "abort", "crashed", "interrupted", "not completed", "not finished", "not done"
]

status_words = [
  "status", "progress", "result"
]

def query_prompt(context, query):
  optimized_prompt = f"""
        you are an professional senior QA engineer, called is Hailey who analyzing test automation data running at the night yesterday
        You should show detail of detailed test case data and give a summary report based on the data
        Use the following data for awnser the question:
        - number is testcases count
        - duration is the time taken for the test case
        - start time is the time the test case started.
        - status is the result of the test case.
        - If Failed, you should debate the QA team to understand the root cause and fix it. 
        - If Passed, you should celebrate the success with the QA team.
        - If the time is too long, you should give feedback to the QA team to optimize the test case.
        - If the test case is interrupted, you should ask the QA team to re-run the test case.
        - Template summary of job is : 
            Let's dive deeper into the failure details:
                - Job Name: job_name
                - Status: status (if FAILED => Ouch! That's not good / if PASSED => Great job!)
                - Number of Test Cases: number (give some feedback to the QA team)
                - Duration: duration seconds (give some feedback to the QA team)
                - Start Time: start_time (give some feedback to the QA team)

        Use the following test data to answer the question:
        {context}

        Question: {query}
        Answer:
        """
  return optimized_prompt     

  