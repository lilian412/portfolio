import pickle 
import streamlit as st
from PIL import Image
import numpy as np
import shap
import pandas as pd
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import sys
    
###########################################################
st.set_page_config(page_icon="💸", page_title = "Lilian Martin",
                   layout="wide", initial_sidebar_state = "auto")

st.set_option('deprecation.showPyplotGlobalUse', False)
# We get our fitted model
model = pickle.load(open('./data/health_model.pkl', 'rb'))

# Fonction header
def head(a, b, w):
  col1, col2 = st.columns([3,1])
  with col1:
    st.markdown(a)
  with col2:
    st.image(b, width = w) 


## Fonction SHAP
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

#####################
# Header 
head('''
# Assurancetourix
''',
Image.open('./img/assurancetourix.png'), 125)

# Rentrer les variables test:
#############################
col1, col2 = st.columns([1,1])
with col1:
  sex = st.radio("Select your gender",('Male', 'Female', 'Other'))
with col2:
  smoke = st.selectbox('Do you smoke ?',('Yes', 'No'))

col1, col2 = st.columns([1,1])
with col1:
  age = st.slider('How old are you?', 18, 120,18)
with col2:
  childs = st.slider('How many childrens do you have?', 0, 12,0)

col1, col2 = st.columns([1,1])
with col1:
  height = st.number_input('Height (m,cm)', min_value = .5, value = 1.65)
with col2:
  weight = st.number_input('Weight (kg)', min_value = 30, value = 60)

sexe = np.where(sex == 'Male', 1, 0)
smoker = np.where(smoke == 'Yes', 1, 0)
bmi = weight/height**2
st.write(f'**BMI: {round(bmi,2)}**')

############################################
## We build our X_test row, with col name for shap explicability
test = [[age, sexe, bmi, childs, smoker]]
df = pd.DataFrame(test,
columns = ["age", "sex","bmi","childrens","smoke"])

st.markdown('''### Calculate the cost by clicking this button''')

## By clicking the button
if st.button('Calculate'):
    # we predict the charges
    price = round(model.predict(test)[0])
    st.markdown(f'## You cost {price}$')
    st.markdown('''#### How did our algorithm predict this value?''')

    # We explain the charges
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df)
    shap.initjs()
    # st.write(explainer.expected_value+shap_values[0:].sum())

    ## Besoin de cette fonction pour pouvoir plot shap dans streamlit
    st_shap(
        shap.plots.force(explainer.expected_value,
        shap_values[0:],
        test,
        feature_names = ["age", "sex","bmi","childrens","smoke"],
        show=False))

    plt.title('Total distribution of observations based on Shap values, colored by Target value')
    shap.summary_plot(shap_values, df, show=False)
    st.pyplot(bbox_inches='tight')
    plt.clf()

else:
    st.write('Click the button after filling all informations to calculate your cost')





