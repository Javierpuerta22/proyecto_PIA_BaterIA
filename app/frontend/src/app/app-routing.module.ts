import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { PushDataComponent } from './components/push-data/push-data.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent, pathMatch: 'full' },
  { path: "home", component: PushDataComponent, pathMatch: 'full'},
  { path: "dashboard", component: DashboardComponent, pathMatch: 'full'},
  { path: '**', redirectTo: '/login', pathMatch: 'full'},
  { path: '', redirectTo: '/login', pathMatch: 'full' }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
