import requests
import math
from datetime import datetime

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
    volume = (4/3) * math.pi * radius**3
    return volume * density

def calculate_kinetic_energy(mass_kg, velocity_ms):
    """Calculate kinetic energy in Joules"""
    return 0.5 * mass_kg * velocity_ms**2

def tnt_equivalent(energy_joules):
    """Convert energy to TNT equivalent"""
    tnt_energy = 4.184e6  # J per kg TNT
    return energy_joules / tnt_energy

def crater_diameter(energy_joules, target_density=2500, gravity=9.81):
    """Estimate crater diameter using scaling laws"""
    scaling_factor = 1.8
    return scaling_factor * (energy_joules / (target_density * gravity))**(1/3.4)

def seismic_magnitude(energy_joules):
    """Convert impact energy to equivalent earthquake magnitude"""
    if energy_joules <= 0:
        return 0
    log_energy = math.log10(energy_joules)
    return (log_energy - 5.24) / 1.44

def risk_assessment(diameter_m, miss_distance_km, is_hazardous):
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

def print_comprehensive_analysis(neo):
    """Print detailed analysis of the NEO"""
    print("=" * 80)
    print(f"COMPREHENSIVE ASTEROID ASSESSMENT: {neo.get('name')}")
    print("=" * 80)

    # Basic Information
    print("\n📊 BASIC INFORMATION")
    print("-" * 40)
    print(f"NASA Reference ID: {neo.get('neo_reference_id')}")
    print(f"Full Name: {neo.get('name')}")
    print(f"Designation: {neo.get('designation', 'N/A')}")
    print(f"Discovery: First observed {neo.get('orbital_data', {}).get('first_observation_date', 'Unknown')}")
    print(f"Last observed: {neo.get('orbital_data', {}).get('last_observation_date', 'Unknown')}")
    print(f"Data arc: {neo.get('orbital_data', {}).get('data_arc_in_days', 'Unknown')} days")
    print(f"Observations used: {neo.get('orbital_data', {}).get('observations_used', 'Unknown')}")

    # Size and Physical Characteristics
    print("\n🌑 PHYSICAL CHARACTERISTICS")
    print("-" * 40)
    diam = neo.get('estimated_diameter', {}).get('meters', {})
    diameter_min = diam.get('estimated_diameter_min', 0)
    diameter_max = diam.get('estimated_diameter_max', 0)
    diameter_avg = (diameter_min + diameter_max) / 2

    print(f"Estimated diameter: {diameter_min:.1f} - {diameter_max:.1f} meters")
    print(f"Average diameter: {diameter_avg:.1f} meters")
    print(f"Absolute magnitude (H): {neo.get('absolute_magnitude_h', 'Unknown')}")
    print(f"Estimated mass: {calculate_mass(diameter_avg):.2e} kg")

    # Hazard Assessment
    print("\n⚠️ HAZARD ASSESSMENT")
    print("-" * 40)
    hazardous = neo.get('is_potentially_hazardous_asteroid', False)
    print(f"Potentially Hazardous Asteroid (PHA): {'YES' if hazardous else 'NO'}")
    if hazardous:
        print("⚠️ This object meets NASA criteria for enhanced monitoring:")
        print("  - Approaches within 7.5 million km of Earth")
        print("  - Estimated diameter > 140 meters")

    # Orbital Information
    print("\n🌍 ORBITAL CHARACTERISTICS")
    print("-" * 40)
    orbital_data = neo.get('orbital_data', {})
    print(f"Semi-major axis: {orbital_data.get('semi_major_axis', 'Unknown')} AU")
    print(f"Eccentricity: {orbital_data.get('eccentricity', 'Unknown')}")
    print(f"Inclination: {orbital_data.get('inclination', 'Unknown')}°")
    print(f"Orbital period: {orbital_data.get('orbital_period', 'Unknown')} days")
    print(f"Perihelion distance: {orbital_data.get('perihelion_distance', 'Unknown')} AU")
    print(f"Aphelion distance: {orbital_data.get('aphelion_distance', 'Unknown')} AU")

    orbit_class = orbital_data.get('orbit_class', {})
    print(f"Orbit class: {orbit_class.get('orbit_class_type', 'Unknown')} - {orbit_class.get('orbit_class_description', 'Unknown')}")

    # Close Approaches Analysis
    print("\n🎯 CLOSE APPROACH HISTORY & FUTURE")
    print("-" * 40)
    approaches = neo.get('close_approach_data', [])

    if approaches:
        print(f"Total recorded close approaches: {len(approaches)}")

        # Find closest approach
        closest_approach = min(approaches, key=lambda x: float(x.get('miss_distance', {}).get('kilometers', float('inf'))))
        closest_distance = float(closest_approach.get('miss_distance', {}).get('kilometers', 0))
        closest_date = closest_approach.get('close_approach_date', 'Unknown')

        print(f"Closest recorded approach: {closest_date}")
        print(f"Closest distance: {closest_distance:,.0f} km ({closest_distance/384400:.2f} lunar distances)")

        # Recent and upcoming approaches
        current_year = datetime.now().year
        recent_approaches = [a for a in approaches if int(a.get('close_approach_date', '0000')[:4]) >= current_year - 5]
        future_approaches = [a for a in approaches if int(a.get('close_approach_date', '0000')[:4]) > current_year]

        if recent_approaches:
            print(f"\nRecent approaches (last 5 years): {len(recent_approaches)}")
            for approach in recent_approaches[:5]:
                date = approach.get('close_approach_date')
                distance = float(approach.get('miss_distance', {}).get('kilometers', 0))
                velocity = approach.get('relative_velocity', {}).get('kilometers_per_second', 'N/A')
                print(f"  {date}: {distance:,.0f} km, {velocity} km/s")

        if future_approaches:
            print(f"\nUpcoming approaches: {len(future_approaches)}")
            for approach in future_approaches[:5]:
                date = approach.get('close_approach_date')
                distance = float(approach.get('miss_distance', {}).get('kilometers', 0))
                velocity = approach.get('relative_velocity', {}).get('kilometers_per_second', 'N/A')
                print(f"  {date}: {distance:,.0f} km, {velocity} km/s")

        # Risk Assessment
        if closest_distance < 10000000:  # Within 10 million km
            size_risk, approach_risk = risk_assessment(diameter_avg, closest_distance, hazardous)
            print(f"\n🚨 RISK ANALYSIS")
            print("-" * 40)
            print(f"Size-based risk: {size_risk}")
            print(f"Approach risk: {approach_risk}")

    # Impact Scenario Analysis
    print("\n💥 HYPOTHETICAL IMPACT ANALYSIS")
    print("-" * 40)
    print("⚠️ NOTE: This is a theoretical analysis for educational purposes")

    # Use typical impact velocity
    impact_velocity_ms = 20000  # 20 km/s typical
    mass_kg = calculate_mass(diameter_avg)
    energy_j = calculate_kinetic_energy(mass_kg, impact_velocity_ms)
    tnt_kg = tnt_equivalent(energy_j)
    crater_d = crater_diameter(energy_j)
    eq_magnitude = seismic_magnitude(energy_j)

    print(f"Assumed impact velocity: 20 km/s (typical)")
    print(f"Kinetic energy: {energy_j:.2e} Joules")
    print(f"TNT equivalent: {tnt_kg:.2e} kg ({tnt_kg/1e9:.1f} gigatons)")
    print(f"Estimated crater diameter: {crater_d:.0f} meters")
    print(f"Equivalent earthquake magnitude: {eq_magnitude:.1f}")

    # Damage Estimates
    print(f"\n🏙️ POTENTIAL CONSEQUENCES")
    print("-" * 40)
    print(f"Urban impact casualties: {estimate_casualties(diameter_avg, 'urban')}")
    print(f"Rural impact casualties: {estimate_casualties(diameter_avg, 'rural')}")
    print(f"Economic damage estimate: {economic_damage_estimate(diameter_avg)}")

    # Historical Context
    print(f"\n📚 HISTORICAL CONTEXT")
    print("-" * 40)
    if diameter_avg < 25:
        print("Similar to: Chelyabinsk meteor (2013) - 20m diameter")
        print("Effects: Atmospheric airburst, widespread window damage, ~1,500 injuries")
    elif diameter_avg < 80:
        print("Similar to: Tunguska event (1908) - ~50-60m diameter")
        print("Effects: Flattened 2,000 km² of forest, no direct casualties due to remote location")
    elif diameter_avg < 200:
        print("Similar to: Barringer Crater impactor (~50,000 years ago) - ~50m diameter")
        print("Effects: Created 1.2km wide crater in Arizona")
    else:
        print("Larger than most historical impacts in human history")
        print("Would represent a significant global threat requiring international response")

    # Additional Information
    print(f"\n🔗 ADDITIONAL RESOURCES")
    print("-" * 40)
    print(f"NASA JPL Database: {neo.get('nasa_jpl_url', 'N/A')}")
    if neo.get('is_sentry_object', False):
        print("⚠️ This object is on NASA's Sentry risk assessment system")

    print(f"\nOrbit uncertainty: {orbital_data.get('orbit_uncertainty', 'Unknown')}")
    print(f"Minimum orbit intersection distance: {orbital_data.get('minimum_orbit_intersection', 'Unknown')} AU")

    print("\n" + "=" * 80)

if __name__ == '__main__':
    print("🛡️ NASA NEO COMPREHENSIVE ANALYSIS TOOL")
    print("Provides detailed asteroid information including impact assessments")
    print("-" * 80)

    while True:
        ref_id = input("\nEnter NASA NEO Reference ID (or 'exit' to quit): ").strip()
        if ref_id.lower() == 'exit':
            print("Exiting program. Stay vigilant! 🌍")
            break
        try:
            print(f"\n🔍 Fetching data for NEO ID: {ref_id}...")
            neo_data = fetch_neo_by_reference_id(ref_id)
            print_comprehensive_analysis(neo_data)

        except requests.HTTPError as e:
            if e.response.status_code == 404:
                print(f"❌ NEO with ID '{ref_id}' not found in NASA database.")
                print("Try these example IDs: 2000433, 2000719, 2000887, 2001036, 2001221")
            else:
                print(f"❌ HTTP Error: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
