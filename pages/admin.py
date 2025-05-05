import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

import folium
from folium.plugins import Draw
from streamlit_folium import st_folium


st.set_page_config(
	page_title="Admin Page",
	page_icon=":smile:"
)

conn = st.connection("gsheets", type=GSheetsConnection)


st.title("Admin Page")


m = folium.Map(location=[21.682952865478285, 39.46426391601563], zoom_start=10, map_type="cartodbpositron", width="75%", height="100%")


col1, col2 = st.columns(2)

with col1:
	st.subheader("Employee Entries")
	Draw(export=True).add_to(m)
	output = st_folium(m)

with col2:
	st.subheader("Address picks")
	# Fetch existing vendors data
	existing_data = conn.read(worksheet="EmpTable", usecols=list(range(4)), ttl=5)
	existing_data = existing_data.dropna(how="all")
	existing_data["Name"] = existing_data["Name"].astype(str)
	
	with st.form(key='employee_form', clear_on_submit=True):
		employee_name = st.text_input(label='Employee Name*')
		mobile = st.text_input(label='Mobile')
		if output["last_clicked"] is None:
			lng = st.text_input(label='Longtitude*')
		else:
			lng = st.text_input(label='Longtitude*', value=output["last_clicked"]["lng"])
		
		if output["last_clicked"] is None:
			lat = st.text_input(label='Latitude*')
		else:
			lat = st.text_input(label='Latitude*', value=output["last_clicked"]["lat"])
		
		# Mark Mandatory Fields
		st.markdown('**required*')
		
		submit_button = st.form_submit_button(label='Save')
		
		
		# If the submit button is pressed
		if submit_button:
			# check if all mandatory fields are filled
			if not employee_name or not lng or not lat:
				st.warning('Ensure all mandatory fields ar filled')
				st.stop()
			elif existing_data["Name"].str.contains(employee_name).any():
				st.warning('A vendor with this company name already exists')
				st.stop()
			else:
				# create a new row of vendor data
				employee_data = pd.DataFrame(
					[
						{
							'Name' : str(employee_name),
							'Mobile' : str(mobile),
							'Long' : lng,
							'Lati' : lat,
						}
					]
				)
				
				m = folium.Map(location=[21.682952865478285, 39.46426391601563], zoom_start=10, map_type="cartodbpositron", width="75%", height="100%")
				Draw(export=True).add_to(m)
				
				# add the new vendor data to the existing data
				updated_df = pd.concat([existing_data, employee_data], ignore_index=True)
				
				# update google sheets with the new vendor data
				conn.update(worksheet='EmpTable', data=updated_df)
				
				st.session_state[1] = ""
				st.session_state[2] = ""
				
				st.success('successfully submitted')

		
		
		
		




























































































