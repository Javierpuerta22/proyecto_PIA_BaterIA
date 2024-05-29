import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { PushDataComponent } from './components/push-data/push-data.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { mainGuard } from './guard/main.guard';
import { HistorialComponent } from './components/historial/historial.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent, pathMatch: 'full' },
  { path: "home", component: PushDataComponent, pathMatch: 'full', canActivate: [mainGuard]},
  { path: "dashboard", component: DashboardComponent, pathMatch: 'full', canActivate: [mainGuard]},
  { path: "historial", component: HistorialComponent, pathMatch: 'full', canActivate: [mainGuard]},
  { path: '**', redirectTo: '/login', pathMatch: 'full'},
  { path: '', redirectTo: '/login', pathMatch: 'full' }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
