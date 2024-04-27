'''
Has pipeline to take export.zip and add it to the database.
'''

from export_cda_parser import parse_export
from mysql_inserter import pipeline
import os 

if __name__ == "__main__":
    os.system('mkdir ./temp')
    os.system('unzip export.zip -d temp')
    os.system('rm export.zip')
    df = parse_export("temp/apple_health_export/export.xml")
    pipeline(df)
    os.system('rm -rf temp')