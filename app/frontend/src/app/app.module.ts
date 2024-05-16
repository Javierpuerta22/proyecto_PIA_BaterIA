import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { PushDataComponent } from './components/push-data/push-data.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatTabsModule } from '@angular/material/tabs';
import { MultiChartCardComponent } from './components/multi-chart-card/multi-chart-card.component';
import { IgxTabsModule } from 'igniteui-angular';
import { MainService } from './services/main.service';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { BsModalService, ModalModule } from 'ngx-bootstrap/modal';


//I keep the new line
@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    PushDataComponent,
    DashboardComponent,
    MultiChartCardComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatTooltipModule,
    MatTabsModule,
    IgxTabsModule,
    HttpClientModule,
    ReactiveFormsModule,
    ModalModule
  ],
  providers: [
    MainService, BsModalService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
