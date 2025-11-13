import pandas as pd
import random
import os
import json


#########################################################
# Read in chart data from the various sources
# 
#########################################################

#try:
#    pkl_charts = pd.read_table(r'PatientCorePopulatedTable.txt', delimiter = "\t")                       #Import chart components.  1.Demograpic data  2.Diagnoses  3.Labs
#    pkl_diagnoses = pd.read_table(r'AdmissionsDiagnosesCorePopulatedTable.txt', delimiter = "\t")
#    pkl_labs = pd.read_table(r'LabsCorePopulatedTable.txt', delimiter = "\t")
#except FileNotFoundError:
#    print("Cannot find file")

#pkl_charts.to_pickle("charts.pkl")
#pkl_diagnoses.to_pickle("diagnoses.pkl")
#pkl_labs.to_pickle("labs.pkl")

def get_patinet_cxrays():
    num_xrays_to_get = random.randrange(1,4)
    total_xrays = len(cxray) - 1
    cxrays = []
    for n in range (num_xrays_to_get):
        index_to_get = random.randrange(1, total_xrays)
        cxrays.append(cxray.iloc[index_to_get,:])
    return cxrays

def get_patient_notes():
    doctors = ['Dr. Howard', 'Dr. Fine', 'Dr. Larry', 'Dr. Moe', 'Dr. Curly']
    dir = './CleanTranscripts'
    filename = random.choice(os.listdir(dir))
    num_notes_to_get = random.randrange(1,4)
    notes = []
    for n in range (num_notes_to_get):
        note = []
        filename = random.choice(os.listdir(dir))
        path_file = os.path.join(dir,filename)
        with open(path_file) as f:
            note_text = f.readlines()
        doctor = random.choice(doctors)
        note.append(doctor)
        note.append(note_text)
        notes.append(note)  
    return notes

def get_CT_JSON_file():
    dir = './Scans'
    filename = 'u.json'
    path_file = os.path.join(dir,filename)
    f=open(path_file)
    data = json.load(f)
    return data

def get_patient_CT_scans(data):
    num_CT_scans_to_get = random.randrange(1,4)
    scans = []
    for n in range (num_CT_scans_to_get):
        scans.append(random.choice(data['list'])['image'])
    return scans


try:
    charts = pd.read_table(r'PatientCorePopulatedTable.txt', delimiter = "\t")                       #Import chart components.  1.Demograpic data  2.Diagnoses  3.Labs
    diagnoses = pd.read_table(r'AdmissionsDiagnosesCorePopulatedTable.txt', delimiter = "\t")
    labs = pd.read_table(r'LabsCorePopulatedTable.txt', delimiter = "\t")
    cxray = pd.read_table(r'indiana_reports.csv', delimiter = ',')
except FileNotFoundError:
    print("Cannot find file")

labs['LabRecord'] = labs['LabName'] + ' ' + labs['LabValue'].astype(str) + ' ' + labs['LabUnits'] + ' ' + labs['LabDateTime']
labs = labs.drop(columns = ['AdmissionID', 'LabName', 'LabValue', 'LabUnits', 'LabDateTime'])                       #Remove unneeded columns from labs dataframe, we dont care about what admission the lab was done during
lab_group = labs.groupby('PatientID')['LabRecord'].apply(list).reset_index(name = 'Labs')                           #Each patient's labs are now in a list held in column 'Labs'
charts = pd.merge(charts, lab_group, on = 'PatientID')

chest_xrays_list = []
for counter in range (1, len(charts)+1):
    chest_xrays_list.append(get_patinet_cxrays())
charts['ChestXrays'] = chest_xrays_list

notes_list = []
for counter in range (1, len(charts)+1):
    notes_list.append(get_patient_notes())
charts['Notes'] = notes_list


CT_JSON_file_data = get_CT_JSON_file()
CT_scan_list = []
for counter in range (1, len(charts)+1):
    CT_scan_list.append(get_patient_CT_scans(CT_JSON_file_data))
charts['CTScans'] = CT_scan_list

charts.to_csv('charts.csv')