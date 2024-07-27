import streamlit as st
import streamlit.components.v1 as components
import base64
import os
# Function to load and encode images
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return encoded_image

# Load and encode the images
image1_path = os.path.join("Screenshots", "Three_dots.png")
image2_path = os.path.join("Screenshots", "print.png")
image3_path = os.path.join("Screenshots", "print_interface.png")

image1_data = load_image(image1_path)
image2_data = load_image(image2_path)
image3_data = load_image(image3_path)

# FAQ Data
faq_data = [
    {
        "question": "What is the purpose of this dashboard?",
        "answer": "This dashboard provides a comprehensive analysis of job submissions and resource usage in the computing cluster. It helps users understand trends, optimize resource allocation, and improve performance."
    },
    {
        "question": "How do I navigate between different sections?",
        "answer": "Use the navigation buttons at the top right corner of the dashboard to switch between Home, About, and FAQ sections."
    },
    {
        "question": "How can I filter the data displayed?",
        "answer": "You can use the dropdown menus and date pickers provided in the sidebar to filter the data by year, month, domain, and other parameters."
    },
    {
        "question": "Can I download reports from the dashboard?",
        "answer": f"""
            Yes, you can download comprehensive reports in PDF format by clicking the three dots button available at the top right of the Home page.
            <br><br>
            Here are the steps:
            <br>
            <img src="data:image/png;base64,{image1_data}" alt="Step 1" style="width: 80%; margin-bottom: 20px;">
            <br>
            <img src="data:image/png;base64,{image2_data}" alt="Step 2" style="width: 80%; margin-bottom: 20px;">
            <br>
            <img src="data:image/png;base64,{image3_data}" alt="Step 3" style="width: 80%; margin-bottom: 20px;">
        """
    },
    {
        "question": "How do I interpret the job submission charts?",
        "answer": "The job submission charts show the number of jobs submitted over time or across different categories. Hover over the chart elements to see detailed information and use filters to customize the view."
    }
]

# HTML and JavaScript for the FAQ section
faq_html = """
<div style="color: white;">
    <h2>Frequently Asked Questions (FAQ)</h2>
    {faq_items}
</div>
<script>
function toggleAnswer(id) {{
    var answer = document.getElementById(id);
    if (answer.style.display === "none") {{
        answer.style.display = "block";
    }} else {{
        answer.style.display = "none";
    }}
}}
</script>
"""

# Generate HTML for each FAQ item
faq_items = ""
for i, faq in enumerate(faq_data):
    faq_items += f"""
    <div>
        <h3 style="color: white; cursor: pointer;" onclick="toggleAnswer('answer{i}')">{faq['question']}</h3>
        <p id="answer{i}" style="display:none; color: white;">{faq['answer']}</p>
    </div>
    """

# Combine HTML parts
faq_html = faq_html.format(faq_items=faq_items)

# Embed the FAQ section in Streamlit
components.html(faq_html, height=3000)

