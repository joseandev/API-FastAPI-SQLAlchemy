from fastapi import APIRouter, HTTPException, Response, status
from config.db import conn
from models.user import users
from schemas.user import User
from cryptography.fernet import Fernet
from typing import List


key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()

@user.get("/users", response_model=List[User], tags=["users"])
def get_users():
        response = conn.execute(users.select()).fetchall()

        if not response:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No users found")
        return response

@user.get("/users/{id}", response_model=List[User], tags=["users"])
def get_user(id: int):
        result = conn.execute(users.select().where(user,s.c.id == id))    
        return result

@user.post("/users", response_model=User, tags=["users"])
def create_user(user: User):
        new_user = {"name": user.name, "email": user.email}
        new_user["password"] = f.encrypt(user.password.encode("utf-8"))
        result = conn.execute(users.insert().values(new_user))
        conn.commit()

        # Obtener el ID del usuario insertado
        last_inserted_id = result.lastrowid

        # Consultar el usuario recién insertado y convertirlo a un diccionario
        inserted_user = conn.execute(users.select().where(users.c.id == last_inserted_id)).first()

        # Convertir el resultado a un diccionario antes de devolverlo
        inserted_user_dict = dict(inserted_user._asdict())

        return inserted_user_dict

@user.put("/users/{id}", response_model=User, tags=["users"])
def update_user(id: int, user: User):
        result = conn.execute(users.update().values(name=user.name, 
                                           email=user.email, 
                                           password=user.password).where(users.c.id == id))
        conn.commit()

        if not result:
                raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No user found")
        updated_user = conn.execute(users.select().where(users.c.id == id)).first()
        return updated_user

@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: int):
        conn.execute(users.delete().where(users.c.id == id))
        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

@user.delete("/users/", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_users():
        conn.execute(users.delete())
        conn.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
