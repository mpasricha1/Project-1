# This class parses out the job skills from the html 
import pandas as pd 
from bs4 import BeautifulSoup
from listFile import skillList
pd.options.mode.chained_assignment = None

class Parser():
	def parseHtml(self,job_df):
		jobContent = job_df["contents"]
		indexCount = 0 
		try:
			for job in range(len(jobContent)):
				soup = BeautifulSoup(jobContent[job], "lxml")
				text = soup.text
				text=text.replace("," ,"")
				text=text.replace(")" ,"")
				text=text.replace("(" ,"")
				text=text.replace("-" ,"")
				text=text.replace("." ,"")
				words = list(text.lower().split(" "))
				for word in words:
				 	if word in skillList:
				 		index = skillList.index(word)
				 		job_df.loc[indexCount, skillList[index]] = "True"
				indexCount += 1
		except:
			pass
		
		return job_df

		
