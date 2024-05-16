import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class MainService {

  constructor(private http: HttpClient) { }



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

  send_results(data:any){
    return this.http.post('http://localhost:5000/results', data)
  }

}
