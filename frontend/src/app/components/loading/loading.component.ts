import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpResponse,
} from '@angular/common/http';
import { finalize } from 'rxjs/operators';
import { LoadingService } from 'src/app/services/loading.service';

@Component({
  selector: 'app-loading',
  templateUrl: './loading.component.html',
  styleUrls: ['./loading.component.css']
})
export class LoadingComponent implements HttpInterceptor {
  constructor(public loadingService: LoadingService) {}
  intercept(request: HttpRequest<any>, next: HttpHandler) {
    this.loadingService.showLoading(); // Mostrar pantalla de carga
    document.body.style.overflow = 'hidden';

    return next.handle(request).pipe(
      finalize(() => {
        this.loadingService.hideLoading(); // Ocultar pantalla de carga
        document.body.style.overflow = 'auto';
      })
    );
  }
}
