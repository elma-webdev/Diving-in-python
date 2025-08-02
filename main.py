from fastapi import FastAPI, HTTPException
#Union -> we want to set up a variable with one more type
#Optional ->define a variable as a optional
from typing import Union, Optional
from pydantic import BaseModel
server=FastAPI()

class Ticket(BaseModel):
    id: int
    name: str
@server.get("/public")
def public_route():  
    return {"message":"hello world"}


tickets=[
    {"id":1,"name":"ticket1"},
    {"id":2,"name":"ticket2"},
    {"id":3,"name":"ticket3"},
    {"id":4,"name":"ticket4"},
    {"id":5,"name":"ticket5"},]

@server.get("/tickets")
def get_tickets():
   return tickets


# Route params
@server.get("/tickets/{id}")
def get_a_ticket(id:int):
        for ticket in tickets:
            if ticket["id"]==id:
                return ticket
        raise HTTPException(status_code=404, detail="Ticket não encontrado")

#Query params, o facto de nao ter id na URL lhe torna automaticamente query params
@server.get("/ticket/search")
def search_ticket(id: Optional[int] = None, name:str=""):  
    #if id is not None:
    for ticket in tickets:
        if ticket["id"] == id and ticket["name"] == name:
            return ticket 
    raise HTTPException(status_code=404, detail= f"Ticket {id, name} não encontrado")

@server.put("/add_ticket")
# ticket pode ser do tipo dict ou Ticket
def add_ticket(ticket:Ticket):
    tickets.append(ticket)
    return tickets

# Editar name_ticket no query params
@server.put("/update_ticket/{id}")
def update_ticket(id:int, name:str):
    for ticket in tickets:
        if ticket["id"] == id:
            ticket["name"] = name
            return ticket
    raise HTTPException(status_code=404, detail= f"Ticket {id} não encontrado")

# Editar name_ticket no req.body
@server.post("/update_a_ticket/{id}")

# podia criar uma nova baseModel apenas pra validar o name do ticket para str
def update_ticket(id:int, name:Ticket):
    for ticket in tickets:
        if ticket["id"] == id:
            ticket["name"] = name.name
            return ticket
    raise HTTPException(status_code=404, detail= f"Ticket {id} não encontrado")

# deletar o ticker com o remove, que deleta o elemento
@server.delete("/delete_a_ticket/{id}")
def delete_ticket(id:int):
    for ticket in tickets:
        if ticket["id"] == id:
            tickets.remove(ticket)
            return tickets
    raise HTTPException(status_code=404, detail= f"Ticket {id} não encontrado")

# deletar um ticket com o pop, que deleta a partir do indice
@server.delete("/delete_ticket/{id}")
def delete_ticket(id:int):
    for i, ticket in enumerate(tickets):
        if ticket["id"] == id:
            apagado= tickets.pop(i)
            return apagado
    raise HTTPException(status_code=404, detail= f"Ticket {id} não encontrado")