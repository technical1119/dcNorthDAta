import json
import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup



def encode_company_name(company_name):
    return company_name.replace(" ", "%20")



  

def get_revenue_data(company_name):
    time.sleep(random.randint(1, 8))
    encoded_company_name = encode_company_name(company_name)
    req = requests.get(f"https://www.northdata.de/{encoded_company_name}")

    if req.status_code == 200:
        try:
            north_soup = BeautifulSoup(req.text, 'html.parser')
           

            data = north_soup.find("div", class_="tab-content has-bar-charts") if north_soup.find("div", class_="tab-content has-bar-charts") else None
            
            if data: 
                json_data = json.loads(data.attrs["data-data"])
                year = json_data["item"][0]['data']['data'][-1]['year']
                revenue = json_data["item"][0]['data']['data'][-1]['value0']
                print(year, revenue)

                return year, revenue
                
            else:
                print("no data found")
                return None, None
        except:
            print("error getting revenue data")
            time.sleep(15)
            return None, None
    
    else:
        print(req.status_code)
        print("error getting revenue data")
        time.sleep(15)
        return None, None


def main():
    df = pd.read_csv("AOK_data.csv")

    # Initialize empty lists for revenue data
    revenue_years = []
    revenue_amounts = []

    # Iterate through each company name
    for company in df["locationName"]:
        try:
            year, amount = get_revenue_data(company)
            revenue_years.append(year)
            revenue_amounts.append(amount)
        except:
            print("error getting revenue data")
            revenue_years.append(None)
            revenue_amounts.append(None)

    # Add revenue data as new columns
    df["revenue_year"] = revenue_years
    df["revenue_amount"] = revenue_amounts

    df.to_csv("AOK_data_with_revenue.csv", index=False)


    df_barmer= pd.read_csv("Barmer_data.csv")

    # Initialize empty lists for revenue data
    revenue_years = []
    revenue_amounts = []

    # Iterate through each company name
    for company in df_barmer["name"]:
        try:
            year, amount = get_revenue_data(company)
            revenue_years.append(year)
            revenue_amounts.append(amount)
        except:
            print("error getting revenue data")
            revenue_years.append(None)
            revenue_amounts.append(None)

    # Add revenue data as new columns
    df_barmer["revenue_year"] = revenue_years
    df_barmer["revenue_amount"] = revenue_amounts

    df_barmer.to_csv("Barmer_data_with_revenue.csv", index=False)
    



if __name__ == "__main__":
    main()


