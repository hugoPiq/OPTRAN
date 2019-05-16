# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 13:56:25 2019

@author: Hugo
"""
import numpy as np

def f(x,ro,S,Cx,delta,M,alpha,Cm):
    Rroue=0,5715  #22,7 pouces
    g=9.81
    return x**3*0.5*ro*S*Cx+x*(delta*np.cos(alpha)/Rroue+M*g*np.sin(alpha)-Cm/Rroue)



def Dichotomie(f,a,b,n,ro,S,Cx,delta,M,alpha,Cm):
    m=(a+b)/2
    for i in range(n):
        if f(a,ro,S,Cx,delta,M,alpha,Cm)*f(m,ro,S,Cx,delta,M,alpha,Cm)>0:
            a=m
        else:
            b=m
    return (a+b)/2