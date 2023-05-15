import pandas as pd
import csv
import json


perm = input("Did you check the Excel file for proper format (proper column names), \ncorrectness "
             "and consistency (i.e. no duplicate Ids near each other? y or n? ")
if perm == "y":
    print("Are you sure you checked it...? If you didn't it's gonna break stuff.")
    perm2 = input("Now I'll ask again, did you check the Excel sheet? y or n? ")
    print("Alright...proceed...I'm watching you though.")

    # Select the input Excel sheet
    input_Excel_file = "/Users/person/PycharmProjects/JasonsConversionBatcher/Campaign.xlsx"

    # Select the output csv file
    split_source_file = '/Users/person/PycharmProjects/JasonsConversionBatcher/temp.csv'

    # Start of script that parses the csv and pulls out the specific columns
    df = pd.read_excel(input_Excel_file)
    #print(df.head())
    #print(df.loc[:, ['Encrypted_Customer_Id', 'CaseID', 'RegionID', 'HomeMarketId', 'Pref_lang', 'Survey_Link']].head())
    df.loc[:, ['Encrypted_Customer_Id', 'CaseID', 'RegionID', 'HomeMarketId', 'Pref_lang', 'Survey_Link']].to_csv(split_source_file, index=False)#, header=False)

    file = open(split_source_file, "r")
    file2 = open("temp.json", "w")
    csv_input = csv.DictReader(file)
    # with open(split_source_file, "r") as f_input:
    #     csv_input = csv.DictReader(f_input)

    for row in csv_input:
        cust_id = row['Encrypted_Customer_Id']
        case = row['CaseID']
        region = row['RegionID']
        home_market = row['HomeMarketId']
        lang = row['Pref_lang']
        formLink = row['Survey_Link']
        # This if/else is because python cannot concat NULL values
        if formLink == "":
            formLink = ""
        else:
            formLink = row['Survey_Link']

        blurbSubject = 'BLURB_SUBJECT!'
        blurbBody = 'BLURB_BODY!'

        if region == '1':
            queue = "This is the queue name.com"
            sender = "This is the sender name.com"
        elif region == '2':
            queue = "This is the queue name.co.uk"
            sender = "This is the sender name.co.uk"
        else:
            queue = "This is the queue name.co.jp"
            sender = "This is the sender name.co.jp"

    # Equal to the echo $record statement in the shell
        formDetails = "{\\\"formLink\\\":\\\"" + formLink + "\\\"}"
        record = ("{\"entityIdentifier\":" + "\"" + cust_id + "-" + region + "\", " 
                  "\"actionKey\":" + "\"postReplyToCase\", "
                  "\"region\":" + "\"" + region + "\", "
                  "\"eligibleActions\":[\"postReplyToCase\"], "
                  "\"inputAttributes\": {\"developerId\":\"" + cust_id + "\", "                                                
                  "\"blurbSubject\":" + "\"" + blurbSubject + "\", "
                  "\"blurbName\":" + "\"" + blurbBody + "\", "
                  "\"caseId\":" + "\"" + case + "\", "
                  "\"caseStatus\": " + "\"Pending Customer Action\", "
                  "\"reasonString\": " + "\"This is the reason string!\", "
                  "\"marketplaceIds\":" + "\"" + home_market + "\", "
                  "\"fromAddress\": " + "\"somebody@somewhere.com\", "
                  "\"fromName\":" + "\"Who's this from?\", "
                  "\"formDetails\": " + "\"" + formDetails + "\", "
                  "\"queueName\":" + "\"" + queue + "\", "
                  "\"marketplaceIds\":" + "\"" + home_market + "\", "
                  "\"language\":" + "\"" + lang + "\"}, "
                  "\"ttl\":" + "1800}")
        file2.write(record + "\n")
    file2.close()
    file.close()


    #you need to add your path here
    with open('temp.json', 'r', encoding='utf-8') as f1:
        ll = [json.loads(line.strip()) for line in f1.readlines()]

        print("\nBatching completed!\n")
        #this is the total length size of the json file
        print("There were " + (str(len(ll)) + " lines in your temp file."))

        #in here 500 means we getting splits of 500 json objects
        #you can define your own size of split according to your need
        size_of_the_split = 500
        total = len(ll) // size_of_the_split

        #in here you will get the Number of splits
        print("Meaning you have " + (str(total+1) + " batches.\nHave a smooth campaign!\nWatch for errors!"))

        for i in range(total+1):
            json.dump(ll[i * size_of_the_split:(i + 1) * size_of_the_split], open(
                "/Users/person/PycharmProjects/JasonsConversionBatcher/campaign_" + str(i+1) + ".json", 'w',
                encoding='utf8'), ensure_ascii=False, indent=True)
else:
    print("Make sure that you check the Excel sheet for proper format (i.e. column names), correctness, consistency, and NO DUPLICATES NEAR EACH OTHER! ")

#==============================================
# This script only does csv files, not json
##############################
# Different script that does #
# the same thing only bigger #
# and with UUID capabilities #
##############################


# # import os
# # import pandas as pd
# # import uuid
# #
# #
# # class FileSettings(object):
# #     def __init__(self, file_name, row_size=100):
# #         self.file_name = file_name
# #         self.row_size = row_size
# #
# #
# # class FileSplitter(object):
# #
# #     def __init__(self, file_settings):
# #         self.file_settings = file_settings
# #
# #         if type(self.file_settings).__name__ != "FileSettings":
# #             raise Exception("Please pass correct instance ")
# #
# #         self.df = pd.read_csv(self.file_settings.file_name,
# #                               chunksize=self.file_settings.row_size, header=False)
# #
# #     def run(self, directory="/Users/whitbyja/PycharmProjects/JasonsBatchScript"):
# #
# #         try:
# #             os.makedirs(directory)
# #         except Exception as e:
# #             pass
# #
# #         counter = 0
# #
# #         while True:
# #             try:
# #                 file_name = "{}/{}_{}_row_{}_{}.csv".format(
# #                     directory, self.file_settings.file_name.split(".")[0], counter, self.file_settings.row_size,
# #                     uuid.uuid4().__str__()
# #                 )
# #                 df = next(self.df).to_csv(file_name)
# #                 counter = counter + 1
# #             except StopIteration:
# #                 break
# #             except Exception as e:
# #                 print("Error:", e)
# #                 break
# #
# #         return True
# #
# #
# # def main():
# #     helper = FileSplitter(FileSettings(
# #         file_name='out.csv',
# #         row_size=40
# #     ))
# #     helper.run()
# #
# #
# # main()