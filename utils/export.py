"""
CarbonSnap – PDF/PNG Report Exporter using ReportLab.
"""
import io
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.colors import HexColor
import pandas as pd


# Colour palette
GREEN_DARK = HexColor("#16a34a")
GREEN_LIGHT = HexColor("#bbf7d0")
DARK_BG = HexColor("#1e293b")
SLATE = HexColor("#475569")
WHITE = colors.white
AMBER = HexColor("#f59e0b")


def export_report(df: pd.DataFrame, total: float, badges: set = None,
                  city: str = "India", user_name: str = "CarbonSnapper") -> bytes:
    """
    Generate a PDF report and return as bytes.

    Parameters
    ----------
    df        : breakdown DataFrame from calculate_footprint()
    total     : total kg CO₂e
    badges    : set of awarded badge keys
    city      : user's city string
    user_name : display name
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
        leftMargin=1.5*cm, rightMargin=1.5*cm
    )
    styles = getSampleStyleSheet()
    story = []

    # ── Header ──────────────────────────────────────────────────────────────
    header_style = ParagraphStyle(
        "Header", fontSize=28, textColor=GREEN_DARK,
        fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4
    )
    sub_style = ParagraphStyle(
        "Sub", fontSize=12, textColor=SLATE,
        fontName="Helvetica", alignment=TA_CENTER, spaceAfter=16
    )
    story.append(Paragraph("🌿 CarbonSnap Report", header_style))
    story.append(Paragraph(
        f"{user_name} · {date.today().strftime('%d %B %Y')} · {city}",
        sub_style
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=GREEN_DARK, spaceAfter=12))

    # ── Summary Card ────────────────────────────────────────────────────────
    rating = _get_rating(total)
    summary_data = [
        ["Metric", "Value"],
        ["Daily Footprint", f"{total:.2f} kg CO₂e"],
        ["vs India Avg (4 kg)", f"{_pct_vs(total, 4.0)}"],
        ["vs Paris Target (2.5 kg)", f"{_pct_vs(total, 2.5)}"],
        ["Carbon Rating", rating],
        ["Report Date", date.today().strftime("%d %b %Y")],
    ]
    summary_table = Table(summary_data, colWidths=[8*cm, 8*cm])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN_DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 11),
        ("BACKGROUND", (0, 1), (-1, -1), GREEN_LIGHT),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, GREEN_LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.5, SLATE),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 16))

    # ── Category Breakdown ──────────────────────────────────────────────────
    if not df.empty:
        story.append(Paragraph("📊 Category Breakdown", ParagraphStyle(
            "SectionHeader", fontSize=14, textColor=DARK_BG,
            fontName="Helvetica-Bold", spaceAfter=8
        )))

        cat_df = df.groupby("Category")["kg_CO2e"].sum().reset_index()
        table_data = [["Category", "kg CO₂e", "% of Total"]]
        for _, row in cat_df.iterrows():
            pct = (row["kg_CO2e"] / total * 100) if total > 0 else 0
            table_data.append([
                row["Category"],
                f"{row['kg_CO2e']:.3f}",
                f"{pct:.1f}%",
            ])

        cat_table = Table(table_data, colWidths=[7*cm, 5*cm, 4*cm])
        cat_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, HexColor("#f1f5f9")]),
            ("GRID", (0, 0), (-1, -1), 0.5, SLATE),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        story.append(cat_table)
        story.append(Spacer(1, 16))

        # Subcategory detail
        story.append(Paragraph("🔍 Detailed Breakdown", ParagraphStyle(
            "SectionHeader", fontSize=14, textColor=DARK_BG,
            fontName="Helvetica-Bold", spaceAfter=8
        )))
        detail_data = [["Category", "Item", "Value", "Factor", "kg CO₂e"]]
        for _, row in df.sort_values("kg_CO2e", ascending=False).iterrows():
            detail_data.append([
                row["Category"],
                f"{row.get('emoji','')} {row['Subcategory']}",
                f"{row['Value']} {row['Unit']}",
                f"×{row['Factor']}",
                f"{row['kg_CO2e']:.4f}",
            ])
        detail_table = Table(detail_data, colWidths=[3.5*cm, 5*cm, 2.5*cm, 2*cm, 3*cm])
        detail_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), DARK_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, HexColor("#f1f5f9")]),
            ("GRID", (0, 0), (-1, -1), 0.3, SLATE),
            ("ALIGN", (2, 1), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(detail_table)

    # ── Badges ──────────────────────────────────────────────────────────────
    if badges:
        story.append(Spacer(1, 16))
        story.append(Paragraph("🏆 Achievements Unlocked", ParagraphStyle(
            "SectionHeader", fontSize=14, textColor=DARK_BG,
            fontName="Helvetica-Bold", spaceAfter=8
        )))
        from utils.badges import BADGE_CATALOGUE
        badge_text = "  ".join(
            f"{BADGE_CATALOGUE[b]['emoji']} {BADGE_CATALOGUE[b]['title']}"
            for b in badges if b in BADGE_CATALOGUE
        )
        story.append(Paragraph(badge_text, ParagraphStyle(
            "Badges", fontSize=11, textColor=SLATE, fontName="Helvetica", spaceAfter=8
        )))

    # ── Footer ──────────────────────────────────────────────────────────────
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=GREEN_DARK, spaceBefore=8))
    story.append(Paragraph(
        "Generated by 🌿 CarbonSnap · EcoHack 2025 · India-specific emission factors",
        ParagraphStyle("Footer", fontSize=8, textColor=SLATE,
                       fontName="Helvetica-Oblique", alignment=TA_CENTER)
    ))

    doc.build(story)
    return buffer.getvalue()


def _pct_vs(user: float, ref: float) -> str:
    if ref == 0:
        return "N/A"
    p = (user - ref) / ref * 100
    arrow = "↓" if p < 0 else "↑"
    return f"{arrow} {abs(p):.1f}%"


def _get_rating(total: float) -> str:
    if total <= 2.0:
        return "A+ 🌿 Eco Champion"
    elif total <= 3.5:
        return "A 🌱 Green Warrior"
    elif total <= 5.0:
        return "B 🌍 Average"
    elif total <= 7.0:
        return "C ⚠️ High Emitter"
    else:
        return "D 🔥 Carbon Heavy"
