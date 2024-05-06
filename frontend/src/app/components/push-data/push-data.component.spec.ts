import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PushDataComponent } from './push-data.component';

describe('PushDataComponent', () => {
  let component: PushDataComponent;
  let fixture: ComponentFixture<PushDataComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PushDataComponent]
    });
    fixture = TestBed.createComponent(PushDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
