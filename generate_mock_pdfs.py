import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def build_pdf_resume(filename, name, skills_list, experience_text):
    # Ensure docs directory exists
    os.makedirs("docs", exist_ok=True)
    filepath = os.path.join("docs", filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, 750, f"RESUME: {name}")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 710, "Core Technical Skills:")
    
    c.setFont("Helvetica", 12)
    y_pos = 690
    for skill in skills_list:
        c.drawString(70, y_pos, f"- {skill}")
        y_pos -= 20
        
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_pos - 10, "Professional Experience:")
    c.setFont("Helvetica", 12)
    c.drawString(50, y_pos - 30, experience_text)
    
    c.save()
    print(f"📄 Generated actual PDF resume: {filepath}")

# Generate 2 highly customized profiles for verification
build_pdf_resume(
    filename="resume_vishal.pdf",
    name="Vishal Gangwar",
    skills_list=["Kotlin", "Android Studio", "MVVM", "XML", "Java", "Git"],
    experience_text="Built multiple Android apps utilizing View Binding and clean design layouts."
)

build_pdf_resume(
    filename="resume_rohit.pdf",
    name="Rohit Kumar",
    skills_list=["Python", "Django", "SQL", "HTML", "CSS", "AWS"],
    experience_text="Experienced backend engineer focused on cloud APIs and system integrations."
)