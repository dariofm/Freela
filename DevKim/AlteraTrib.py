# coding: utf-8
#Objetivo do Script é corrigir Tributos COFINS movimentada no NFC-e

from dataclasses import replace
import os 
from core.models import Uteis
import time, sys
from bson import ObjectId
import configparser
import datetime

uteis = Uteis()
database = uteis.conexao

Movimentacoes = database["Movimentacoes"]


dt_inicial = datetime.datetime(2022,10,1)
dt_final   = datetime.datetime(2022,10,30) 

print(f'Data Inicial : {dt_inicial}')
print(f'Data Final   : {dt_final}')

#for i in Movimentacoes.find({"Modelo.Modelo":"65","Numero":106561}): >> Filtrar por Número

for i in Movimentacoes.find({"Modelo.Modelo":"65", # >> Filtrar por Data
                            "DataHoraEmissao":{
                                '$gte': dt_inicial,
                                '$lte': dt_final
                                }
                             }):
    idMov = i["_id"]
    print(f'* Nota Fiscal {i["Numero"]} *')
    ItensBase = i['ItensBase']
    
    quantidade_produtos = len(ItensBase)
    print(f'Quantidade de Produtos: {quantidade_produtos}')
    
    indice = 0
    for prd in ItensBase:
        
        print(f'    >> {ItensBase[indice]["ProdutoServico"]["Descricao"]}') 
        print(f'    >> PIS: {ItensBase[indice]["PIS"]["CstPISCOFINS"]["Codigo"]}')   
        print(f'    >> COFINS: {ItensBase[indice]["COFINS"]["CstPISCOFINS"]["Codigo"]}')                 
        print('-----------------------------------------------------------------')
         
        
        Movimentacoes.update_many(
            {
                "_id":idMov    
                },
            {"$set":
                {
                    f"ItensBase.{indice}.COFINS":    {
                        "_t" : "PISCOFINSTributadoSaida",
                        "CstPISCOFINS" : {
                            "_t" : "OperacaoTributavelComAliquotaBasica",
                            "Codigo" : 1,
                            "Descricao" : "Operação Tributável com Alíquota Básica"
                        },
                        "PercentualBaseCalculo" : 100.0,
                        "Percentual" : 3.0,
                        "AbaterValorPisCofinsDoTotalLiquido" : True,
                        "AbaterIcmsBaseCalculoPisCofins" : False
                    }
                    }
                }
     
            )       
        indice = indice + 1  

    
