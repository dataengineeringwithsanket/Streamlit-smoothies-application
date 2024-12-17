# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")

name=st.text_input('Name on Smoothie: ')
st.write(
    """Choose the fruit you want in your custom smoothie.
    """
)


# Get the current credentials
cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)


ingredients_list = st.multiselect('Choose upto 5 ingredients: ', my_dataframe ,max_selections=5)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit + ' '

        #st.write('List Ingredient string: ' + ingredients_string)
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(each_fruit + ' Nutrition information')
    
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        #st.text(smoothiefroot_response.json())
        sfdf=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name + """')"""
    submit = st.button('Submit Order')
    # st.write(my_insert_stmt)
    if submit:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")

 #st.text(smoothiefroot_response.json(),use_container_width=True)
