from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin:str

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address:Address


address_dict={'city':'howrah','state':'WB','pin':'711104'}

address1=Address(**address_dict)

patient_dict={'name':'diya','gender':'female','age':20,'address':address1}

p1=Patient(**patient_dict)

temp=p1.model_dump(exclude=['name','age'])

print(p1)
print(p1.address.state)
print((temp))