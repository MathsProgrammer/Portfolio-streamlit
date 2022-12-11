import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
from streamlit_pandas_profiling import st_profile_report
from textblob import TextBlob
import cleantext




menu = option_menu(menu_title=None,
    options = ["Home",'Automated Data Analysis','Sentiment Analysis', 'Nutrition',], 
    orientation = "horizontal")


if menu == "Home":
    st.title("Application Portfolio")
    st.write("I've deployed this application portfolio with a few functions for you to try. Seemed like a nicer way of seeing if someone can code rather than masses of code on GitHub.")
    pass

if menu == 'Sentiment Analysis':
    st.title("Sentiment Analysis")
    st.write("Sentiment analysis is used to get the emotional undertone of a statement or passage of text without having to read it yourself. It is part of a much wider natural language toolset but this in particular could be used to filter through large amounts of reviews or emails. A score of 1 is the most positive while -1 is negative. Enter your own text below to see the sentiment:")
    with st.expander('Analyse Text'):
        text = st.text_input('Text here: ')
        if text:
            blob = TextBlob(text)
            if blob.sentiment.polarity >= 0.36:
                st.write('Positive with a score of:', round(blob.sentiment.polarity,2))
            if blob.sentiment.polarity <= -0.36:
                st.write('Negative with a score of:', round(blob.sentiment.polarity,2))
            else:    
                st.write('Fairly neutral with a score of:', round(blob.sentiment.polarity,2))
            
        pre = st.text_input("Clean Text:")
        if pre:
            st.write(cleantext.clean(pre, clean_all= False, extra_spaces=True ,
                                 stopwords=True ,lowercase=True ,numbers=True , punct=True))
    st.write("If you have an Excel file of comments you can drop it into the box below to have sentiment analysis automatically added in a new column. This will be then downloadable for you to use.")        
    with st.expander('Analyse CSV'):
        upl = st.file_uploader('Upload file')

    def score(x):
        blob1 = TextBlob(x)
        return blob1.sentiment.polarity

#
    def analyze(x):
        if x >= 0.5:
            return 'Positive'
        elif x <= -0.5:
            return 'Negative'
        else:
            return 'Neutral'

#
    if upl:
        df = pd.read_excel(upl)
        del df['Unnamed: 0']
        df['score'] = df['tweets'].apply(score)
        df['analysis'] = df['score'].apply(analyze)
        st.write(df.head(10))

        @st.cache
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='sentiment.csv',
            mime='text/csv',
        )        
    
if menu == 'Automated Data Analysis':
    with st.sidebar:
        st.title("Automated Data Analysis")
        user_menu1 = st.radio("Navigation",
            options = ['Upload','EDA']
        )
             
        
    if user_menu1 == "Upload":
        st.title("Upload data for modelling")
        st.write("All you have to do is select a CSV file and click on the EDA secction for extensive data analysis.")
        file = st.file_uploader("Upload your dataset")
        if file: 
            df = pd.read_csv(file,index_col = None)
            df.to_csv("Source.csv",index=None)
            st.dataframe(df)
            
    if os.path.exists("Source.csv"):
        df = pd.read_csv("Source.csv", index_col = None)    

    if user_menu1 == "EDA":
        st.title("Automated Data Analysis")
        profile_report = df.profile_report()
        st_profile_report(profile_report)





if menu == "Nutrition":
    with st.sidebar:
        st.title("Nutrition Advisor")
        user_menu = st.radio("Navigation",
            options = ['Nutrition Advisor','BMI Calculator','Basic Calculator']
        )
    
    if user_menu == 'Basic Calculator':
        st.title("Calculator")
        
        first = st.text_input("Enter your first number", "0")
        second = st.text_input("Enter your second number", "0")
        
        operation  = st.selectbox("Select Operation", ["Addition", "Subtraction", "Multiplication", "Division"])
        
        if st.button("Perform Operation:"):
            if operation == "Addition":
                result = float(first) + float(second)
                st.success(result)
                
            elif operation == "Subtraction":
                result = float(first) - float(second)
                st.success(result)        
            
            elif operation == "Multiplication":
                result = float(first) * float(second)
                st.success(result)
                
            elif operation == "Division":
                result = float(first)/ float(second)
                st.success(result)        
          
    if user_menu == "BMI Calculator":
        st.title("BMI Calculator")
        st.write("A BMI score is a rule of thumb measurement for healthy weights. It does not take into account gender, frame or muscle mass so be aware that results are not always perfectly indicative of health.")
        
        firsts = st.text_input("Enter your weight in kg", "80")
        seconds = st.text_input("Enter your height in cm", "180")
        bmi = round(int(firsts)/(int(seconds)/100)**2,1)
        
        if bmi>25 or bmi <18:
            st.success(('Your BMI is:', + bmi, 'which is outside of the healthy range 18-25'))
        else:
            st.success(('Your BMI is:', + bmi, 'which is within the healthy range 18-25'))
            
    if user_menu == "Nutrition Advisor":
        st.title("Nutrition Advisor")
        st.write("This section will look at your daily calorie usage to guide you to your goals. Please enter a few metrics below:")  
        genders = st.selectbox("Are you male or female?",["Male","Female"])
        firsts = st.text_input("Enter your weight in kg", "80")
        seconds = st.text_input("Enter your height in cm", "180")
        age = st.text_input("Enter your age", "45")
        
        st.subheader("Your resting calorie burn is:")
        
        if genders == "Male":
            cal = round(88 + (14*float(firsts)) + (4.799*float(seconds)) - (5.677*(float(age))))
            st.success(cal)
        elif genders == "Female":
            cal =  round(447.593 + (11*float(firsts)) + (3.098*float(seconds)) - (4.330*(float(age))))   
            st.success(cal)    
        
        st.write("Now, taking into account your daily activity with how many steps you do a day:")
        step = st.selectbox("Do you know how many steps you take a day roughly?", ["Yes", "No"])
        if step == "No":
            active  = st.selectbox("Daily, how active are you?", ["Low activity (Under 2000 steps)", "British average (2000-5000 steps)", "Active (5000-10000 steps)", "Very Active (10000-15000 steps)"])
            if active == "Low activity (Under 2000 steps)":
                steps = 1500
            elif active == "British average (2000-5000 steps)":
                steps = 4000
            elif active == "Active (5000-10000 steps)":
                    steps = 7500
            elif active == "Very Active (10000-15000 steps)":
                        steps = 12500
        elif step == "Yes":
            steps = st.text_input("How many steps do you take on an average day?", "4000")
        
        
                    
        calextra = ((float(firsts) *2.2)/3) *(int(steps)/1000)
        total = calextra+cal
        st.subheader("You burned an extra:")
        st.success((round(calextra)))
        st.subheader("Your total daily calorie burn is:")
        st.success((round(calextra+cal)))
        
        goal = st.selectbox("What is your goal?",["To gain muscle","To lose fat"])
        
        st.subheader("To sustainably move towards your goal you should aim to eat this many calories a day:")
        
        if goal == "To lose fat":
            st.success(round((round(total - 500,-2))))
        elif goal == "To gain muscle":
            st.success(round((round(total + 300,-2))))
        
        
        
    
    
    
    
    
         