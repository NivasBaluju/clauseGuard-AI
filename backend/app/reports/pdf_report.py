import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)

DISCLAIMER_TEXT = (
    "ClauseGuard AI provides automated, non-expert analysis for informational purposes only. "
    "It is not legal advice. Consult a qualified attorney for decisions with legal consequences."
)

def generate_pdf_report(document, clauses, missing_clauses, deadlines, pii_findings) -> bytes:
    """
    Generates a professional, print-ready PDF analysis report for a document using ReportLab.
    Includes overall score, risk bands, per-clause findings, missing clauses, deadlines,
    PII summary, and the mandatory permanent non-legal-advice disclaimer.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#000000"),
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#666666"),
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#111827"),
        spaceBefore=14,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1F2937"),
    )
    body_bold = ParagraphStyle(
        "ReportBodyBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1F2937"),
    )
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#B91C1C"),
    )

    elements = []

    elements.append(Paragraph("ClauseGuard AI — Risk Analysis Report", title_style))
    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')} | Document ID: {document.id}",
            subtitle_style,
        )
    )
    elements.append(Spacer(1, 10))

    disclaimer_table = Table(
        [[Paragraph(f"<b>LEGAL NOTICE:</b> {DISCLAIMER_TEXT}", disclaimer_style)]],
        colWidths=[540],
    )
    disclaimer_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FEF2F2")),
            ("BORDER", (0, 0), (-1, -1), 1, colors.HexColor("#FCA5A5")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])
    )
    elements.append(disclaimer_table)
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("1. Document Overview & Executive Summary", section_heading))
    
    band_colors = {
        "low": colors.HexColor("#15803D"),
        "medium": colors.HexColor("#B45309"),
        "high": colors.HexColor("#C2410C"),
        "critical": colors.HexColor("#B91C1C"),
    }
    score_color = band_colors.get(document.risk_band, colors.HexColor("#B91C1C"))

    score_text = f"<b>{document.overall_risk_score} / 100</b> ({document.risk_band.upper() if document.risk_band else 'N/A'})"
    
    overview_data = [
        [Paragraph("<b>Filename:</b>", body_style), Paragraph(document.filename, body_style),
         Paragraph("<b>Overall Risk Score:</b>", body_style), Paragraph(score_text, ParagraphStyle("Score", parent=body_style, textColor=score_color))],
        [Paragraph("<b>Document Type:</b>", body_style), Paragraph(document.document_type.replace('_', ' ').title(), body_style),
         Paragraph("<b>Pages:</b>", body_style), Paragraph(str(document.page_count or 1), body_style)],
        [Paragraph("<b>Model Version:</b>", body_style), Paragraph(document.model_version or "N/A", body_style),
         Paragraph("<b>Analyzed At:</b>", body_style), Paragraph(document.analyzed_at.strftime('%Y-%m-%d %H:%M') if document.analyzed_at else "N/A", body_style)],
    ]

    overview_table = Table(overview_data, colWidths=[100, 170, 110, 160])
    overview_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F9FAFB")),
            ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#F9FAFB")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ])
    )
    elements.append(overview_table)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("2. Privacy & PII Redaction Summary", section_heading))
    pii_counts = {}
    for p in pii_findings:
        pii_counts[p.entity_type] = pii_counts.get(p.entity_type, 0) + 1

    if pii_counts:
        pii_rows = [[Paragraph("<b>Redacted Entity Type</b>", body_bold), Paragraph("<b>Count Detected</b>", body_bold)]]
        for ent, count in sorted(pii_counts.items()):
            pii_rows.append([Paragraph(ent, body_style), Paragraph(str(count), body_style)])
        pii_table = Table(pii_rows, colWidths=[270, 270])
        pii_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ])
        )
        elements.append(pii_table)
    else:
        elements.append(Paragraph("No sensitive personal identification items detected for redaction.", body_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("3. Expected but Missing Clauses", section_heading))
    if missing_clauses:
        m_rows = [[Paragraph("<b>Clause Type</b>", body_bold), Paragraph("<b>Severity</b>", body_bold), Paragraph("<b>Standard Protection Note</b>", body_bold)]]
        for m in missing_clauses:
            sev_color = colors.HexColor("#B91C1C") if m.severity == "high" else (colors.HexColor("#B45309") if m.severity == "medium" else colors.HexColor("#15803D"))
            m_rows.append([
                Paragraph(m.clause_type.replace('_', ' ').title(), body_style),
                Paragraph(f"<b>{m.severity.upper()}</b>", ParagraphStyle("Sev", parent=body_style, textColor=sev_color)),
                Paragraph(m.checklist_note or "Expected standard provision.", body_style),
            ])
        m_table = Table(m_rows, colWidths=[140, 70, 330])
        m_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ])
        )
        elements.append(m_table)
    else:
        elements.append(Paragraph("All standard expected clauses for this document type were identified.", body_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("4. Deadlines & Date-Bound Obligations", section_heading))
    if deadlines:
        dl_rows = [[
            Paragraph("<b>Type</b>", body_bold),
            Paragraph("<b>Target Clause Text / Timeline</b>", body_bold),
            Paragraph("<b>Relative Days</b>", body_bold),
            Paragraph("<b>Confidence</b>", body_bold),
        ]]
        for dl in deadlines:
            conf_text = "CONFIDENT" if dl.confidence == "confident" else "NEEDS REVIEW"
            conf_color = colors.HexColor("#15803D") if dl.confidence == "confident" else colors.HexColor("#B45309")
            dl_rows.append([
                Paragraph(dl.deadline_type.replace('_', ' ').title() if dl.deadline_type else "Other", body_style),
                Paragraph(dl.raw_text[:180], body_style),
                Paragraph(f"{dl.relative_days} days" if dl.relative_days else (dl.parsed_date.strftime('%Y-%m-%d') if dl.parsed_date else "N/A"), body_style),
                Paragraph(f"<b>{conf_text}</b>", ParagraphStyle("Conf", parent=body_style, textColor=conf_color)),
            ])
        dl_table = Table(dl_rows, colWidths=[110, 270, 80, 80])
        dl_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F3F4F6")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E5E7EB")),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ])
        )
        elements.append(dl_table)
    else:
        elements.append(Paragraph("No time-sensitive deadlines or relative notice obligations detected.", body_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("5. Detailed Clause-by-Clause Risk Breakdown", section_heading))
    for c in clauses:
        fav_label = (c.favorability_label or "fair").upper()
        fav_color = colors.HexColor("#15803D") if fav_label == "FAIR" else (colors.HexColor("#B45309") if fav_label == "NEEDS_REVIEW" else colors.HexColor("#B91C1C"))
        
        c_header = (
            f"<b>Clause {c.clause_index + 1}: {c.clause_type.replace('_', ' ').title() if c.clause_type else 'Unclassified'}</b> "
            f"| Risk Score: <b>{c.risk_score}</b> | Favorability: <font color='{fav_color.hexval()}'><b>{fav_label}</b></font>"
        )
        if c.favorability_label == "needs_review":
            c_header += " <font color='#B45309'>[FLAGGED FOR HUMAN REVIEW]</font>"

        clause_block = [
            Paragraph(c_header, body_bold),
            Spacer(1, 3),
            Paragraph(c.redacted_text, body_style),
            Spacer(1, 6),
            HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5E7EB"), spaceBefore=2, spaceAfter=6),
        ]
        elements.append(KeepTogether(clause_block))

    elements.append(Spacer(1, 10))
    elements.append(disclaimer_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
