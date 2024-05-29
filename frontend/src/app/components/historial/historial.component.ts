import { AfterViewInit, Component } from '@angular/core';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-historial',
  templateUrl: './historial.component.html',
  styleUrls: ['./historial.component.css']
})
export class HistorialComponent implements AfterViewInit{


  result_baterias:any 
  ploting_data:any

  constructor(private service: MainService) { }


  ngAfterViewInit(): void {
    this.service.get_historial().subscribe((res:any) => {
      this.result_baterias = res;
      this.ploting_data = res["means"]
    })
      
  }


}
