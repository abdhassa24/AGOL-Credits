from arcgis.gis import GIS
import pandas as pd
import datetime
import os

date = datetime.datetime.now() - datetime.timedelta(days=2)
date = datetime.datetime.now() 
reportdate = date.strftime("%Y-%m-%d")
profile = ""
gis_account = GIS("https://www.arcgis.com", profile=profile)
report = gis_account.users.me.report(report_type='content',start_time = '',duration = 'monthly')
items = gis_account.content.search("OrganizationItems_{}".format(reportdate),max_items=1)
items[0].download("C:")
print(items[0])
print ("Downloaded AGOL Items Report")
gis_account.content.delete_items(items)
os.rename("C:_{}.csv".format(reportdate),"C:_{}_{}.csv".format(reportdate,profile))
df = pd.read_csv("C:_{}_{}.csv".format(reportdate,profile))
df["Feature Storage Monthly Credit Usage"] = df["Feature Storage Size"] /10 * 2.4
df["Feature Storage Monthly Credit Usage"] = df["Feature Storage Monthly Credit Usage"].round(3)
df ["File Storage Monthly Credit Usage"]= df["File Storage Size"] / 1024 * 1.2
df["File Storage Monthly Credit Usage"] = df["File Storage Monthly Credit Usage"].round(3)
df = df.sort_values("Feature Storage Monthly Credit Usage", ascending=False)
df = df.reindex(columns=["Title","Item ID","Item Url","Item Type","Date Created","Date Modified","Content Category","View Counts","Owner",	"File Storage Size","File Storage Monthly Credit Usage","Feature Storage Size","Feature Storage Monthly Credit Usage","Share Level","# of Groups shared with","Tags","Number of Comments","Is Hosted Service"])
tags = ["Some Tag"] 
df = df[df.Tags.str.contains('|'.join(tags),case=False,na=False)]
df.to_csv("C:{}_{}.csv".format(reportdate,profile),index=False)
print ("AGOL Items Report Ready To Go")
