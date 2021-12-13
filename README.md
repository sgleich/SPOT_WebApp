# SPOT Web App
**By:** Samantha Gleich\
**Last Updated:** December 13, 2021\
\
**This web app allows the user to specify a taxonomic group of interest and a depth. Then, the web app summarizes and visualizes 18S tag-sequencing data that were collected at the San Pedro Ocean Time-Series (SPOT) site based on the user input.** 

## Required packages
This web app requires the use of functions in pandas, os, matplotlib, flask, io, and base64 and was created in python 3.7 using the PyCharm IDE. 
```
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template,redirect,render_template,request,session
from io import BytesIO
import base64
app = Flask(__name__)
```

##
