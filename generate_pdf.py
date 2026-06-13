import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Suppress headers/footers on the cover page
        if self._pageNumber == 1:
            # Draw beautiful cover page background elements
            self.setFillColor(colors.HexColor('#269683'))  # Primary teal
            self.rect(0, 750, 612, 42, fill=True, stroke=False)
            self.setFillColor(colors.HexColor('#4382dc'))  # Secondary blue
            self.rect(0, 0, 612, 18, fill=True, stroke=False)
            self.restoreState()
            return

        # Header
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor('#1b7a6a'))
        self.drawString(54, 756, "MEDLINK HOSPITAL SYSTEM")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#667671'))
        self.drawRightString(558, 756, "Project Documentation & Workspace Guide")
        
        # Header line
        self.setStrokeColor(colors.HexColor('#d1e9e5'))
        self.setLineWidth(0.5)
        self.line(54, 748, 558, 748)

        # Footer line
        self.line(54, 48, 558, 48)

        # Footer
        self.drawString(54, 34, "Confidential - For Internal Use Only")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 34, page_str)
        self.restoreState()

def create_pdf(filename):
    # Setup document
    # letter page is 612 x 792 pt
    # Printable area width = 612 - 2*36 = 540 pt
    # Printable area height = 792 - 2*54 = 684 pt
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Styles (using HexColors corresponding to the premium UI palette)
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=30,
        leading=36,
        textColor=colors.HexColor('#125146'),
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#4c5b57'),
        spaceAfter=30
    )
    
    metadata_style = ParagraphStyle(
        'CoverMetadata',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=14,
        textColor=colors.HexColor('#667671'),
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1b7a6a'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#275193'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'SectionBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor('#24312e'),
        spaceAfter=10
    )

    list_style = ParagraphStyle(
        'SectionList',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    story = []

    # ================= COVER PAGE =================
    story.append(Spacer(1, 150))
    story.append(Paragraph("MEDLINK", ParagraphStyle('CoverBrand', fontName='Helvetica-Bold', fontSize=14, leading=16, textColor=colors.HexColor('#269683'), spaceAfter=10)))
    story.append(Paragraph("AI-Powered Healthcare Prediction &<br/>Resource Management System", title_style))
    story.append(Paragraph("Complete Technical Documentation and Module Workspace Guide", subtitle_style))
    
    # Decorative divider
    story.append(Table(
        [['']], 
        colWidths=[540], 
        rowHeights=[4], 
        style=TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#269683')),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ])
    ))
    story.append(Spacer(1, 180))
    
    # Metadata footer
    metadata_text = """
    <b>Author:</b> Hospital Information Systems Development Team<br/>
    <b>Framework Stack:</b> FastAPI (Backend) & React + Vite + Tailwind (Frontend)<br/>
    <b>Deployment Stack:</b> Render (PaaS) & SQLite (Database)<br/>
    <b>Document Version:</b> 1.0.0 (Production Workspace Release)
    """
    story.append(Paragraph(metadata_text, metadata_style))
    story.append(PageBreak())

    # ================= SECTION 1: ARCHITECTURE OVERVIEW =================
    story.append(Paragraph("1. System Architecture & Tech Stack", h1_style))
    story.append(Paragraph(
        "Medlink is a command-grade, fully integrated healthcare management platform that operates as "
        "a dual-service system combining administrative control, clinical tools, operations optimization, "
        "and artificial intelligence. The system layout is structured as follows:",
        body_style
    ))
    
    arch_data = [
        ["Layer / Component", "Technology", "Role & Description"],
        ["Frontend UI", "React (JS), Vite, Tailwind CSS, Lucide Icons", "Delivers a responsive dashboard with a custom theme and glassmorphic card elements."],
        ["Backend REST API", "FastAPI (Python), Uvicorn", "Handles JWT authentication, resource scheduling, EHR CRUD, and routes data to ML models."],
        ["Database", "SQLite, SQLAlchemy ORM", "Stores clinical data, transaction logs, records, doctor profiles, and appointments."],
        ["AI Intelligence", "Scikit-Learn, XGBoost, Joblib", "Executes disease risk prediction, treatment path heuristics, and report analytics."]
    ]
    
    t = Table(arch_data, colWidths=[110, 130, 300])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2f3ef')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#125146')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c1e5dd')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Core Workspace Modules Overview", h2_style))
    story.append(Paragraph("&bull; <b>Overview / Command Dashboard:</b> Triage workspace showing registered volumes and live widgets.", list_style))
    story.append(Paragraph("&bull; <b>EHR Management Layer:</b> Prescriptions, medical records, allergies, and patient timelines.", list_style))
    story.append(Paragraph("&bull; <b>AI Intelligence Engine:</b> Machine learning diagnostics, outcome scoring, and report ingestion.", list_style))
    story.append(Paragraph("&bull; <b>Operations Intelligence Layer:</b> Bed allocations, ward tracking, and scheduling optimization.", list_style))
    story.append(Paragraph("&bull; <b>AI Assistant Dashboard:</b> Chat agents, knowledge bases, and executive-level analytics.", list_style))
    
    story.append(PageBreak())

    # Helper function for generating standard sections
    def add_section(title, image_path, explanation, features):
        sect_story = []
        sect_story.append(Paragraph(title, h1_style))
        
        # Display image
        if os.path.exists(image_path):
            # Printable width is 540pt, we use 480pt centered width
            # Image aspect ratio is 16:9, so height is 270pt
            img = Image(image_path, width=480, height=270)
            img.hAlign = 'CENTER'
            sect_story.append(img)
            sect_story.append(Spacer(1, 12))
        else:
            sect_story.append(Paragraph(f"<i>Image missing: {image_path}</i>", body_style))
            sect_story.append(Spacer(1, 10))

        sect_story.append(Paragraph("<b>Description & Workspace Ingestion:</b>", h2_style))
        sect_story.append(Paragraph(explanation, body_style))
        
        sect_story.append(Paragraph("<b>Key Dashboard Features:</b>", h2_style))
        for feat in features:
            sect_story.append(Paragraph(f"&bull; {feat}", list_style))
        
        sect_story.append(PageBreak())
        return sect_story

    # ================= SECTION 2: ADMIN COMMAND CENTER =================
    story.extend(add_section(
        "2. Admin Command Center Overview",
        "assets/admin_dashboard.png",
        "The Admin Overview acts as the operational headquarters of the Medlink system. It visualizes "
        "registered clinical volumes (patients, doctors, appointments) and streams platform status diagnostics. "
        "Integrated live widgets display operational velocity metrics and platform module distributions via Chart.js "
        "charts which have been customized to align with our premium design palette.",
        [
            "<b>Clinical Volume Statistics:</b> Shows live totals of patients, doctors, and schedules at a glance.",
            "<b>Operational Velocity Widget:</b> Bar charts tracing weekly hospital activity and intake rates.",
            "<b>Platform Distribution mix:</b> Doughnut chart visualizing the split between doctors, patients, and queue items.",
            "<b>Intake Queue:</b> An actionable live log of patient arrivals and routing requirements."
        ]
    ))

    # ================= SECTION 3: DOCTOR WORKSPACE =================
    story.extend(add_section(
        "3. Doctor Workspace & Clinical Dashboard",
        "assets/doctor_workspace.png",
        "The Doctor Workspace is tailored for practitioners. It offers a calm, clinical layout that highlights "
        "immediate priorities including pending, approved, and completed consultations. The dashboard is designed to "
        "reduce clinician cognitive load and simplify triage through clear visual indicators.",
        [
            "<b>Clinical Rhythm Panel:</b> Highlighted daily actions and priority follow-ups before the morning clinic.",
            "<b>Triage Metric Cards:</b> Quantifies daily waiting rooms, approved visits, and finalized files.",
            "<b>Live Appointment Queue:</b> Tracks incoming patient bookings for real-time consultation access."
        ]
    ))

    # ================= SECTION 4: PATIENT WORKSPACE =================
    story.extend(add_section(
        "4. Patient Profile & Command Center",
        "assets/patient_dashboard.png",
        "The Patient Dashboard serves as the central hub for patient interaction. It grants access to the "
        "appointment scheduler, prescription logs, lab uploads, and AI consultation tools, allowing patients to manage "
        "their healthcare files, tracking progress, and interact with the hospital staff directly.",
        [
            "<b>Clinical Record Quick Links:</b> Rapid links to EHR sheets, timelines, prescriptions, and vaccines.",
            "<b>Appointment Scheduler Widget:</b> Displays upcoming consultation dates and approved slots.",
            "<b>Self-service AI Assistant:</b> Access point for patient medical query assistance."
        ]
    ))

    # ================= SECTION 5: EHR MANAGEMENT LAYER =================
    story.extend(add_section(
        "5. Electronic Health Records (EHR) Hub",
        "assets/ehr_dashboard.png",
        "The Electronic Health Records (EHR) layer centralizes patients' medical documentation. Doctors "
        "and clinical staff can access records, input prescriptions with detailed medication line items, "
        "upload lab results, and review structured histories. The dashboard compiles these points into a timeline "
        "view for sequential tracking.",
        [
            "<b>Prescriptions and Line Items:</b> Details regarding dosage, frequency, and duration of medications.",
            "<b>Lab Report Repository:</b> Centralized storage and viewer for diagnostic files and reports.",
            "<b>Allergies and Vaccination Log:</b> Tracks patient histories to ensure safety in medication administration.",
            "<b>Chronological Patient Timeline:</b> A sequence showing visits, records, and clinical events."
        ]
    ))

    # ================= SECTION 6: AI INTELLIGENCE ENGINE =================
    story.extend(add_section(
        "6. AI Intelligence and Prediction Engine",
        "assets/ai_intelligence_dashboard.png",
        "The AI Intelligence Engine runs advanced diagnostics using python ML packages (Scikit-Learn & XGBoost). "
        "It generates disease risk scoring, predictive outcome metrics (such as readmission or length of stay), "
        "treatment plan recommendations, and automates report analysis via natural language ingestion.",
        [
            "<b>Disease Risk Predictor:</b> Generates probability metrics based on demographic and laboratory factors.",
            "<b>Outcome Prediction Model:</b> Forecasts hospital stay durations and readmission risks.",
            "<b>Treatment Optimization Heuristics:</b> Recommends treatment paths aligned with clinical guidelines.",
            "<b>Report Analyzer:</b> Parses uploaded diagnostic documents to extract critical health markers."
        ]
    ))

    # ================= SECTION 7: HOSPITAL OPERATIONS CENTER =================
    story.extend(add_section(
        "7. Hospital Operations Center",
        "assets/operations_dashboard.png",
        "The Operations Intelligence layer provides real-time logistics mapping. Administrators can trace bed "
        "allocations, monitor ward capacities, view resource inventories, check staff scheduling recommendations, "
        "and handle emergency signals from a command-grade unified console.",
        [
            "<b>Real-Time Bed Allocations:</b> Visual map of occupied and vacant beds across wards.",
            "<b>Ward Occupancy Ratios:</b> Live metrics tracking ICU, general, and specialty ward capacity.",
            "<b>Resource Optimization Alerts:</b> Flags inventory shortages and recommends restocking paths.",
            "<b>Emergency Alert System:</b> Broadcasts emergency signals and shifts staff schedules instantly."
        ]
    ))

    # ================= SECTION 8: AI ASSISTANT DASHBOARD =================
    story.extend(add_section(
        "8. AI Copilot & Assistant Console",
        "assets/ai_assistant_dashboard.png",
        "The AI Assistant Dashboard connects clinicians and managers to intelligence tools. It features a "
        "Doctor Copilot for research queries, Patient Assistant bots, a hospital Knowledge Base parser, and "
        "Executive Insights charts summarizing overall platform performance and diagnostic KPIs.",
        [
            "<b>Doctor Copilot:</b> Assists clinicians in researching complex drug interactions and guidelines.",
            "<b>Hospital Knowledge Base:</b> Searchable repository of hospital guidelines, policies, and files.",
            "<b>Executive Insights Widget:</b> Visualizes manager analytics and general performance metrics."
        ]
    ))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == '__main__':
    create_pdf('medlink_workspace_documentation.pdf')
    print("PDF Generation complete: medlink_workspace_documentation.pdf")
