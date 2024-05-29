import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { route_to_images } from 'src/app/app.component';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-push-data',
  templateUrl: './push-data.component.html',
  styleUrls: ['./push-data.component.css']
})
export class PushDataComponent {

  form!: FormGroup;
  msg_error: string = '';

  constructor(private myformg: FormBuilder, private mainservice: MainService, private route:Router) {
    this.form = this.myformg.group({
      file: ['']
    });
   }

   file: File | null = null;

  onFileChange(event: any) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
      this.file = file;
      this.form.patchValue({
        file: file
      });
    }
  }

  onSubmit() {
    if (this.file) {
      // Enviar el archivo al backend
     this.mainservice.send_file(this.file).subscribe((res) => {
        console.log(res);
        this.mainservice.set_cookie('data', 'true');
        this.route.navigate(['/dashboard']);
        
      },
    (error) => {
      this.msg_error = error.error.message;

    })

    }
  }

  route_image = route_to_images + "logo.jpg"




}
