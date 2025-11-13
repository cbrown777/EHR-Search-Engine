import pickle
import pandas as pd
import random
import os
import json

##############################################################################################################
#  This program assembles our main data set (chart.csv or chart2.csv) from various data sources off of the web
#  I started with the data from the 10,000 patients database created by Uri Kartoun, PhD.  This can be found at
#  https://figshare.com/articles/dataset/A_10_000-patient_database/7040060.  This data served as the framework
#  to which I added additional data.  Names for the patients were created using the website 
#  http://api.namefake.com and stored in a pkl file.  Ids were randomly created numbers also stored in a pkl.
#  Chest x-rays were obtained from the Indiana University collection 
#  https://www.kaggle.com/datasets/raddar/chest-xrays-indiana-university?select=indiana_reports.csv
#  Scans were scraped from the NIH open image dataset https://openi.nlm.nih.gov/services#searchAPIUsingGET
##############################################################################################################


## This function takes the chest Xray dataframe and randomly selects a random number of XRays to add to each chart
## Returs a list of chest x-rays 
def get_patinet_cxrays(cxray):                                                      
    num_xrays_to_get = random.randrange(2,5)                                        # How many cxrays to return
    total_xrays = len(cxray) - 1                                                    # How many cxrays are there in the pandas dataframe
    cxrays = []                                                                     # Initialize list of chest x-rays to return
    
    for n in range (num_xrays_to_get):                                              # Loop through number of cxrays to get
        index_to_get = random.randrange(0, total_xrays)                             # Pick a random cxray and get it
        
        cxr = (cxray.iloc[index_to_get,:])
        cxr_findings = cxr['findings']                                              # We just want the findings column
        
        if type(cxr_findings) == str:                                               # Append it if it is something other than 'nan'
            cxrays.append(cxr_findings)
    
    return cxrays

## Notes are separate documents stored in the CleanTranscripts directory.
## This function selects a random number of these transcripts and adds
## a random doctor name as the author.  This function returns a list of doctor notes
## a doctor note is a list containing the doctor's not and the text of the note 
def get_patient_notes():
    doctors = ['Dr. Howard', 'Dr. Fine', 'Dr. Larry', 'Dr. Moe', 'Dr. Curly']       # Potential doctors to write notes
    dir = './CleanTranscripts'                                                      # Directory containing transcripts
    num_notes_to_get = random.randrange(1,4)                                        # How many notes to return
    notes = []                                                                      # Function will return num_notes_to_get notes

    for n in range (num_notes_to_get):                                              # Loop through number of transcripts to make into notes
        note = []
        
        filename = random.choice(os.listdir(dir))                                   # Randomly select a trascript
        path_file = os.path.join(dir,filename)                                      # Create the whole filename
        
        with open(path_file) as f:                                                  # Read in file
            note_text = f.readlines()
        [i.strip() for i in note_text]                                              # Strip spaces, etc
       
        note_text = [i for i in note_text if i != '\n']                             # Get rid of all \n
        note_text = [i.replace('\n', '') for i in note_text]
        doctor = random.choice(doctors)                                             # Find random doctor to be 'Author' of note
        
        note.append(doctor)                                                         # Add doctor and text        
        note.append(note_text)                                                      
        notes.append(note)                                                          # Add note to list of notes
        
    return notes

## Open the JSON file to get the appropriate scan data
def get_JSON_file(file):
    #dir = './Scans'
    #filename = file + '.json'
    #path_file = os.path.join(dir,filename)
    f=open('./Scans/' + file + '.json')
    print(f)
    data = json.load(f)
    return data

## Parse the scan data 
def get_scan_JSON(data, n):
    num_scans_to_get = random.randrange(1, n)
    scans =[]
    for i in range (num_scans_to_get):
        caption = (random.choice(data['list'])['image']['caption'])                 #Get rid of any scans lacking a report
        if (caption != 'Not Available.') & (caption != 'Replace this - DESCRIPTION OF THE IMAGE OR FINDINGS.'):
            scans.append(caption)
    return scans





try:
    charts = pd.read_table(r'./Chartdata/PatientCorePopulatedTable.txt', delimiter = "\t")                       # Import chart components.  
    diagnoses = pd.read_table(r'./Chartdata/AdmissionsDiagnosesCorePopulatedTable.txt', delimiter = "\t")
    labs = pd.read_table(r'./Chartdata/LabsCorePopulatedTable.txt', delimiter = "\t")
    cxray_data = pd.read_table(r'./Cxrays/indiana_reports.csv', delimiter = ',')
except FileNotFoundError:
    print("Cannot find file")

# Merge the labs into the patient chart dataframe

labs['LabRecord'] = labs['LabName'] + ' ' + labs['LabValue'].astype(str) + ' ' + labs['LabUnits'] + ' ' + labs['LabDateTime']
labs = labs.drop(columns = ['AdmissionID', 'LabName', 'LabValue', 'LabUnits', 'LabDateTime'])                       # Remove unneeded columns from labs dataframe, we dont care about what admission the lab was done during
lab_group = labs.groupby('PatientID')['LabRecord'].apply(list).reset_index(name = 'Labs')                           # Each patient's labs are now in a list held in column 'Labs'
charts = pd.merge(charts, lab_group, on = 'PatientID')                                                              # Merge based on patient ID

# Once we have merged the labs and patient chart based on PatientID, we can remove the long patient ID from the 10,000 patients dataset
charts = charts.drop(columns=['PatientID'])

# add our synthetic names
with open('./Names/names_list.pkl', 'rb') as f:
    names_list= pickle.load(f)
charts['Name'] = names_list

# add our shortened IDs
with open('./Ids/ids_list.pkl', 'rb') as f:
    ids_list= pickle.load(f)
charts['Id'] = ids_list

# add chest x-rays
chest_xrays_list = []
cxray_data = cxray_data.drop(columns = ['uid', 'MeSH'])
for counter in range (1, len(charts)+1):
    chest_xrays_list.append(get_patinet_cxrays(cxray_data))
charts['ChestXrays'] = chest_xrays_list

# add notes
notes_list = []
for counter in range (1, len(charts)+1):
    notes_list.append(get_patient_notes())
charts['Notes'] = notes_list

# add scans
scan_types = ['MRIs', 'CTs', 'Ultrasounds']
for scan_type in scan_types:
    data = get_JSON_file(scan_type)
    scan_list = []
    for counter in range (1, len(charts)+1):
        scan_list.append(get_scan_JSON(data, 5))
    charts[scan_type] = scan_list

# rename the columns to shorter names
charts.rename(columns = {'PatientGender':'Gender'}, inplace = True)
charts.rename(columns = {'PatientRace':'Race'}, inplace = True)
charts.rename(columns = {'PatientMaritalStatus':'MaritalStatus'}, inplace = True)
charts.rename(columns = {'PatientLanguage':'Language'}, inplace = True)
charts.rename(columns = {'PatientPopulationPercentageBelowPoverty':'PovertyRate'}, inplace = True)

cols = ['Id', 'Name', 'Gender', 'Race', 'MaritalStatus', 'Language', 'PovertyRate', 'ChestXrays', 'Notes', 'CTs', 'Ultrasounds', 'MRIs']

# get just the columns we want
charts = charts[cols]

#export our dataset!!!
charts.to_csv('charts2.csv')