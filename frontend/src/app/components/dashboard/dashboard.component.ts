import { AfterViewInit, Component, OnInit, TemplateRef } from '@angular/core';
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
  cantidades:any


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

  ngAfterViewInit() {
    //this.initForm();
    console.log("patata")
    this.mainservice.get_results().subscribe((res:any) => {
      console.log(res)
      this.tabs = res["ids"];
      console.log(this.tabs)
      this.actual_tab = this.tabs[0];
      this.name = this.tabs[0];
      this.results_baterias = res["resultados"]
      this.pilas = res["cantidades_resultados"]


      this.ploting_data = res["plots"];


      this.initForm();
    }, (error) => {
      console.log(error)
    })

  }



  pilas: any = [0,0,0];
  tabs:any

  actual_tab:any;
  name:any



  change_data(id:any){
    this.actual_tab = this.tabs[id]
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
