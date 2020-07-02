#This class is for pulling data from the API 
import requests 
import pandas as pd
import json

class dataPuller():
	def getMaxPageCount(self,base_url,locationString,category): 
		page = "page=1"
		response = requests.get(f"{base_url}&category={category}&{locationString}{page}").json()
		maxPageCount = response["page_count"]
		
		return maxPageCount

	def buildCitiesString(self,cityList, stateList):
		seperator = "%2C%20"
		finalCityURLString = ''
		for x in range(len(cityList)):
			finalCityURLString += f"location={cityList[x]}{seperator}{stateList[x]}&"
		return finalCityURLString
	 
	def getAllResultsJobs(self,base_url, maxPageCount, category, locationString): 
		jobList = []
		pageCount = 1
		page = "page="
		while pageCount <= maxPageCount:
			resultNum = 0
			response = requests.get(f"{base_url}category={category}&{locationString}{page}{pageCount}").json()
			print(f"Loading requests from page {pageCount}")
			while resultNum < 20:
				jobs_dict = {"job id": '',
					 "job level": '',
					 "location": '',
					 "job name": '',
					 "post date": '',
					 "category": '',
					 "company id": '',
					 "company name": '',
					 "content": '',
				}
				try:
					jobs_dict["location"] = response["results"][resultNum]["locations"][0]["name"]
					jobs_dict["job id"] = response["results"][resultNum]["id"]
					jobs_dict["job level"] = response["results"][resultNum]["levels"][0]["name"]
					jobs_dict["job name"] = response["results"][resultNum]["name"]
					jobs_dict["post date"] = response["results"][resultNum]["publication_date"]
					jobs_dict["category"] = response["results"][resultNum]["categories"][0]["name"]
					jobs_dict["company id"] = response["results"][resultNum]["company"]["id"]
					jobs_dict["company name"] = response["results"][resultNum]["company"]["name"]
					jobs_dict["contents"] = response["results"][resultNum]["contents"]
			
				except (KeyError,IndexError):
					pass
				
				jobList.append(jobs_dict)
				resultNum += 1
			pageCount += 1
		return jobList

	def getAllResultsCompanies(self,base_url,maxPageCount,locationString,category):
		companyList = []
		pageCount = 1
		page = "&page="
		while pageCount <= maxPageCount:
			resultNum = 0
			response = requests.get(f"{base_url}{category}{page}{pageCount}&{locationString}").json()
			print(f"Loading requests from page {pageCount}")
			while resultNum < 20:
				company_dict = {"company id": '' }
				try: 
					company_dict["company id"] = response["results"][resultNum]["id"]
					if len(response["results"][resultNum]["industries"]) > 1: 
						for i in range(len(response["results"][resultNum]["industries"])): 
							company_dict[f"industry {i+1}"] = response["results"][resultNum]["industries"][i]["name"]
					else:
					 company_dict["industry 1"] = response["results"][resultNum][0]["industries"]
				except(KeyError,IndexError):
					pass

				companyList.append(company_dict)
				resultNum += 1 
			pageCount += 1
		return companyList

