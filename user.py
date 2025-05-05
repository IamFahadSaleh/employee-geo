import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

import folium
from streamlit_folium import st_folium


def read_data():
	conn = st.connection("gsheets", type=GSheetsConnection)
	df = conn.read(worksheet="EmpTable")
	data = []
	
	for row in df.itertuples():
		data.append({
			'name' : str(row.Name),
			'mobile' : str(row.Mobile),
			'latitude' : float(row.Lati),
			'langitude' : float(row.Long)
		})
	
	return data
	
st.set_page_config(
	page_title="Gifting & Recognition for Employees",
	page_icon=":gift:"
)

st.title("Gifting for Employees :gift:")

# Create a connection object.

data = read_data()

map = folium.Map(location=[21.682952865478285, 39.46426391601563], zoom_start=9)

for info in data:
	location = info['latitude'], info['langitude']
	emp = str(info['name']) + "\n" + str(info['mobile'])
	folium.Marker(location, popup=emp).add_to(map)

st_folium(map, width=700)





st.sidebar.success("Select a page above")































































