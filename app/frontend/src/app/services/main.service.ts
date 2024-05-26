import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class MainService {

  constructor(private http: HttpClient, private cookie: CookieService) { }

  // ---------------- cookie ----------------

  set_cookie(name: string, value: string){
    this.cookie.set(name, value)
  }

  get_cookie(name: string){
    return this.cookie.get(name)
  }

  delete_cookie(name: string){
    this.cookie.delete(name)
  }



  // ---------------- login ----------------

  login(data: any){ 
    return this.http.post('http://localhost:5000/login', data)
  }


  // ---------------- push-data ----------------

  send_file(file: File){
    const formData = new FormData();
    formData.append('file', file, file.name);

    return this.http.post('http://localhost:5000/upload', formData)
  }


  // ---------------- dashboard ----------------


  get_results(){
    return this.http.get('http://localhost:5000/dashboard')
  }

  send_results(data:any){
    return this.http.post('http://localhost:5000/results', data)
  }

}
