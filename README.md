This is a python script that I wrote at work over a few weeks to try to automate a manual task in our mostly automated two-way communication emailing system with our customers. Originally, we had to take Excel files that were given to us by account managers with specific
information that would then be batched manually using copy/paste. We would then have a shell script run over the smaller manual batched files that would convert them to JSON formatted payloads that would then be uploaded to an AWS S3 bucket to be parsed and sent out.
The script I wrote used the original shell script rewritten in python and then added an automated batching function that would do this on its own so as to not have to do that tedious part anymore. I also added functionality to check for duplicated customer Ids that way 
there would not be an issue with a customer either receiving an email twice for the same thing. Or, in some workflows there was a deduplication logic that would error out if one was found and stop the upload.
I kept iterating over the script after I was told about the metric collection for time savings that we were supposed to be calcuating with our email campaigns. These automated campaigns were saving the time of the account managers from emailing the customers manually. 
So I put a calculation function into the script to keep track of all of the necessary information that would then be calculated at the end to get the time savings. This script took what used to be an all day thing into just a couple of hours. Not to mention, I really
loved building and iterating over it making it better each time.

To use this script, you need to have the very specific column names that it will be parsing on as the headers for your columns in your Excel sheet. 
This is specifically used for Excel, though you can tune it to work on just a basic CSV file. 
Once you have your column names matching, you just give it the absolute path of the file and run the script. 
It outputs the batched JSON formatted files to wherever you set the output path to. 
And that's it. Hope this saves someone some time like it did my team and myself.

This script requrires the following libraries to run:
- pandas
- openpyxl

These can be installed by running the following command in a terminal that has pip installed:
```
pip install pandas openpyxl
```
When the script is run successfully the output will look like the following:
```
{"entityIdentifier":"ASODNFO23RAWE-1", "actionKey":"createCaseAndPostReply", "region":"1", "eligibleActions":["createCaseAndPostReply"], "inputAttributes": {"developerId":"ASODNFO23RAWE", "blurbSubject":"MIGRATION_V_1_SUBJECT", "blurbName":"MIGRATION_V_1", "caseStatus": "Pending Merchant Action", "reasonString": "Migration - Newer Library Update", "marketplaceIds":"1", "fromAddress": "thing_no-reply@there.com", "fromName":"WhoThisIsComingFrom@somewhere.com", "formDetails": "{\"formLink\":\"\"}", "queueName":"thing_no-reply@there.com", "timeBoundInput": "", "language":"English"}, "ttl":1}
```

The statistics that are generated from the calculations is delivered in a .txt file. There is an example in the sidebar along with the fake data in an example Excel sheet.
