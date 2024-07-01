import pandas as pd



def preprocess(df,region_df):

    df=df[df['Season']=='Summer']
    df=df.merge(region_df , on='NOC',how='left')
    df.drop_duplicates(inplace=True)
    df= pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    df.Gold = df.Gold.replace({True: 1, False: 0})
    df.Silver = df.Silver.replace({True: 1, False: 0})
    df.Bronze = df.Bronze.replace({True: 1, False: 0})
    return df