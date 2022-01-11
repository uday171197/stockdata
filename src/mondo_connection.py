#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 01:01:29 2021

@author: uday
"""
import urllib
import pymongo

client = pymongo.MongoClient("mongodb+srv://stockdata:"+"stockdata@4321"+"@cluster0.cbllb.mongodb.net/stockdata?retryWrites=true&w=majority")
db = client.test
