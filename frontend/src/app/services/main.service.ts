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

  logout(){
    this.cookie.deleteAll()
    localStorage.clear()
  }



  // ---------------- login ----------------

  login(data: any){ 
    return this.http.post('http://127.0.0.1:8000/login', data)
  }


  // ---------------- push-data ----------------

  send_file(file: File){
    const formData = new FormData();
    formData.append('file', file, file.name);

    return this.http.post('http://127.0.0.1:8000/upload', formData)
  }


  // ---------------- dashboard ----------------


  get_results(){
    return this.http.get('http://127.0.0.1:8000/dashboard')
  }

  send_results(data:any){
    return this.http.post('http://127.0.0.1:8000/results', data)
  }


  // ---------------- historial ----------------

  get_historial(){
    return this.http.get('http://127.0.0.1:8000/historial')
  }

}
