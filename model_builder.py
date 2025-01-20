from cobra import Model
from cobra.util.solver import linear_reaction_coefficients
from metabolites import define_metabolites
from reactions import define_reactions

def build_model():
    """
    Build and return the glycolysis metabolic model.
    """
    # Create the model
    model = Model("glycolysis_debug")

    # Define metabolites and reactions
    metabolites = define_metabolites()
    reactions = define_reactions(metabolites)

    # Add reactions to the model
    model.add_reactions(list(reactions.values()))

    # Set the objective
    model.objective = "atp_maintenance"

    # Ensure compatible solver
    model.solver = "glpk"
    print(f"Using solver: {model.solver.interface}")

    # Debug: Check model consistency
    print("\n--- Checking Model Consistency ---")
    for reaction in model.reactions:
        if reaction.lower_bound > reaction.upper_bound:
            print(f"Warning: Reaction '{reaction.id}' has inconsistent bounds: "
                  f"[{reaction.lower_bound}, {reaction.upper_bound}]")

    # Debug: Check for linear reaction coefficients
    print("\n--- Checking Linear Coefficients ---")
    coefficients = linear_reaction_coefficients(model)
    for reaction_id, coefficient in coefficients.items():
        print(f"Reaction '{reaction_id}' has coefficient: {coefficient}")

    return model
