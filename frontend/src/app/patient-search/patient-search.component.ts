import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { patient } from 'src/classes/patient';
import { PatientService } from '../patient.service';

@Component({
  selector: 'app-patient-search',
  templateUrl: './patient-search.component.html',
  styleUrls: ['./patient-search.component.css']
})

export class PatientSearchComponent implements OnInit {
  title = 'Patient Charts';
  search = "";
  patients:patient[] = [];

  constructor(
    private router: Router, 
    private patientService: PatientService){
  }

  ngOnInit(): void {
  }

  searchUsers(){
    this.patientService.getPatients(this.search).subscribe(pats => {
      this.patients =[];
      if (pats.hits.length == 0){
        let pat = new patient();
        pat.id = '0000';
        pat.name = 'No Patients Found';
        pat.gender = 'N/A';
        pat.race = 'N/A';
        pat.maritalStatus = 'N/A';
        pat.language = 'N/A';
        pat.poverty = 'N/A';
        pat.chestxray = 'N/A';
        pat.notes = 'N/A';
        pat.ctScans = 'N/A';
        pat.ultrasounds = 'N/A';
        pat.mris = 'N/A';
        this.patients.push(pat)
      }
      for (let i = 0; i < pats.hits.length; i++){
        let pat = new patient();
        pat.id = pats.hits[i]._source.Id;
        pat.name = pats.hits[i]._source.Name.replaceAll('[', '').replaceAll(',', '').replaceAll(']', '').replaceAll(/'/g, '');
        pat.gender = pats.hits[i]._source.Gender;
        pat.race = pats.hits[i]._source.Race;
        pat.maritalStatus = pats.hits[i]._source.MaritalStatus;
        pat.language = pats.hits[i]._source.Language;
        pat.poverty = pats.hits[i]._source.PovertyRate;
        pat.chestxray = pats.hits[i]._source.ChestXrays.replaceAll('[', '').replaceAll(']', '').replaceAll(/'/g, '').replaceAll(',', '\n');
        pat.notes = pats.hits[i]._source.Notes.replaceAll('[', '').replaceAll(']', '').replaceAll(/'/g, '').replaceAll(/"/g, '').replaceAll(',', '').replaceAll('D:', '\nD:').replaceAll('P:', '\nP:');
        pat.ctScans = pats.hits[i]._source.CTs.replaceAll('[', '').replaceAll(']', '').replaceAll(/'/g, '').replaceAll(',', '\n');
        pat.ultrasounds = pats.hits[i]._source.Ultrasounds.replaceAll('[', '').replaceAll(']', '').replaceAll(/'/g, '').replaceAll(',', '\n');
        pat.mris = pats.hits[i]._source.MRIs.replaceAll('[', '').replaceAll(']', '').replaceAll(/'/g, '').replaceAll(',', '\n');
        this.patients.push(pat)
      }
    });
  }

  viewPatientDetails(pat: patient) {
    this.router.navigate(['/details'], {state: {data: pat}});
  }

  numSequence(n: number): Array<number> {
    if (n < 0){
      return Array(0);
    }
    return Array(n);
  }
}
