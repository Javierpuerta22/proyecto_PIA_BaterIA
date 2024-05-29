import { Component } from '@angular/core';

@Component({
  selector: 'app-navigator',
  templateUrl: './navigator.component.html',
  styleUrls: ['./navigator.component.css']
})
export class NavigatorComponent {


  nombres = ["Subir datos", "Dashboard", "Historial", "Cerrar sesión"]
  routes = ["home", "dashboard", "historial", "login"]
}
