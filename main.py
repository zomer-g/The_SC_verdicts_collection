import requests
import json
from csv import DictWriter


# Based on the Json file, receive verdicts data
def case_Verdicts(year, case_number):
    url = "https://supremedecisions.court.gov.il/Home/SearchVerdicts"
    # the Json file as it appears on the website of the Supreme Court
    j_file = {"document": {"Year": year, "Counsel": [
        {"Text": "", "textOperator": 2, "option": "2", "Inverted": False, "Synonym": False, "NearDistance": 3,
         "MatchOrder": False}], "CaseNum": 1213, "Technical": None, "fromPages": None, "toPages": None, "dateType": 1,
                           "PublishFrom": None, "PublishTo": None, "publishDate": None, "translationDateType": None,
                           "translationPublishFrom": None, "translationPublishTo": None, "translationPublishDate": 8,
                           "SearchText": [
                               {"Text": "", "textOperator": 1, "option": "2", "Inverted": False, "Synonym": False,
                                "NearDistance": 3, "MatchOrder": False}], "Judges": None, "Parties": [
            {"Text": "", "textOperator": 2, "option": "2", "Inverted": False, "Synonym": False, "NearDistance": 3,
             "MatchOrder": False}], "Mador": None, "CodeMador": [], "TypeCourts": None, "TypeCourts1": None,
                           "TerrestrialCourts": None, "LastInyan": None, "LastCourtsYear": None,
                           "LastCourtsMonth": None, "LastCourtCaseNum": None, "Old": False, "JudgesOperator": 2,
                           "Judgment": None, "Type": None, "CodeTypes": [], "CodeJudges": [], "Inyan": None,
                           "CodeInyan": [],
                           "AllSubjects": [{"Subject": None, "SubSubject": None, "SubSubSubject": None}],
                           "CodeSub2": [], "Category1": None, "Category2": None, "Category3": None, "CodeCategory3": [],
                           "translationPublishPeriod": None, "Subjects": None, "SubSubjects": None,
                           "SubSubSubjects": None}, "lan": 1}
    str_results = requests.post(url, json=j_file)
    dict_results = json.loads(str_results.text)
    result = {'year': year, 'case': case_number, 'Verdicts': dict_results}
    return (result)


# add each dict to new csv row
def add_to_csv(field_names, dict, csv_name):
    with open(csv_name, 'a', encoding='utf-8', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        dictwriter_object.writerow(dict)
        f_object.close()


# Defining fields for a CSV file
field_names = ['year', 'case', 'Verdicts']
csv_name = 'Verdicts.csv'

# Run year and case number loops and write results to CSV
for y in range(2020, 2023):
    fails = 0
    print(f'Start collect year {y}')
    for c in range(1, 10000):
        # Check whether there is a relevant case
        if case_Verdicts(y, c)['Verdicts']['data']:
            fails = 0
            # If the case exists, writing it to CSV
            add_to_csv(field_names, case_Verdicts(y, c), csv_name)
            print('case', case_Verdicts(y, c)['case'], '/', case_Verdicts(y, c)['year'], 'add to CSV')
        # Count number of continuous fails
        else:
            fails += 1
        # if got more than X continuous fails, stop for this year
        if fails == 10:
            print(f'Finish collect from year {y}')
            break
        print(f'{fails} number of continuous fails')
