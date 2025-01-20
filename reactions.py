from cobra import Reaction

def define_reactions(metabolites):
    reactions = {}

    # Glucose import
    reactions["EX_glucose"] = Reaction("EX_glucose")
    reactions["EX_glucose"].add_metabolites({metabolites["glucose"]: -1})
    reactions["EX_glucose"].lower_bound = -40  # Allow sufficient glucose uptake
    reactions["EX_glucose"].upper_bound = 0

    # Hexokinase
    reactions["hexokinase"] = Reaction("hexokinase")
    reactions["hexokinase"].add_metabolites({
        metabolites["glucose"]: -1,
        metabolites["adp"]: -1,
        metabolites["glucose_6p"]: 1,
        metabolites["atp"]: 1
    })
    reactions["hexokinase"].lower_bound = 0
    reactions["hexokinase"].upper_bound = 2000

    # Oxidative phosphorylation
    reactions["oxphos"] = Reaction("oxphos")
    reactions["oxphos"].add_metabolites({
        metabolites["glucose_6p"]: -1,
        metabolites["adp"]: -2,
        metabolites["atp"]: 2
    })
    reactions["oxphos"].lower_bound = 0
    reactions["oxphos"].upper_bound = 1000

    # Pyruvate kinase
    reactions["pyruvate_kinase"] = Reaction("pyruvate_kinase")
    reactions["pyruvate_kinase"].add_metabolites({
        metabolites["glucose_6p"]: -1,
        metabolites["adp"]: -1,
        metabolites["atp"]: 1
    })
    reactions["pyruvate_kinase"].lower_bound = 0
    reactions["pyruvate_kinase"].upper_bound = 1000

    # ATP maintenance
    reactions["atp_maintenance"] = Reaction("atp_maintenance")
    reactions["atp_maintenance"].add_metabolites({
        metabolites["atp"]: -1,
        metabolites["adp"]: 1
    })
    reactions["atp_maintenance"].lower_bound = 10  # Minimum ATP demand
    reactions["atp_maintenance"].upper_bound = 1000

    return reactions
