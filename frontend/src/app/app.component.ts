import { Component } from '@angular/core';
import { MainService } from './services/main.service';
import { Router } from '@angular/router';

export const route_to_images: string = "static/content/images/"


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

  is_data(){
    return this.service.get_cookie('data');
  }



  logout(){
    this.service.delete_cookie('registered');
    this.router.navigate(['/login']);
  }
}
