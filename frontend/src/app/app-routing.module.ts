import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PatientSearchComponent } from './patient-search/patient-search.component';
import { PatientChartComponent } from './patient-chart/patient-chart.component';

const routes: Routes = [
  { path: 'search', component: PatientSearchComponent },
  { path: 'details', component: PatientChartComponent },
  { path: '',   redirectTo: '/search', pathMatch: 'full' },
  { path: '**', component: PatientSearchComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
