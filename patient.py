from fastapi import HTTPException
from pydantic import BaseModel,Field,computed_field
import json
from fastapi.responses import JSONResponse
from typing import Annotated
from fastapi import FastAPI



app=FastAPI()

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
    
def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

@app.post('/create')
def create_patient(patient:Patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient already exists')
    data[patient.id] =patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created successfulyy'})

