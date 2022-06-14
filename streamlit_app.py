import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit)
  fruityvice_df = pd.json_normalize(fruityvice_response.json())
  return fruityvice_df

def get_fruit_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt").set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)
streamlit.header('Fruityvice Fruit Advice!')

try:
  fruit = streamlit.text_input("What fruit would you like information about?")
  if not fruit:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_df = get_fruityvice_data(fruit)
    streamlit.dataframe(fruityvice_df)
except URLError as e:
  streamlit.error()

#streamlit.stop()
streamlit.header("The fruit load list contains:")
if streamlit.button("get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_list()
  streamlit.dataframe(my_data_row)

#sel_fruit = streamlit.text_input("What fruit would you like to add?","jackfruit")
#streamlit.write("Thanks for adding", fruit)
#my_cur.execute("insert into fruit_load_list values('from streamlit')")
