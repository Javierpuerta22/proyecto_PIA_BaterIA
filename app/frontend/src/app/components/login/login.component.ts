import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  form!: FormGroup
  error_msg: string = '';
  constructor(private mainservice:MainService, private myformg:FormBuilder, private router:Router) {
    this.form = this.myformg.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    })
   }

   


  send_form(data: any){

    if (this.form.invalid) {
      this.error_msg = 'Rellena los campos correctamente';
    }

    else{
      if (data.username == 'admin' && data.password == 'admin') {
        this.router.navigate(['/home']);
        this.mainservice.set_cookie('registered', 'true');

      }
      else{
        this.error_msg = 'Usuario o contraseña incorrectos';
      }
    }

    /*
    this.mainservice.login(data).subscribe((res) => {
      console.log(res);
    })
  }*/
  }



}
