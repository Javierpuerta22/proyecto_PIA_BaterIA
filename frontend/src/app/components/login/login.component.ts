import { AfterViewInit, Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { route_to_images } from 'src/app/app.component';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements AfterViewInit {

  form!: FormGroup
  error_msg: string = '';
  constructor(private mainservice:MainService, private myformg:FormBuilder, private router:Router) {
    this.form = this.myformg.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    })
   }

   
   route_image = route_to_images + "logo.jpg"

   ngAfterViewInit(): void {
       this.mainservice.logout();
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
