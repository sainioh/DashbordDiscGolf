import sqlite3
import pandas as pd

dg_db = sqlite3.connect('discgolf.db')
c = dg_db.cursor()