import warnings

def explain_infeasibility(model):
    """
    Extract infeasibility explanation for the GLPK solver.
    """
    try:
        problem = model.solver.problem
        if hasattr(problem, "get_infeasibility"):
            return problem.get_infeasibility(model.solver.variables)
        return "Infeasibility explanation is not supported by the current solver."
    except Exception as e:
        warnings.warn(f"Failed to explain infeasibility: {e}", UserWarning)
        return "Error occurred while explaining infeasibility."

def simulate_conditions(model):
    """
    Simulate the model under various conditions and record results.
    """
    results = {
        "Base": [],
        "Low Glucose": [],
        "Hexokinase Deficiency": [],
        "reaction_fluxes": {}
    }

    # Reset bounds
    print("\n--- Resetting Reaction Bounds for Simulation ---")
    model.reactions.get_by_id("EX_glucose").lower_bound = -40
    model.reactions.get_by_id("hexokinase").upper_bound = 2000
    model.reactions.get_by_id("oxphos").upper_bound = 1000
    model.reactions.get_by_id("pyruvate_kinase").upper_bound = 1000

    # Base condition
    print("\n--- Simulating Base Condition ---")
    model.objective = "atp_maintenance"
    solution = model.optimize()
    if solution.status == "optimal":
        print("Base condition feasible.")
        results["Base"].append(solution.objective_value)
        results["reaction_fluxes"]["Base"] = solution.fluxes.to_dict()
    else:
        print("Base condition infeasible.")
        print(f"Infeasibility explanation: {explain_infeasibility(model)}")
        results["Base"].append(0)
        results["reaction_fluxes"]["Base"] = {}

    # Low glucose condition
    print("\n--- Simulating Low Glucose Condition ---")
    glucose_reaction = model.reactions.get_by_id("EX_glucose")
    original_glucose_bound = glucose_reaction.lower_bound

    for glucose_limit in range(-20, -1, 2):
        glucose_reaction.lower_bound = glucose_limit
        solution = model.optimize()
        scenario_name = f"Low Glucose {glucose_limit}"
        if solution.status == "optimal":
            print(f"Scenario '{scenario_name}' feasible.")
            results["Low Glucose"].append(solution.objective_value)
            results["reaction_fluxes"][scenario_name] = solution.fluxes.to_dict()
        else:
            print(f"Scenario '{scenario_name}' infeasible.")
            results["Low Glucose"].append(0)
            results["reaction_fluxes"][scenario_name] = {}
    glucose_reaction.lower_bound = original_glucose_bound

    # Hexokinase deficiency
    print("\n--- Simulating Hexokinase Deficiency ---")
    hexokinase_reaction = model.reactions.get_by_id("hexokinase")
    original_hexokinase_bound = hexokinase_reaction.upper_bound

    for enzyme_limit in range(5, 1001, 100):
        hexokinase_reaction.upper_bound = enzyme_limit
        solution = model.optimize()
        scenario_name = f"Hexokinase {enzyme_limit}"
        if solution.status == "optimal":
            print(f"Scenario '{scenario_name}' feasible.")
            results["Hexokinase Deficiency"].append(solution.objective_value)
            results["reaction_fluxes"][scenario_name] = solution.fluxes.to_dict()
        else:
            print(f"Scenario '{scenario_name}' infeasible.")
            results["Hexokinase Deficiency"].append(0)
            results["reaction_fluxes"][scenario_name] = {}
    hexokinase_reaction.upper_bound = original_hexokinase_bound

    return results
