import streamlit as st


def show_about():

    st.markdown("""
    # About Our Dashboard

    Welcome to MARWAN HPC Cluster Job Analysis Dashboard!

    This dashboard provides a comprehensive analysis of job submissions in MARWAN HPC cluster. Here you can explore various aspects of the cluster usage, job distributions, and performance metrics to gain valuable insights. 
    ## MARWAN HPC information
    
    The MARWAN network is the National Education and Research Network created in 1998. Currently, it is in its fifth version (MARWAN 5).
    MARWAN 5 consists of a national infrastructure using an MPLS/L2 backbone. Today, MARWAN interconnects all the networks of educational and research institutions in Morocco through an IP service. The institutions are connected via circuits such as VPN/LL Layer 2 Leased Line connections.
    Important characteristics of MARWAN are:
    - More than 250 connected institutions over 140 links covering all Moroccan territory
    - Offered bandwidth ranges from 100Mbps to 5Gbps
    - Total access bandwidth : 96 Gbps
    - MARWAN is connected to the Internet via 2 links of 12Gbps each in Rabat and Casablanca
    - MARWAN is connected to European Network GÉANT with 1Gbps link from Rabat to London
    - All links are in Fiber Optic
    - MARWAN is based on SD-WAN
    - IPv6 is deployed natively in Dual Stack
    - IP multicast support
    - 
    ## Key Features

    - **Job Submissions Overview:**
      - Visualize the number of jobs submitted over different periods (year, month).
      - Analyze job submissions by various universities and account types.

    - **Domain-Specific Analysis:**
      - Explore the distribution of jobs across different domains such as Data Science, Bioinformatics, Physics, etc.
      - Identify trends and patterns in job submissions within each domain.

    - **Performance Metrics:**
      - Compare waiting times for jobs across different years.
      - Assess the usage of computing resources like CPUs across various jobs.

    ## How to Use the Dashboard

    1. **Navigation:**
       - Use the buttons at the top right corner to navigate between different sections of the dashboard (Home, About, FAQ).

    2. **Interactive Charts:**
       - Hover over the charts to see detailed information.
       - Use the filters to customize the data view based on your specific needs.

    3. **Download Reports:**
       - Generate and download comprehensive reports in PDF format for offline analysis.

    ## About Us

    We are a dedicated team focused on delivering the best tools to help our users understand and optimize their usage of our computing cluster. Our goal is to provide clear, actionable insights through an intuitive and interactive interface.

    ## Contact Us

    If you have any questions or feedback, please feel free to reach out to us at support@example.com. We are here to help you make the most of our dashboard.

    ---

    Thank you for using our Cluster Job Analysis Dashboard!
    """)
show_about()
