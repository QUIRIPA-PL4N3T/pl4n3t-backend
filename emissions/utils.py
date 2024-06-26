from emissions.models import EmissionFactor


def calculate_emission(name, factor: EmissionFactor, consumption, application_percentage=1):
    """
    Calculate emissions for a given emission factor.

    Parameters:
    - name (str): The name of the component or main factor.
    - factor (EmissionFactor): The emission factor object to be used for calculations.
    - consumption (float): The amount of consumption for the emission source.
    - application_percentage (float): The percentage of application of the emission factor (default is 1, i.e., 100%).

    Returns:
    - dict: A dictionary containing the component name, detailed results for each greenhouse gas, and total CO2e emissions.
    """

    total_co2e = 0
    results = []

    # Calculate emissions for each greenhouse gas associated with the emission factor
    for gas_emission_factor in factor.greenhouse_emission_gases.all():
        if gas_emission_factor.value != 0:
            # Get gas data
            gas_emission = gas_emission_factor.greenhouse_gas
            # Get emission factor value and uncertainty
            factor_value = gas_emission_factor.value
            uncertainty = gas_emission_factor.percentage_uncertainty

            # Calculate CO2e and GWP (Global Warming Potential)
            co2e = consumption * factor_value * application_percentage
            gwp = gas_emission.kg_co2_equivalence * co2e

            total_co2e = total_co2e + gwp

            # Append results for the current gas
            results.append({
                'gas_name': gas_emission.name,
                'gas': gas_emission.acronym,
                'value': factor_value,
                'co2e': co2e,
                'uncertainty': uncertainty,
                'gwp': gwp
            })

    # Return the final results including the total CO2e for the component
    return {
        'component': name,
        'results': results,
        'co2e': total_co2e
    }

