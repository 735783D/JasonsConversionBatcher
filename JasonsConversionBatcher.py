# Also works in local CLI using the python3 suffix after allowing for execution(chmod +x)
# Does lose formatting on vertical screen if you do this, which will cause errors.
import pandas as pd
import csv
import os

beta = False
english_count = 0
chinese_count = 0
german_count = 0
turkish_count = 0
spanish_count = 0
french_count = 0
italian_count = 0
japanese_count = 0
portuguese_count = 0
swedish_count = 0
dutch_count = 0
polish_count = 0
lang_minute_count = 0
lang_second_count = 0
dynamic_injection_count = 0
dynamic_injections = 0
dynamic_injection_seconds_count = 0

# Duplicate CID Mover

# Select the input Excel sheet from your file system
# Load the Excel file into a DataFrame

# This is where you will specify the file Excel file you want to batch (Use absolute path for best results)
    # Example:
        # excel_file = 'PATH_TO_EXCEL_BOOK.xlsx'
# TEST INPUTS
    # Beta
#excel_file = 'PATH_TO_EXCEL_BOOK.xlsx'
    # Prod
#excel_file = 'PATH_TO_EXCEL_BOOK.xlsx'

# FULL SCALE
excel_file = 'PATH_TO_EXCEL_BOOK.xlsx'

# This should always be "Sheet1" unless the POC changed the name.
# It will let you know if it is incorrect with an error though.
sheet_name = 'Sheet1'  # Replace with the sheet name you're working with
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Specify the column you want to check for duplicates
column_to_check = 'Encrypted_CID'  # Replace with the actual column name

# Finds and extracts the duplicated rows
duplicates = df[df.duplicated(subset=column_to_check, keep='first')]

# Removes the duplicated rows from the original DataFrame
df.drop(df[df.duplicated(subset=column_to_check, keep='first')].index, inplace=True)

# Appends the duplicated rows to the end of the DataFrame
df = df._append(duplicates, ignore_index=True)

# Saves the updated DataFrame back to the original Excel file
df.to_excel(excel_file, sheet_name=sheet_name, index=False)

if not duplicates.empty:
    print("Duplicated values moved to the end of the sheet and saved to the same file.")

# If no other path is chosen for temp.csv file will be created locally
split_source_file = 'temp.csv'

# ===============================================================================

# Reader/converter

# Start of script that parses the csv and pulls out the specific columns
df = pd.read_excel(excel_file)

# Removes front and ending blank spaces from rows
df = df.replace({"^\s*|\s*$": ""}, regex=True)

# This converts the Excel sheet to a .csv file in a dataframe using Pandas
# df2.loc[:, ['Encrypted_CID', 'case_id', 'region_id', 'home_marketplace_id', 'preferred_language',
#            'Qualtrics_Link']].to_csv(split_source_file, index=False)
df.loc[:, ['Encrypted_CID', 'region_id', 'home_marketplace_id', 'preferred_language', 'Qualtrics_Link']].to_csv(split_source_file, index=False)

with open(split_source_file, "r") as file:
    with open("temp.txt", "w") as file2:

        # Reads the csv file for the information that will be used to run the item converter over
        csv_input = csv.DictReader(file)

        # This for loop iterates over the specific columns in the .csv file
        for row in csv_input:
            dev_id = row['Encrypted_CID']
            region = row['region_id']
            home_market = row['home_marketplace_id']
            lang = row['preferred_language']
            # This is checking the language to determine time savings and increments both time and instance counters.
            if lang == 'English':
                lang_second_count = lang_second_count + 90
            else:
                lang_second_count = lang_second_count + 120
            if lang == 'English':
                english_count = english_count + 1
            elif lang == 'Spanish':
                spanish_count = spanish_count + 1
            elif lang == 'German':
                german_count = german_count + 1
            elif lang == 'Turkish':
                turkish_count = turkish_count + 1
            elif lang == 'Japanese':
                japanese_count = japanese_count + 1
            elif lang == 'Chinese':
                chinese_count = chinese_count + 1
            elif lang == 'Portuguese':
                portuguese_count = portuguese_count + 1
            elif lang == 'French':
                french_count = french_count + 1
            elif lang == 'Italian':
                 italian_count = italian_count + 1
            # elif lang == 'Polish':
            #     polish_count = polish_count + 1
            # elif lang == 'Swedish':
            #     swedish_count = swedish_count + 1
            # elif lang == 'Dutch':
            #     dutch_count = dutch_count + 1

            # Comment section if no Qualtrics link is given, or just the column header to your
            # Excel sheet if it seems easier.
            # The first if/else is because python cannot concat NULL values
            #-----------------------------------------------------------#
            # formLink = row['Qualtrics_Link']
            # if formLink == "":
            #     formLink = ""
            # else:
            #     formLink = row['Qualtrics_Link']
            #
            # # This is checking for dynamic injections and increments an instance and time counter.
            # if formLink:
            #     dynamic_injections = dynamic_injections + 1
            #     dynamic_injection_seconds_count = dynamic_injection_seconds_count + 30
            #----------------------------------------------------------#

        # Pay very close attention to the blurb and subject you are using

            #  Example:
            # blurbSubject = "MIGRATION_SUBJECT"
            # blurbBody = "MIGRATION"

            blurbSubject = 'MIGRATION_V_1_SUBJECE'
            blurbBody = 'MIGRATION_V_1'

            # blurbSubject = 'MANUAL_CONTACT'
            # blurbBody = 'MANUAL_CONTACT_v_1'

            blurbSubject = blurbSubject.strip()
            blurbBody = blurbBody.strip()


        # Queue names are extremely important for routing the blurbs.
            if excel_file == "/Users/whitbyja/PycharmProjects/JasonsBatchScript/Excels/0-CCAPR-BETA-0.xlsx":
                beta = True
                queue = "beta-general@there.com"
                sender = "beta-general@there.com"
            else:
                if region == '1':
                    queue = "thing_no-reply@there.com"
                    sender = "thing_no-reply@there.com"
                elif region == '2':
                    queue = "thing_no-reply@there.co.uk"
                    sender = "thing_no-reply@there.co.uk"
                else:
                    queue = "thing_no-reply@there.co.jp"
                    sender = "thing_no-reply@there.com"


        # an external change in status that will typically prompt the workflow to go down a different path than if it
        # timed out. 
            caseStatus = "Pending Merchant Action"  # Setting to Pending Merchant Action because the developer is expected to make an api call if they want to be excluded

        # The amount of time that before the timeBoundBlurbNotifications step function with wait to move onto the next step:

            timeoutSeconds = 5

        # This section is injected into the main record in a later step.
            # The timeboundInput attributes are specific to the timeBound BlurbNotifications step in your stip function.

            timeBoundInput = ""

        # The reasonString is the "address" part of the routing mechanism in the queue.

            if beta:
                reasonString = "Audit - Checking Customer Library"
            else:
                reasonString = "Migration - Newer Library Update"

        # The fromName describes who the email is from. This is typically specified in the campaign SIM.
            fromName = "WhoThisIsComingFrom@somewhere.com"
            formLink = ""
            formDetails = "{\\\"formLink\\\":\\\"" + formLink + "\\\"}"

            record = ("{\"entityIdentifier\":" + "\"" + dev_id + "-" + region + "\", " 
                      "\"actionKey\":" + "\"createCaseAndPostReply\", "
                      "\"region\":" + "\"" + region + "\", "
                      "\"eligibleActions\":[\"createCaseAndPostReply\"], "
                      "\"inputAttributes\": {\"developerId\":\"" + dev_id + "\", "  
                      "\"blurbSubject\":" + "\"" + blurbSubject + "\", "
                      "\"blurbName\":" + "\"" + blurbBody + "\", "                                                                            
                      "\"caseStatus\": " + "\"" + caseStatus + "\", "                                                  
                      "\"reasonString\": " + "\"" + reasonString + "\", "
                      "\"marketplaceIds\":" + "\"" + home_market + "\", "
                      "\"fromAddress\": " + "\"" + sender + "\", "
                      "\"fromName\":" + "\"" + fromName + "\", "
                      "\"formDetails\": " + "\"" + formDetails + "\", "
                      "\"queueName\":" + "\"" + queue + "\", "
                      "\"timeBoundInput\": " + "\"" + timeBoundInput + "\", "
                      "\"language\":" + "\"" + lang + "\"}, "
                      "\"ttl\":" + "1}")
            file2.write(record + "\n")

# ===============================================================================

# Batcher
input_file = "temp.txt"
max_lines_per_file = 300
output_file_prefix = "PATH_TO_OUTPUT_"

with open(input_file, "r") as infile:
    count = 0
    outfile = None
    for line in infile:
        if count % max_lines_per_file == 0:
            if outfile:
                outfile.close()
            outfile = open(output_file_prefix + str(count // max_lines_per_file + 1) + ".json", "w")
        outfile.write(line)
        count += 1
    if outfile:
        outfile.close()

# ===============================================================================

# Statistics Generation
print('Number of dynamic variables: ' + str(dynamic_injections))
total_second_count = lang_second_count + dynamic_injection_count
print('Total seconds: ' + str(total_second_count) + ' seconds')
total_hour_count = total_second_count/3600
print('Total hours saved: ' + str(total_hour_count) + ' hrs')
dynamic_injections = str(dynamic_injections)
total_hour_count = str(total_hour_count)
total_second_count = str(total_second_count)
total_id_count = chinese_count+english_count+french_count+german_count+italian_count+japanese_count+portuguese_count+spanish_count+turkish_count#+dutch_count+swedish_count+polish_count

stats_output_prefix = output_file_prefix + "statistics.txt"
with open(stats_output_prefix, 'w') as stats:
    stats.write('Blurb count by language:' + '\n' +
                '\tChinese: ' + str(chinese_count) + '\n' +
                '\tEnglish: ' + str(english_count) + '\n' +
                '\tFrench: ' + str(french_count) + '\n' +
                '\tGerman: ' + str(german_count) + '\n' +
                '\tItalian: ' + str(italian_count) + '\n' +
                '\tJapanese: ' + str(japanese_count) + '\n' +
                '\tPortuguese: ' + str(portuguese_count) + '\n' +
                '\tSpanish: ' + str(spanish_count) + '\n' +
                '\tTurkish: ' + str(turkish_count) + '\n' +
                # '\tSwedish: ' + str(swedish_count) + '\n' +
                # '\tPolish: ' + str(polish_count) + '\n' +
                # '\tDutch: ' + str(dutch_count) + '\n' +
                '\tTotal number of Ids in Batches: ' + str(total_id_count) + '\n' +
                'Number of dynamic variables: ' + dynamic_injections + '\n' +
                'Total seconds: ' + total_second_count + ' seconds' + '\n' +
                'Total hours saved: ' + total_hour_count + ' hrs')
