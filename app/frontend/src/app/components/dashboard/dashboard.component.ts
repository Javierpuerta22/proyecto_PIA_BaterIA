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
  ploting_data:any


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

    this.mainservice.get_results().subscribe((res:any) => {
      this.results_baterias = res["results"];
      this.tabs = res["plots"].keys;
      this.actual_tab = this.tabs[0];


      this.ploting_data = res["plots"];


      this.initForm();
    })
  }


  pilas: any = [3, 1, 2];
  tabs:any

  actual_tab:any;
  name:any



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
