from cobra import Metabolite

def define_metabolites():
    # Define metabolites with appropriate compartments
    metabolites = {
        "glucose": Metabolite("glucose", name="Glucose", compartment="e"),
        "glucose_6p": Metabolite("glucose_6p", name="Glucose-6-Phosphate", compartment="c"),
        "atp": Metabolite("atp", name="ATP", compartment="c"),
        "adp": Metabolite("adp", name="ADP", compartment="c"),
    }
    return metabolites
