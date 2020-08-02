import pandas as pd

data = "https://bites-data.s3.us-east-2.amazonaws.com/summer.csv"


def athletes_most_medals(data=data):
    pd.read_csv(data) 
    
if __name__ == "__main__":
    athletes_most_medals()