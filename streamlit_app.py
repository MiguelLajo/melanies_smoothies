# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
    )

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)  # Más eficiente que el loop
    
    # Sentencia CORRECTA que menciona ambas columnas
    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        try:
            session.sql(my_insert_stmt).collect()
            st.success(f'✅ Your Smoothie is ordered, {name_on_order}!')
        except Exception as e:
            st.error(f"Order failed: {str(e)}")
