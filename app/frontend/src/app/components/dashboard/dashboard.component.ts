import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {

  pilas: any = [3, 1, 2];
  tabs = ['First', 'Second', 'Third'];
}
