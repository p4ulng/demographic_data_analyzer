import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    df_men=df[df['sex']=='Male']
    df_men['sex'].unique()
    df_men.loc['age']=df_men['age'].astype(int)
    average_age_men = df_men['age'].mean().round(1)   
  

    # What is the percentage of people who have a Bachelor's degree?
    education_counts = df['education'].value_counts()

    percentage_bachelors = ((education_counts['Bachelors']/education_counts.sum())*100).round(1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = education_counts[education_counts.index.isin({'Bachelors','Masters','Doctorate'})]
    higher_education =(100* (higher_education.sum()/education_counts.sum()) ).round(1)
    lower_education = (100*(1 - higher_education)).round(1)

    # percentage with salary >50K
    df_higher_education = df[df['education'].isin(['Bachelors','Masters','Doctorate'])]

    series_higher_education_salary=df_higher_education['salary'].value_counts()
    
    higher_education_rich = (100*series_higher_education_salary['>50K']/series_higher_education_salary.sum()).round(1)


    df_lower_education = df[~df['education'].isin(['Bachelors','Masters','Doctorate'])]
    
    series_lower_education_salary=df_lower_education['salary'].value_counts()
    
    lower_education_rich = (100*series_lower_education_salary['>50K']/series_lower_education_salary.sum()).round(1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = len(df['hours-per-week']==min_work_hours)

    df_minHours=df[df['hours-per-week']==min_work_hours]

    df_minHours_salaryCount = df_minHours['salary'].value_counts()

    rich_percentage = 100*(df_minHours_salaryCount['>50K']/df_minHours_salaryCount.sum())

    # What country has the highest percentage of people that earn >50K?
    df1=df.groupby('native-country')['salary'].value_counts(normalize=True).mul(100).rename('percentage').reset_index()
    salary_over_50k=df1[df1['salary']=='>50K']
    #print(salary_over_50k.sort_values('percentage',ascending=False))
    max_salary_country=salary_over_50k.nlargest(1,'percentage')
    #print(max_salary_country)
    highest_earning_country= max_salary_country['native-country'].values[0]
    highest_earning_country_percentage=max_salary_country['percentage'].values[0].round(1)

    # Identify the most popular occupation for those who earn >50K in India.
    df_india_high_salary = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')].filter(items=["occupation"]).value_counts().rename('num').reset_index()
    df_india_high_salary
    top_IN_occupation = df_india_high_salary.nlargest(1,'num')['occupation'].values[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
