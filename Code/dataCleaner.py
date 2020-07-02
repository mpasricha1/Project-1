#renameJobs and cleanValues originally written by Melissa
#Class creation and alterations to logic by Mark
#This Class performs all the data cleaning
from listFile import scientist_list
from listFile import analyst_list
from listFile import cleanCityList
import pandas as pd

class ProcessData():
    data_scientist_list = scientist_list
    data_analyst_list = analyst_list
    cityList = cleanCityList
    
    def renameJobs(self, job_data):
        indexCount = 0
        for job in job_data["job name"].tolist():
            try:
                job=job.replace("," ,"")
                job=job.replace(")" ,"")
                job=job.replace("(" ,"")
                job=job.replace("-" ,"")
                job_word=job.lower().split(" ")
                other_exists=True
                for word in job_word:
                    if word in self.data_scientist_list:
                        job_data.loc[indexCount, "simple name"] = "Data Scientist"
                        other_exists=False
                        print(f"Changing name for {job} to Data Scientist")
                        indexCount+=1
                        break
                    elif word in self.data_analyst_list:
                        job_data.loc[indexCount, "simple name"]  = "Data Analyst"
                        other_exists=False
                        print(f"Changing name for {job} to Data Analyst")
                        indexCount+=1
                        break
                if other_exists == True:
                 job_data.loc[indexCount, "simple name"]  = "Other"
                 print(f"Changing name for {job} to Other")
                 indexCount+=1
            except:
                break

        return job_data

    def dropUnwantedColumns(self, df):
        if "job id" in df.columns:
            df = df.drop(["Unnamed: 0"],axis=1)
            df.dropna(subset=["job id"], inplace=True)
        elif "company id" in df.columns:
            df = df.drop(["Unnamed: 0"],axis=1)
            df.dropna(subset=["company id"], inplace=True)
        return df

    def mergeAndSplitLocation(self, job_df, company_df):
        merged_df = job_df.merge(company_df, on="company id", how="left")
        merged_df[["city", "state"]] = merged_df.location.str.split(", ", expand=True,)

        return merged_df

    def cleanValues(self,df):
        cleaned_df = df[df.location.isin(self.cityList)]
        cleaned_df["industry 1"].fillna("Unspecified", inplace = True)
        cleaned_df["job level"]=cleaned_df["job level"].replace("management","Management")
        cleaned_df.rename(columns={'industy 1': 'Industry','simple name':'Job Title'},inplace=True)

        return cleaned_df



