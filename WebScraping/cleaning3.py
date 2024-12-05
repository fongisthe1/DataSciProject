import pandas as pd

df = pd.read_csv("./Database-files/final3_arxiv_articles.csv")

mapper1 = {
    'adap-org':'Adaptation and Self-Organizing Systems',
    'chao-dyn':"Chaotic Dynamics",
    'cmp-lg':'Computation and Language',
    'solv-int':'Exactly Solvable and Integrable Systems',
    'chem-ph':"Chemical Physics"
}

mapper2 = {
    'astro-ph':'Astrophysics',
    'adap-org':"Nonlinear Science",
    'chao-dyn':'Nonlinear Science',
    'atom-ph':'Atom Physics',
    'cmp-lg':"Computer Science",
    'cond-mat':"Condensed Matter",
    'solv-int':"Nonlinear Science",
    'chem-ph':"Physics"
}

#Deal with null values
df.loc[df['Subject Areas'].isnull() | (df['Subject Areas'] == ''), 'Classification'] = (df['cat_id'].map(mapper1))    # Fill Subject Areas where missing
missing_mask = df['Subject Areas'].isnull() | (df['Subject Areas'] == '')
df.loc[missing_mask, 'Subject Areas'] = df.loc[missing_mask, 'cat_id'].map(mapper2)
temp = df[df['Subject Areas'].isnull()].groupby('cat_id').count()
print(temp)
#Remove Time of day of publication
df['Publication Date'] = df['Publication Date'].apply(lambda x: x.split('T')[0])
print(df.head)

#Save to the file
df.to_csv('./Database-files/final4_arxiv_articles.csv',index=False)
print("Successfully Saved")