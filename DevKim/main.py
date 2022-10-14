# coding: utf-8
from dataclasses import replace
import os 
from core.models import Uteis
import firebirdsql
import time, sys
from bson import ObjectId
import configparser
from datetime import datetime

bancoCon = firebirdsql.connect(user="SYSDBA",password="masterkey",database='C:\\import\\DATAGES (1).FDB',host='127.0.0.1',charset="latin1")
bCursor = bancoCon.cursor()  

uteis = Uteis()
database = uteis.conexao

Pessoas = database["Pessoas"]


bCursor.execute('select NOME,OBS from CLIENTE_TMP')

for cli in bCursor.fetchall():
    
    Pessoas.update_one(
        {"Nome":cli[0]},
        {
            "$set":{"Observacao":cli[1]}
        })

