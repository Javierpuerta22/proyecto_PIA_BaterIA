import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { MainService } from '../services/main.service';

@Injectable({
  providedIn: 'root'
})
export class mainGuard implements CanActivate {

  constructor(private router: Router, private service:MainService) {}

  canActivate(): boolean {
    
    const token = this.service.get_cookie('registered');

    if (token) {
      return true;
    } else {
      // El token no existe, el usuario no está autenticado, redirigir a la página de inicio
      this.router.navigate(['/login']); // Cambia '/inicio' a la ruta de tu página de inicio
      return false;
    }
  }
}
