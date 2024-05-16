import { AfterViewInit, Component, TemplateRef } from '@angular/core';
import { FormArray, FormBuilder, FormGroup } from '@angular/forms';
import { BsModalRef, BsModalService } from 'ngx-bootstrap/modal';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements AfterViewInit{


  modalRef?: BsModalRef;
  msg_final:any
  form!: FormGroup

  results_baterias: any


  constructor(private modalService: BsModalService, private mainservice: MainService, private myformg: FormBuilder) {
    this.form = this.myformg.group({
      baterias: this.myformg.array([])
    });
  }
 
  openModal(template: TemplateRef<void>) {
    this.modalRef = this.modalService.show(template);
    this.msg_final = ""
  }

  get baterias(): FormArray {
    return this.form.get('baterias') as FormArray;
  }

  initForm() {
    for (const [id, value] of Object.entries(this.results_baterias)) {
      this.baterias.push(this.myformg.group({
        id: [id],
        value: [value]
      }));
    }
  }

  ngAfterViewInit(): void {

    this.results_baterias = {"1": true, 
      "2": false,
      "3": true,
      "4": false
    }

    this.initForm();

    /*this.mainservice.get_results().subscribe((res:any) => {
      this.results_baterias = res["results"];
      this.initForm();
    });*/
  }


  pilas: any = [3, 1, 2];
  tabs = ['AJCJ23', 'ADJCK32', 'ACD45'];

  actual_tab = 0;
  name:any

  datasets = {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      label: 'My First Dataset',
      data: [65, 59, 80, 81, 56, 55, 40],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(255, 205, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(201, 203, 207, 0.2)'
      ],
      borderColor: [
        'rgb(255, 99, 132)',
        'rgb(255, 159, 64)',
        'rgb(255, 205, 86)',
        'rgb(75, 192, 192)',
        'rgb(54, 162, 235)',
        'rgb(153, 102, 255)',
        'rgb(201, 203, 207)'
      ],
      borderWidth: 1
    }]
  };



  change_data(id:any){
    this.actual_tab = id
    this.name = this.tabs[id]
  }


  send_results(){

    const result = this.form.value.items.reduce((acc: any, item: any) => {
      acc[item.id] = item.value;
      return acc;
    }, {});


    this.mainservice.send_results(result).subscribe((res:any) => {
      this.msg_final = res["msg"]
    })
  }


}
