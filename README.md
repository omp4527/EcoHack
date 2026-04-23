# 🌿 CarbonSnap – Personal Carbon Footprint Tracker

> **EcoHack 2025** | Climate & Energy Theme | India-Specific | Fully Gamified

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Quick Start

```bash
# 1. Clone / navigate to project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📱 Features

| Feature | Description |
|---------|-------------|
| 📊 **Live Calculator** | Real-time footprint from transport, energy, food & waste |
| 🇮🇳 **India Factors** | Car: 0.25kg/km, Electricity: 0.75kg/kWh (grid 2024) |
| 🥧 **Plotly Charts** | Interactive pie, bar, area & forecast charts |
| 🏆 **Badge System** | 14 badges with XP · Streak tracking · Level-up system |
| ⚔️ **Challenges** | 8 gamified quests ("No Beef Week", "Car-Free Week"…) |
| 📈 **7-Day Forecast** | Trend projection + 5% reduction scenario overlay |
| 📄 **PDF Export** | Full ReportLab report with breakdown & badges |
| 📲 **Share** | WhatsApp & Twitter deep links |
| 🌙 **Dark/Light** | Toggle in sidebar |
| 📱 **Responsive** | Mobile-friendly via Streamlit |

---

## 🏗️ Project Structure

```
EcoHack/
├── app.py                    # 🏠 Main entry point (4 tabs)
├── requirements.txt
├── pages/
│   ├── dashboard.py         # 🏠 Dashboard + metrics + charts + tips
│   ├── tracker.py           # 📅 History + trend charts + CSV export
│   ├── challenges.py        # ⚔️ Gamified quests
│   └── profile.py           # 👤 Badges + yearly stats + gauge
└── utils/
    ├── calculations.py      # Core emission math engine
    ├── tips.py              # Context-aware tip generator
    ├── badges.py            # Achievement system
    ├── forecast.py          # Weekly/yearly projection
    ├── comparison.py        # City/country benchmarks
    ├── export.py            # PDF report generator
    ├── storage.py           # Session-state history
    ├── charts.py            # Plotly chart builder
    └── styles.py            # CSS injection + HTML components
```

---

## 🇮🇳 Emission Factors (India-Specific)

| Source | Factor |
|--------|--------|
| Car (Petrol) | 0.25 kg/km |
| Car (Diesel) | 0.27 kg/km |
| Two-Wheeler | 0.113 kg/km |
| Bus | 0.089 kg/km |
| Metro/Train | 0.031 kg/km |
| Electricity | **0.75 kg/kWh** (India grid 2024) |
| LPG | 2.983 kg/kg |
| Beef | 27.0 kg/kg consumed |
| Chicken | 6.9 kg/kg |
| Rice | 2.7 kg/kg |

---

## 🏆 Badges

| Badge | Condition |
|-------|-----------|
| 🌍 Carbon Tracker | First calculation |
| 🌱 Below Average | Daily < 4 kg (India avg) |
| 🥇 Eco Champion | Daily ≤ 2 kg |
| 🔥 Green Streak | 3 days tracked |
| 🌿 Week Warrior | 7-day streak |
| 🏆 Eco Hero | 30-day streak |
| 🚗 No-Car Day | Zero transport emissions |
| 🥗 Plant Power | Zero animal product food |
| ♻️ Zero Waster | Zero landfill waste |
| ☀️ Sun Powered | Electricity < 0.5 kWh |
| 📉 10% Reducer | Cut weekly avg by 10% |
| 📊 20% Reducer | Cut weekly avg by 20% |
| 📤 Eco Ambassador | Shared a report |

---

## 🌍 Demo Flow (Hackathon Presentation)

1. Open app → loads in **< 1 second**
2. Click **🎭 Load Demo Data** → instantly seeds 14-day history
3. Point to **Dashboard** → show live pie chart + forecast + tips
4. Navigate to **⚔️ Challenges** → start "No Beef Week"
5. Navigate to **👤 Profile** → show badge wall + gauge vs Paris target
6. Hit **📄 Download PDF** → export polished report
7. Hit **📲 Share on WhatsApp** → social sharing demo

---

## 📦 Dependencies

```
streamlit>=1.32.0
plotly>=5.20.0
pandas>=2.2.0
reportlab>=4.1.0
Pillow>=10.3.0
numpy>=1.26.0
kaleido>=0.2.1
```

---

*Built with ❤️ for EcoHack 2025 | MIT-ALANDI*
