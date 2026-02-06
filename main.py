from fastapi import FastAPI,Path,HTTPException,Query
import json


app=FastAPI()

def loadData():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

@app.get('/')
def hello():
    return{'message':'Patient management system api'}

@app.get('/about')
def about():
    return{'message':'functional patient manage api'}

@app.get('/view')
def view():
    data=loadData()

    return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description='Id of the patient in db',examples='1')):
    data=loadData()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient not found')


@app.get('/sort')
def sort_patients(sort_by:str=Query(...,description='Sort on the basis of height,weight or bmi'),order:str=Query('asc',description='sort in asc or desc order')):
    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'Invalid field select from{valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order select between asc and desc')
    
    data=loadData()

    sort_order=True if order=='desc' else False

    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=True)

    return sorted_data