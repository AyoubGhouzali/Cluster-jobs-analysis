import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image
import base64
import os

# Define UI
st.set_page_config(layout="wide", page_title="Cluster Jobs Analysis", )
st.sidebar.success("Select a page")

# Read data
jobs_univ = pd.read_csv("C:/Users/ayoub/Desktop/Stage 1A/Data frames/Jobs_univ.csv", encoding='latin1')
waittime = pd.read_csv("C:/Users/ayoub/Desktop/Stage 1A/Data frames/waittime.csv", encoding='latin1')
waittime_boxp_par = pd.read_csv("C:/Users/ayoub/Desktop/Stage 1A/Data frames/waittime_boxp_par.csv", encoding='latin1')
waittime_boxp_ncpus = pd.read_csv("C:/Users/ayoub/Desktop/Stage 1A/Data frames/waittime_boxp_ncpus.csv",
                                  encoding='latin1')

col = st.columns((1.5, 4.5, 2), gap='medium')

# Sidebar
st.sidebar.header("Input parameters")
year = st.sidebar.selectbox("Année:", ["All", "2022", "2023", "2024"])
month = None
if year != "All":
    month = st.sidebar.selectbox("Mois:",
                                 ["All", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août",
                                  "Septembre", "Octobre", "Novembre", "Décembre"])

domain = st.sidebar.selectbox("Domaine:",
                              ["All", "Physique", "Chimie", "Maths", "BioInformatique", "Science de la Terre",
                               "Intelligence Artificielle", "Générique", "Big Data", "Data science", "Informatique"])

st.sidebar.header("Temps d'attente")
boxplot_par = st.sidebar.selectbox("Paramètres",
                                   ["Minimum", "Premier quartile", "Médiane", "Moyenne", "Troisième quartile",
                                    "Maximum"])
fonc = st.sidebar.selectbox("En fonction de:", ["Nombre de cpus", "Partition"])

# Filter data
filtered_data = jobs_univ.copy()
if year != "All":
    filtered_data = filtered_data[filtered_data['Year'] == int(year)]
    if month and month != "All":
        monthdict = {"Janvier": 1, "Février": 2, "Mars": 3, "Avril": 4, "Mai": 5, "Juin": 6, "Juillet": 7, "Août": 8,
                     "Septembre": 9, "Octobre": 10, "Novembre": 11, "Décembre": 12}
        month_num = monthdict[month]
        filtered_data = filtered_data[filtered_data['Month'] == month_num]

if domain != "All":
    filtered_data = filtered_data[filtered_data['lib_domaine'] == domain]

with col[0]:
    total_jobs = filtered_data.shape[0]


    # function to display the card
    def display_card(State, Total):
        st.markdown(
            f"""
            <div style="padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h2 style="margin: 0;">Total jobs</h2>
                <div style="background-color: #333; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <h3 style="margin: 0;">{State}</h3>
                    <h1 style="margin: 0;">{Total}</h1>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # Example values (replace with actual logic to get the change)
    state = "Total Jobs"
    total = total_jobs  # Convert to millions

    # Display the card
    display_card(state, round(total, 1))

    # Total serial jobs:
    serial_jobs = filtered_data[filtered_data["NCPUS"] == 1]
    total_serial_jobs = serial_jobs.shape[0]


    # function to display the card
    def display_card(State, Total):
        st.markdown(
            f"""
            <div style="padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h2 style="margin: 0;">Total serial jobs</h2>
                <div style="background-color: #333; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <h3 style="margin: 0;">{State}</h3>
                    <h1 style="margin: 0;">{Total}</h1>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    state = "Total serial Jobs"
    total = total_serial_jobs  # Convert to millions
    # Example change in thousands

    # Display the card
    display_card(state, round(total, 1))

    # Total parallel jobs
    parallel_jobs = filtered_data[filtered_data["NCPUS"] > 1]
    total_parallel_jobs = parallel_jobs.shape[0]


    # function to display the card
    def display_card(State, Total):
        st.markdown(
            f"""
            <div style="padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h2 style="margin: 0;">Total parallel jobs</h2>
                <div style="background-color: #333; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <h3 style="margin: 0;">{State}</h3>
                    <h1 style="margin: 0;">{Total}</h1>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # Example values (replace with actual logic to get the change)
    state = "Total parallel Jobs"
    total = total_parallel_jobs

    # Display the card
    display_card(state, round(total, 1))

    completed_jobs = filtered_data[filtered_data["State"] == "COMPLETED"]
    total_completed_jobs = completed_jobs.shape[0]


# function to display the card
    def display_card(State, Total):
        st.markdown(
            f"""
            <div style="padding: 20px; border-radius: 10px; text-align: center; color: white;">
                <h2 style="margin: 0;">Total completed jobs</h2>
                <div style="background-color: #333; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <h3 style="margin: 0;">{State}</h3>
                    <h1 style="margin: 0;">{Total}</h1>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # Example values (replace with actual logic to get the change)
    state = "Total completed Jobs"
    total = total_completed_jobs

    # Display the card
    display_card(state, round(total, 1))

with col[1]:
    st.text("Server is ready for your input.")

    # Plot Jobs by universities
    if not filtered_data.empty:
        chart = alt.Chart(filtered_data).mark_bar().encode(
            x=alt.X('lib_universite', title='University'),
            y=alt.Y('count()', title='Number of Jobs'),
            color=alt.value('blue')
        ).properties(
            title=f"Number of Jobs in {year if year != 'All' else 'all years'} for {domain if domain != 'All' else 'all domains'} domain{f' in month {month}' if month and month != 'All' else ''}",
            width=700,
            height=400
        ).configure_title(
            fontSize=14,
            anchor='middle'
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )
        st.altair_chart(chart)
    else:
        st.text("No data available for the selected filters")

    # plots for wait time
    wt_data = waittime_boxp_ncpus.copy() if fonc == "Nombre de cpus" else waittime_boxp_par.copy()
    #
    foncdict = {
        "Nombre de cpus": "ncpus_category",
        "Partition": "Partition",
    }
    boxpdict = {
        "Minimum": 'Min',
        "Premier quartile": '1st_Qu.',
        "Médiane": 'Median',
        "Moyenne": 'Mean',
        "Troisième quartile": '3rd_Qu.',
        "Maximum": 'Max'
    }

    wt_data_melted = wt_data.melt(id_vars=[foncdict[fonc], 'Year'], value_vars=boxpdict[boxplot_par])

    chart2 = alt.Chart(wt_data_melted).mark_line(point=True).encode(
        x=alt.X(foncdict[fonc], title=fonc),
        y=alt.Y('value', title=boxplot_par),
        color='Year:N'
    ).properties(
        title=f"{boxplot_par} by {fonc}",
        width=700,
        height=400
    ).configure_title(
        fontSize=14,
        anchor='middle'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )
    st.altair_chart(chart2)

    jobs_per_domain = filtered_data['lib_domaine'].value_counts().reset_index()
    jobs_per_domain.columns = ['Domain', 'Number of Jobs']

    data = jobs_per_domain.to_dict(orient='list')

    # Create the HTML and JavaScript code for the donut chart
    chart_js = f"""
    <div>
    <canvas id="myDonutChart" width="400" height="400"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    var ctx = document.getElementById('myDonutChart').getContext('2d');
    var myDonutChart = new Chart(ctx, {{
        type: 'doughnut',
        data: {{
            labels: {data['Domain']},
            datasets: [{{
                data: {data['Number of Jobs']},
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }}]
        }},
        options: {{
            responsive: true,
            legend: {{
                position: 'bottom'
            }},
            plugins: {{
                tooltip: {{
                    callbacks: {{
                        label: function(context) {{
                            var label = context.label || '';
                            if (label) {{
                                label += ': ';
                            }}
                            if (context.raw !== null) {{
                                label += context.raw + ' jobs';
                            }}
                            return label;
                        }}
                    }}
                }}
            }}
        }}
    }});
    </script>
    </div>
    """

    # Display the JavaScript chart in Streamlit
    components.html(chart_js, height=600)

with col[2]:
    account_counts = filtered_data['Account'].value_counts().reset_index()
    account_counts.columns = ['Account', 'count']

    chart3 = alt.Chart(account_counts).mark_bar().encode(
        x=alt.X('Account', title='Type de compte'),
        y=alt.Y('count', title='Nombre de Jobs'),
        color=alt.value('pink')
    ).properties(
        title="Nombre de Jobs par Type de compte",
        width=400,
        height=400
    ).configure_title(
        fontSize=14,
        anchor='middle'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )
    st.altair_chart(chart3)


    partition_counts = filtered_data['Partition'].value_counts().reset_index()
    partition_counts.columns = ['Partition', 'count']

    chart4 = alt.Chart(partition_counts).mark_bar().encode(
        x=alt.X('Partition', title='Partition'),
        y=alt.Y('count', title='Nombre de Jobs'),
        color=alt.value('pink')
    ).properties(
        title="Nombre de Jobs par Partition",
        width=400,
        height=400
    ).configure_title(
        fontSize=14,
        anchor='middle'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    st.altair_chart(chart4)

    jobs_2023 = jobs_univ[jobs_univ['Year'] == 2023].groupby('Month').size().reset_index(name='Number_of_Jobs')

    chart5 = alt.Chart(jobs_2023).mark_line(point=True).encode(
        x=alt.X('Month', title='Month'),
        y=alt.Y('Number_of_Jobs', title='Number of Jobs'),
        color=alt.value('pink')
    ).properties(
        title="Number of Jobs Submitted Each Month during 2023",
        width=400,
        height=400
    ).configure_title(
        fontSize=14,
        anchor='middle'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    st.altair_chart(chart5)

    jobs_2024 = jobs_univ[jobs_univ['Year'] == 2024].groupby('Month').size().reset_index(name='Number_of_Jobs')
    chart6 = alt.Chart(jobs_2024).mark_line(point=True).encode(
        x=alt.X('Month', title='Month'),
        y=alt.Y('Number_of_Jobs', title='Number of Jobs'),
        color=alt.value('pink')
    ).properties(
        title="Number of Jobs Submitted Each Month during 2024",
        width=400,
        height=400
    ).configure_title(
        fontSize=14,
        anchor='middle'
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    )

    st.altair_chart(chart6)
