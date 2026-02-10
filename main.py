from pydantic import BaseModel,EmailStr,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional,Annotated

class Patient(BaseModel):
    name:str
    email:EmailStr
    age:int
    weight:float
    height:float
    married:Annotated[bool,Field(default=None,description='Is the patient married')]
    allergies:Optional[List[str]]=None
    contact_details:Dict[str,str]

    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

    @model_validator(mode="after")
    def validate_emergency_conatct(cls,model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('error')
        return model

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains=['hdfc.com']

        domain_name=value.split('@')[-1]

        if(domain_name) not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value

    @field_validator('name')
    @classmethod
    def transfrom_name(cls,value):
        return value.upper()
    


def insert_patient_info(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.calculate_bmi)
    print('Inserted')

patient_info={'name':'Diya','email':'d@hdfc.com','age':65,'weight':45,'height':'5','married':False,'contact_details':{'emergency':'124566'}}
patient1=Patient(**patient_info)

insert_patient_info(patient1)