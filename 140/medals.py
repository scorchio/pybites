import pandas as pd

data = "https://bites-data.s3.us-east-2.amazonaws.com/summer.csv"


def athletes_most_medals(data=data):
    medals_df = (
        pd.read_csv(data)
        .groupby(['Gender', 'Athlete'])
        .size()
        .reset_index(name='Medals')
    )
    most_medals_df = (
        medals_df
        .groupby(['Gender'])
        .apply(lambda row: row.nlargest(1, "Medals"))
        .reset_index(drop=True)
        [["Athlete", "Medals"]]
        .set_index('Athlete')
    )
    return most_medals_df.to_dict('dict')['Medals']

if __name__ == "__main__":
    athletes_most_medals()