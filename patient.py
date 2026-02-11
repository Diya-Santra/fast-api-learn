from multiprocessing import Value
from fastapi import HTTPException
from pydantic import BaseModel,Field,computed_field
import json
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
from fastapi import FastAPI



app=FastAPI()

#create patient model
class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ID of the patient',examples=['1'])]
    weight:Annotated[float,Field(gt=0,description='weight of the patient')]
    height:Annotated[float,Field(...,gt=0,description='height of the patient')]
    age:Annotated[int,Field(...,gt=0,description='age of the patient')]
    pressure:float

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
#update patient model
class PatientUpdate(BaseModel):
    weight:Annotated[float,Field(Optional[float],gt=0,description='weight of the patient')]
    height:Annotated[Optional[float],Field(gt=0,description='height of the patient')]
    age:Annotated[Optional[int],Field(gt=0,description='age of the patient')]
    pressure:float

#loading data in file
def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

#saving new data in file
def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

#post route
@app.post('/create')
def create_patient(patient:Patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient already exists')
    data[patient.id] =patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created successfulyy'})

#put route
@app.put('/update/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    
    exsiting_patient_info=data[patient_id]

    updated_patient_info=patient_update.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        exsiting_patient_info[key]=value

    

    data[patient_id]=exsiting_patient_info

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):

    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient deleted'})
