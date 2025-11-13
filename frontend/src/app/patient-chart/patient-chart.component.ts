import { Component, OnInit, ɵɵsyntheticHostProperty } from '@angular/core';
import { patient } from 'src/classes/patient';

@Component({
  selector: 'app-patient-chart',
  templateUrl: './patient-chart.component.html',
  styleUrls: ['./patient-chart.component.css']
})
export class PatientChartComponent implements OnInit {
  patient: patient = new patient();

  constructor() { }

  ngOnInit(): void {
    this.patient = history.state.data;
  }

}
