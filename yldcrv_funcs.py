# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 13:31:20 2021

@author: mbourque
"""
import pandas as pd
import pdblp


def get_data(sdate, edate):
    
    con = pdblp.BCon()
    con.start()
    
    ### Canada ###
    df_cad = con.bdh(['GTCAD3M Govt',
                      'GTCAD6M Govt',
                      'GTCAD1Y Govt', 
                      'GTCAD2Y Govt', 
                      'GTCAD3Y Govt',  
                      'GTCAD5Y Govt', 
                      'GTCAD7Y Govt',
                      'GTCAD10Y Govt', 
                      'GTCAD20Y Govt', 
                      'GTCAD30Y Govt'], 
                      'yld_ytm_mid', sdate, edate)
    
    df_cad = df_cad.dropna()
    df_cad = df_cad.droplevel('field', 1)
    
    df_cad = df_cad[['GTCAD3M Govt',
                      'GTCAD6M Govt',
                      'GTCAD1Y Govt', 
                      'GTCAD2Y Govt', 
                      'GTCAD3Y Govt',
                      'GTCAD5Y Govt', 
                      'GTCAD7Y Govt', 
                      'GTCAD10Y Govt', 
                      'GTCAD20Y Govt', 
                      'GTCAD30Y Govt']]
    
    ### Ontario ###
    df_ont = con.bdh(['IB3MONT BVLI INDEX', 
                      'IB6MONT BVLI INDEX',
                      'IB01ONT BVLI INDEX',
                      'IB02ONT BVLI INDEX',
                      'IB03ONT BVLI INDEX',
                      'IB05ONT BVLI INDEX',
                      'IB07ONT BVLI INDEX',
                      'IB10ONT BVLI INDEX',
                      'IB20ONT BVLI INDEX',
                      'IB30ONT BVLI INDEX'], 
                     'PX_LAST', sdate, edate)
    
    df_ont = df_ont.dropna()
    df_ont = df_ont.droplevel('field', 1)
    
    df_ont = df_ont[['IB3MONT BVLI INDEX', 
                      'IB6MONT BVLI INDEX',
                      'IB01ONT BVLI INDEX',
                      'IB02ONT BVLI INDEX',
                      'IB03ONT BVLI INDEX',
                      'IB05ONT BVLI INDEX',
                      'IB07ONT BVLI INDEX',
                      'IB10ONT BVLI INDEX',
                      'IB20ONT BVLI INDEX',
                      'IB30ONT BVLI INDEX']]
    
    ### Quebec ###
    df_que = con.bdh(['IB3MQUE BVLI INDEX', 
                      'IB6MQUE BVLI INDEX',
                      'IB01QUE BVLI INDEX',
                      'IB02QUE BVLI INDEX',
                      'IB03QUE BVLI INDEX',
                      'IB05QUE BVLI INDEX',
                      'IB07QUE BVLI INDEX',
                      'IB10QUE BVLI INDEX',
                      'IB20QUE BVLI INDEX',
                      'IB30QUE BVLI INDEX'], 
                     'PX_LAST', sdate, edate)
    
    df_que = df_que.dropna()
    df_que = df_que.droplevel('field', 1)
    
    df_que = df_que[['IB3MQUE BVLI INDEX', 
                      'IB6MQUE BVLI INDEX',
                      'IB01QUE BVLI INDEX',
                      'IB02QUE BVLI INDEX',
                      'IB03QUE BVLI INDEX',
                      'IB05QUE BVLI INDEX',
                      'IB07QUE BVLI INDEX',
                      'IB10QUE BVLI INDEX',
                      'IB20QUE BVLI INDEX',
                      'IB30QUE BVLI INDEX']]
    
    
    ### Alberta ###
    df_ab = con.bdh(['IB3MAB BVLI INDEX', 
                      'IB6MAB BVLI INDEX',
                      'IB01AB BVLI INDEX',
                      'IB02AB BVLI INDEX',
                      'IB03AB BVLI INDEX',
                      'IB05AB BVLI INDEX',
                      'IB07AB BVLI INDEX',
                      'IB10AB BVLI INDEX',
                      'IB20AB BVLI INDEX',
                      'IB30AB BVLI INDEX'],                     
                     'PX_LAST', sdate, edate)
    
    df_ab = df_ab.dropna()
    df_ab = df_ab.droplevel('field', 1)
    
    df_ab = df_ab[['IB3MAB BVLI INDEX', 
                    'IB6MAB BVLI INDEX',
                    'IB01AB BVLI INDEX',
                    'IB02AB BVLI INDEX',
                    'IB03AB BVLI INDEX',
                    'IB05AB BVLI INDEX',
                    'IB07AB BVLI INDEX',
                    'IB10AB BVLI INDEX',
                    'IB20AB BVLI INDEX',
                    'IB30AB BVLI INDEX']]
    
    ### BC ###
    df_bc = con.bdh(['IB3MBC BVLI INDEX', 
                      'IB6MBC BVLI INDEX',
                      'IB01BC BVLI INDEX',
                      'IB02BC BVLI INDEX',
                      'IB03BC BVLI INDEX',
                      'IB05BC BVLI INDEX',
                      'IB07BC BVLI INDEX',
                      'IB10BC BVLI INDEX',
                      'IB20BC BVLI INDEX',
                      'IB30BC BVLI INDEX'],                      
                     'PX_LAST', sdate, edate)
    
    df_bc = df_bc.dropna()
    df_bc = df_bc.droplevel('field', 1)
    
    df_bc = df_bc[['IB3MBC BVLI INDEX', 
                    'IB6MBC BVLI INDEX',
                    'IB01BC BVLI INDEX',
                    'IB02BC BVLI INDEX',
                    'IB03BC BVLI INDEX',
                    'IB05BC BVLI INDEX',
                    'IB07BC BVLI INDEX',
                    'IB10BC BVLI INDEX',
                    'IB20BC BVLI INDEX',
                    'IB30BC BVLI INDEX']]


    return df_cad, df_ont, df_que, df_ab, df_bc

def is_busday(date):
    return bool(len(pd.bdate_range(date, date)))