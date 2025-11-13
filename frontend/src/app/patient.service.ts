import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { patient } from 'src/classes/patient';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class PatientService {
  private patientsUrl = 'http://18.118.170.215:8000/search/?query='
  
  constructor(private http: HttpClient) { }

  getPatients(input: string): Observable<any> {
    return this.http.get<patient[]>(this.patientsUrl + input)
  }

  private log(message: string) {
    console.log(`${message}`);
  }
}
