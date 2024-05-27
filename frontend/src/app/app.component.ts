import { Component } from '@angular/core';
import { MainService } from './services/main.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';

  constructor(private service:MainService, private router: Router){}

  is_logged(){
    return this.service.get_cookie('registered');
  }

  logout(){
    this.service.delete_cookie('registered');
    this.router.navigate(['/login']);
  }
}
