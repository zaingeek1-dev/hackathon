import sys
import requests
import math
from datetime import datetime, date, timezone
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)

NASA_API_BASE = 'https://api.nasa.gov/neo/rest/v1'
API_KEY = 'lr86Sx6eyQXbNm32gmmPAuHzzJeXTIfUdzcTjiGB'



def fetch_neo_by_reference_id(reference_id):
    """Fetch detailed NEO data from NASA API"""
    url = f"{NASA_API_BASE}/neo/{reference_id}"
    params = {'api_key': API_KEY}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def calculate_mass(diameter_m, density=3000):
    """Calculate asteroid mass assuming spherical shape"""
    radius = diameter_m / 2
    volume = (4 / 3) * math.pi * radius ** 3
    return volume * density


def calculate_kinetic_energy(mass_kg, velocity_ms):
    """Calculate kinetic energy in Joules"""
    return 0.5 * mass_kg * velocity_ms ** 2


def tnt_equivalent(energy_joules):
    """Convert energy to TNT equivalent"""
    tnt_energy = 4.184e6  # J per kg TNT
    return energy_joules / tnt_energy


def crater_diameter(energy_joules, target_density=2500, gravity=9.81):
    """Estimate crater diameter using scaling laws"""
    scaling_factor = 1.8
    return scaling_factor * (energy_joules / (target_density * gravity)) ** (1 / 3.4)


def seismic_magnitude(energy_joules):
    """Convert impact energy to equivalent earthquake magnitude"""
    if energy_joules <= 0:
        return 0
    log_energy = math.log10(energy_joules)
    return (log_energy - 5.24) / 1.44


def risk_assessment(diameter_m, miss_distance_km):
    """Provide risk assessment based on size and approach"""
    if diameter_m < 50:
        size_risk = "Low - Likely atmospheric breakup"
    elif diameter_m < 140:
        size_risk = "Moderate - Regional damage potential"
    elif diameter_m < 1000:
        size_risk = "High - Continental effects possible"
    else:
        size_risk = "Extreme - Global catastrophe potential"

    if miss_distance_km < 100000:
        approach_risk = "CRITICAL - Extremely close approach"
    elif miss_distance_km < 1000000:
        approach_risk = "HIGH - Close monitoring required"
    elif miss_distance_km < 7500000:  # Moon's distance
        approach_risk = "MODERATE - Within lunar distance"
    else:
        approach_risk = "LOW - Safe distance"

    return size_risk, approach_risk


def estimate_casualties(diameter_m, impact_location="urban"):
    """Rough casualty estimates based on diameter and location"""
    if diameter_m < 20:
        return "Hundreds to thousands (mostly injuries)" if impact_location == "urban" else "Minimal"
    elif diameter_m < 100:
        return "Thousands to tens of thousands" if impact_location == "urban" else "Hundreds to thousands"
    elif diameter_m < 500:
        return "Hundreds of thousands to millions" if impact_location == "urban" else "Tens of thousands"
    else:
        return "Millions to tens of millions" if impact_location == "urban" else "Hundreds of thousands"


def economic_damage_estimate(diameter_m):
    """Rough economic damage estimates in billions USD"""
    if diameter_m < 50:
        return "0.1 - 1 billion USD"
    elif diameter_m < 140:
        return "1 - 50 billion USD"
    elif diameter_m < 500:
        return "50 - 1,000 billion USD"
    else:
        return "1,000+ billion USD (potential civilization impact)"


def parse_approach_date(approach):
    """Safely parse the close approach date string into a datetime.date object."""
    try:
        return datetime.strptime(approach.get('close_approach_date', ''), '%Y-%m-%d').date()
    except Exception:
        return None


def get_historical_approaches(approaches):
    """Filters and returns the last 5 close approaches before today (UTC)"""
    today = datetime.now(timezone.utc).date()
    past_approaches = [
        a for a in approaches
        if (date_obj := parse_approach_date(a)) is not None and date_obj < today
    ]
    past_approaches.sort(key=lambda x: parse_approach_date(x) or date.min, reverse=True)
    return past_approaches[:5]


class NEOAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NASA NEO Comprehensive Analysis")
        self.setGeometry(300, 300, 900, 750)

        self.input_field = None
        self.fetch_button = None
        self.output_area = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        label = QLabel("Enter NASA NEO Reference ID:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("e.g. 2001865 (Eros), 2001036 (Ganymed)")
        self.fetch_button = QPushButton("Fetch and Analyze")
        self.fetch_button.clicked.connect(self.on_fetch_clicked)

        input_layout.addWidget(label)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.fetch_button)

        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("font-family: monospace; font-size: 11pt;")

        layout.addLayout(input_layout)
        layout.addWidget(self.output_area)
        self.setLayout(layout)
        self.output_area.setText("  NASA NEO COMPREHENSIVE ANALYSIS TOOL\n"
                                 "Enter an asteroid reference ID and click 'Fetch and Analyze' to get a detailed report.")

    def on_fetch_clicked(self):
        ref_id = self.input_field.text().strip()
        if not ref_id:
            QMessageBox.warning(self, "Input Error", "Please enter a valid NASA NEO Reference ID.")
            return

        self.output_area.clear()
        self.output_area.append(f"  Fetching data for NEO ID: {ref_id}...\n")

        self.fetch_button.setEnabled(False)
        QApplication.processEvents()

        try:
            neo_data = fetch_neo_by_reference_id(ref_id)
            analysis_text = NEOAnalyzerApp.generate_comprehensive_analysis_text(neo_data)
            self.output_area.append(analysis_text)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                self.output_area.append(f"  NEO with ID '{ref_id}' not found in NASA database.\n"
                                        "Try these example IDs: 99942 (Apophis), 2000433 (Eros)")
            else:
                self.output_area.append(f"  HTTP Error: {e.response.status_code} - {e}")
        except requests.RequestException as e:
            self.output_area.append(f"  Connection Error: Failed to reach NASA API. Check internet connection. Error: {e}")
        except Exception as e:
            self.output_area.append(f"  An unexpected error occurred: {e}")
        finally:
            self.fetch_button.setEnabled(True)

    @staticmethod
    def generate_comprehensive_analysis_text(neo):
        lines = []
        now_utc = datetime.now(timezone.utc)
        today = now_utc.date()

        lines.append("=" * 80)
        lines.append(f"COMPREHENSIVE ASTEROID ASSESSMENT: {neo.get('name')}")
        lines.append("=" * 80)

        lines.append("\n  BASIC INFORMATION")
        lines.append("-" * 40)
        lines.append(f"NASA Reference ID: {neo.get('neo_reference_id')}")
        lines.append(f"Full Name: {neo.get('name')}")
        lines.append(f"Designation: {neo.get('designation', 'N/A')}")
        lines.append(f"Discovery: First observed {neo.get('orbital_data', {}).get('first_observation_date', 'Unknown')}")
        lines.append(f"Last observed: {neo.get('orbital_data', {}).get('last_observation_date', 'Unknown')}")
        lines.append(f"Data arc: {neo.get('orbital_data', {}).get('data_arc_in_days', 'Unknown')} days")
        lines.append(f"Observations used: {neo.get('orbital_data', {}).get('observations_used', 'Unknown')}")

        lines.append("\n  PHYSICAL CHARACTERISTICS")
        lines.append("-" * 40)
        diam = neo.get('estimated_diameter', {}).get('meters', {})
        diameter_min = diam.get('estimated_diameter_min', 0)
        diameter_max = diam.get('estimated_diameter_max', 0)
        diameter_avg = (diameter_min + diameter_max) / 2
        lines.append(f"Estimated diameter: {diameter_min:.1f} - {diameter_max:.1f} meters")
        lines.append(f"Average diameter: {diameter_avg:.1f} meters")
        lines.append(f"Absolute magnitude (H): {neo.get('absolute_magnitude_h', 'Unknown')}")
        lines.append(f"Estimated mass: {calculate_mass(diameter_avg):.2e} kg")

        lines.append("\n  HAZARD ASSESSMENT")
        lines.append("-" * 40)
        hazardous = neo.get('is_potentially_hazardous_asteroid', False)
        lines.append(f"Potentially Hazardous Asteroid (PHA): {'YES' if hazardous else 'NO'}")
        if hazardous:
            lines.append("  This object meets NASA criteria for enhanced monitoring:")
            lines.append("  - Approaches within 7.5 million km of Earth")
            lines.append("  - Estimated diameter > 140 meters")

        lines.append("\n  ORBITAL CHARACTERISTICS")
        lines.append("-" * 40)
        orbital_data = neo.get('orbital_data', {})
        lines.append(f"Semi-major axis: {orbital_data.get('semi_major_axis', 'Unknown')} AU")
        lines.append(f"Eccentricity: {orbital_data.get('eccentricity', 'Unknown')}")
        lines.append(f"Inclination: {orbital_data.get('inclination', 'Unknown')}°")
        lines.append(f"Orbital period: {orbital_data.get('orbital_period', 'Unknown')} days")
        lines.append(f"Perihelion distance: {orbital_data.get('perihelion_distance', 'Unknown')} AU")
        lines.append(f"Aphelion distance: {orbital_data.get('aphelion_distance', 'Unknown')} AU")

        orbit_class = orbital_data.get('orbit_class', {})
        lines.append(f"Orbit class: {orbit_class.get('orbit_class_type', 'Unknown')} - {orbit_class.get('orbit_class_description', 'Unknown')}")

        lines.append("\n  CLOSE APPROACH HISTORY & FUTURE")
        lines.append("-" * 40)
        approaches = neo.get('close_approach_data', [])

        if approaches:
            lines.append(f"Total recorded close approaches: {len(approaches)}")

            closest_approach = min(approaches, key=lambda x: float(x.get('miss_distance', {}).get('kilometers', float('inf'))))
            closest_distance = float(closest_approach.get('miss_distance', {}).get('kilometers', 0))
            closest_date = closest_approach.get('close_approach_date', 'Unknown')

            lines.append(f"Current Reference Date: {now_utc.strftime('%Y-%m-%d')} (UTC)")
            lines.append(f"Closest recorded approach: {closest_date}")
            lines.append(f"Closest distance: {closest_distance:,.0f} km ({closest_distance / 384400:.2f} lunar distances)")

            historical_approaches = get_historical_approaches(approaches)
            if historical_approaches:
                lines.append("\nLast 5 Historical Approaches:")
                for approach in historical_approaches:
                    date_str = approach.get('close_approach_date')
                    distance = float(approach.get('miss_distance', {}).get('kilometers', 0))
                    velocity = approach.get('relative_velocity', {}).get('kilometers_per_second', 'N/A')
                    lines.append(f"  {date_str}: {distance:,.0f} km, {velocity} km/s")

            upcoming_approaches = [a for a in approaches if (date_obj := parse_approach_date(a)) is not None and date_obj > today]
            if upcoming_approaches:
                lines.append(f"\nUpcoming approaches: {len(upcoming_approaches)}")
                for approach in upcoming_approaches[:5]:
                    date_str = approach.get('close_approach_date')
                    distance = float(approach.get('miss_distance', {}).get('kilometers', 0))
                    velocity = approach.get('relative_velocity', {}).get('kilometers_per_second', 'N/A')
                    lines.append(f"  {date_str}: {distance:,.0f} km, {velocity} km/s")

            if closest_distance < 10000000:
                size_risk, approach_risk = risk_assessment(diameter_avg, closest_distance)
                lines.append("\n  RISK ANALYSIS")
                lines.append("-" * 40)
                lines.append(f"Size-based risk: {size_risk}")
                lines.append(f"Approach risk: {approach_risk}")

        lines.append("\n  HYPOTHETICAL IMPACT ANALYSIS")
        lines.append("-" * 40)
        lines.append("  NOTE: This is a theoretical analysis for educational purposes")

        impact_velocity_ms = 20000
        mass_kg = calculate_mass(diameter_avg)
        energy_j = calculate_kinetic_energy(mass_kg, impact_velocity_ms)
        tnt_kg = tnt_equivalent(energy_j)
        crater_d = crater_diameter(energy_j)
        eq_magnitude = seismic_magnitude(energy_j)

        lines.append(f"Assumed impact velocity: 20 km/s (typical)")
        lines.append(f"Kinetic energy: {energy_j:.2e} Joules")
        lines.append(f"TNT equivalent: {tnt_kg:.2e} kg ({tnt_kg / 1e9:.1f} gigatons)")
        lines.append(f"Estimated crater diameter: {crater_d:.0f} meters")
        lines.append(f"Equivalent earthquake magnitude: {eq_magnitude:.1f}")

        lines.append("\n  POTENTIAL CONSEQUENCES")
        lines.append("-" * 40)
        lines.append(f"Urban impact casualties: {estimate_casualties(diameter_avg, 'urban')}")
        lines.append(f"Rural impact casualties: {estimate_casualties(diameter_avg, 'rural')}")
        lines.append(f"Economic damage estimate: {economic_damage_estimate(diameter_avg)}")

        lines.append("\n  HISTORICAL CONTEXT")
        lines.append("-" * 40)
        if diameter_avg < 25:
            lines.append("Similar to: Chelyabinsk meteor (2013) - 20m diameter")
            lines.append("Effects: Atmospheric airburst, widespread window damage, ~1,500 injuries")
        elif diameter_avg < 80:
            lines.append("Similar to: Tunguska event (1908) - ~50-60m diameter")
            lines.append("Effects: Flattened 2,000 km² of forest, no direct casualties due to remote location")
        elif diameter_avg < 200:
            lines.append("Similar to: Barringer Crater impactor (~50,000 years ago) - ~50m diameter")
            lines.append("Effects: Created 1.2km wide crater in Arizona")
        else:
            lines.append("Larger than most historical impacts in human history")
            lines.append("Would represent a significant global threat requiring international response")

        lines.append("\n  ADDITIONAL RESOURCES")
        lines.append("-" * 40)
        lines.append(f"NASA JPL Database: {neo.get('nasa_jpl_url', 'N/A')}")
        if neo.get('is_sentry_object', False):
            lines.append("  This object is on NASA's Sentry risk assessment system")

        lines.append(f"\nOrbit uncertainty: {orbital_data.get('orbit_uncertainty', 'Unknown')}")
        lines.append(f"Minimum orbit intersection distance: {orbital_data.get('minimum_orbit_intersection', 'Unknown')} AU")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NEOAnalyzerApp()
    window.show()
    sys.exit(app.exec_())

