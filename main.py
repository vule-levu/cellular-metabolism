from model_builder import build_model
from simulator import simulate_conditions
from plotter import plot_results, plot_reaction_contributions


def debug_model(model):
    """
    Debug and print details of the metabolic model.
    """
    print("\n--- Debugging Reactions and Metabolites ---")
    for reaction in model.reactions:
        print(f"Reaction: {reaction.id}, Equation: {reaction.reaction}")
        print(f"  Metabolites: {reaction.metabolites}")
        print(f"  Bounds: [{reaction.lower_bound}, {reaction.upper_bound}]")

    for metabolite in model.metabolites:
        print(f"Metabolite: {metabolite.id}, Reactions: {[r.id for r in metabolite.reactions]}")

    # Debug ATP maintenance reaction
    atp_maintenance = model.reactions.get_by_id("atp_maintenance")
    print("\n--- Inputs for atp_maintenance ---")
    for metabolite, coefficient in atp_maintenance.metabolites.items():
        print(f"{metabolite.id}: {coefficient}")


def adjust_model_bounds(model):
    """
    Adjust reaction and resource bounds for debugging.
    """
    print("\n--- Adjusting Reaction Bounds ---")
    model.reactions.get_by_id("hexokinase").upper_bound = 2000
    model.reactions.get_by_id("oxphos").upper_bound = 2000
    model.reactions.get_by_id("pyruvate_kinase").upper_bound = 2000
    model.reactions.get_by_id("EX_glucose").lower_bound = -40
    print("Bounds updated for key reactions.")


def test_incremental_atp_demand(model):
    """
    Test the model's performance under incremental ATP demands.
    """
    print("\n--- Incremental ATP Demand Testing ---")
    atp_maintenance = model.reactions.get_by_id("atp_maintenance")
    for atp_demand in range(10, 101, 10):  # Test ATP demands from 10 to 100
        atp_maintenance.lower_bound = atp_demand
        solution = model.optimize()
        if solution.status == "optimal":
            flux_glucose = abs(solution.fluxes.get("EX_glucose", 0))
            print(f"ATP Demand: {atp_demand}, Objective Value: {solution.objective_value}, "
                  f"ATP Yield per Glucose: {solution.objective_value / flux_glucose:.2f}")
        else:
            print(f"ATP Demand: {atp_demand}, Pathway infeasible.")
            break


def validate_model(model):
    """
    Perform final validation of the model under updated constraints.
    """
    print("\n--- Final Model Validation ---")
    solution = model.optimize()
    if solution.status == "optimal":
        print("ATP production pathway validated under new constraints.")
        print("Objective value (ATP production):", solution.objective_value)
        print("Flux distribution:\n", solution.fluxes)
    else:
        print("Pathway is infeasible under new constraints.")


def test_additional_scenarios(model):
    """
    Run further analyses by modifying reaction bounds and testing model behavior.
    """
    print("\n--- Further Analysis: Limiting Oxidative Phosphorylation ---")
    # Limit oxidative phosphorylation
    model.reactions.get_by_id("oxphos").upper_bound = 20
    solution = model.optimize()
    if solution.status == "optimal":
        print("With oxphos limited to 20, Objective Value (ATP production):", solution.objective_value)
        print("Flux distribution:\n", solution.fluxes)
    else:
        print("Pathway infeasible with oxphos limited to 20.")

    print("\n--- Further Analysis: Increasing ATP Demand Beyond 100 ---")
    # Incrementally increase ATP demand beyond 100
    atp_maintenance = model.reactions.get_by_id("atp_maintenance")
    for atp_demand in range(110, 201, 10):  # Test ATP demands from 110 to 200
        atp_maintenance.lower_bound = atp_demand
        solution = model.optimize()
        if solution.status == "optimal":
            flux_glucose = abs(solution.fluxes.get("EX_glucose", 0))
            print(f"ATP Demand: {atp_demand}, Objective Value: {solution.objective_value}, "
                  f"ATP Yield per Glucose: {solution.objective_value / flux_glucose:.2f}")
        else:
            print(f"ATP Demand: {atp_demand}, Pathway infeasible.")
            break


# def main():
#     # Step 1: Build the metabolic model
#     model = build_model()

#     # Step 2: Debug the model structure
#     debug_model(model)

#     # Step 3: Adjust reaction bounds and resource limits
#     adjust_model_bounds(model)

#     # Step 4: Test ATP production under incremental demands
#     test_incremental_atp_demand(model)

#     # Step 5: Validate the model
#     validate_model(model)

#     # Step 5.1: Test additional scenarios
#     test_additional_scenarios(model)

#     # Step 6: Run simulations for specific scenarios and plot results
#     print("\n--- Running Simulation and Plotting Results ---")
#     simulation_results = simulate_conditions(model)
#     print("\n--- Debug: Reaction Fluxes ---")
#     for scenario, fluxes in simulation_results["reaction_fluxes"].items():
#         print(f"Scenario: {scenario}, Fluxes: {fluxes}")
#     plot_results(simulation_results)

#     # Enhanced visualization
#     print("\n--- Enhanced Visualization: Reaction Contributions ---")
#     plot_reaction_contributions(simulation_results)

def main():
    """
    Main function to build the model, simulate conditions, and plot results.
    """
    # Build and debug the model
    model = build_model()

    # Run simulations for various conditions
    print("\n--- Running Simulation and Plotting Results ---")
    simulation_results = simulate_conditions(model)

    # Debug simulation results
    print("\n--- Debug: Reaction Fluxes ---")
    for scenario, fluxes in simulation_results["reaction_fluxes"].items():
        print(f"Scenario: {scenario}, Fluxes: {fluxes}")

    # Plot simulation results
    plot_results(simulation_results)

    # Enhanced visualization of reaction contributions
    print("\n--- Enhanced Visualization: Reaction Contributions ---")
    plot_reaction_contributions(simulation_results)
    
if __name__ == "__main__":
    main()
