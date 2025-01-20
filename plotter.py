import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

def plot_results(results):
    """
    Plots the simulation results.
    """
    plt.figure(figsize=(10, 6))

    # Base condition
    plt.scatter([0], results["Base"], color='red', label="Base Condition")

    # Low Glucose Condition
    glucose_levels = list(range(-20, -1, 2))
    plt.plot(glucose_levels, results["Low Glucose"], marker='o', label="Low Glucose Condition")

    # Hexokinase Deficiency
    enzyme_limits = list(range(5, 1001, 100))
    plt.plot(enzyme_limits, results["Hexokinase Deficiency"], marker='x', label="Hexokinase Deficiency")

    plt.title("Simulation Results")
    plt.xlabel("Scenario Parameter")
    plt.ylabel("ATP Production")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_reaction_contributions(results):
    reaction_fluxes = results.get("reaction_fluxes", {})
    if not reaction_fluxes:
        print("No reaction flux data available for plotting.")
        return

    # Validate scenarios and reactions
    scenarios = list(reaction_fluxes.keys())
    valid_scenarios = [s for s in scenarios if reaction_fluxes[s]]
    if not valid_scenarios:
        print("No valid reaction fluxes found in any scenario.")
        return

    # Get reaction names from the first valid scenario
    first_valid_scenario = reaction_fluxes[valid_scenarios[0]]
    reaction_names = list(first_valid_scenario.keys())

    # Plot fluxes for each reaction across scenarios
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 8))
    for reaction in reaction_names:
        flux_values = [
            reaction_fluxes[scenario].get(reaction, 0) for scenario in valid_scenarios
        ]
        plt.plot(valid_scenarios, flux_values, marker='o', label=reaction)

    plt.title("Reaction Contributions to ATP Production Across Scenarios - Vu Le 2025")
    plt.xlabel("Scenarios")
    plt.ylabel("Flux Value")
    plt.legend(loc="best", bbox_to_anchor=(1.05, 1), title="Reactions")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid()
    plt.show()

