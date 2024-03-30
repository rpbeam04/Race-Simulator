from scipy.optimize import minimize
from pprint import pprint
from pulp import LpProblem, LpVariable, LpMinimize, lpSum

# Initial Setup
laps = 50
pit_time = 25

# Tire Data
soft = {
    "Lap Time": 60,
    "Degradation": 0.1,
    "Limit": 22
}
medium = {
    "Lap Time": 60.5,
    "Degradation": 0.007,
    "Limit": 30
}
hard = {
    "Lap Time": 61,
    "Degradation": 0.004,
    "Limit": 38
}

# Create a minimization problem
prob = LpProblem("Strategy", LpMinimize)

# Define integer variables with bounds
soft1Use = LpVariable("soft1Use", cat='Binary')
soft2Use = LpVariable("soft2Use", cat='Binary')
medUse = LpVariable("medUse", cat='Binary')
hardUse = LpVariable("hardUse", cat='Binary')
soft1Laps = LpVariable("soft1Laps", lowBound=0, upBound=laps, cat='Integer')
soft2Laps = LpVariable("soft2Laps", lowBound=0, upBound=laps, cat='Integer')
medLaps = LpVariable("medLaps", lowBound=0, upBound=laps, cat='Integer')
hardLaps = LpVariable("hardLaps", lowBound=0, upBound=laps, cat='Integer')
pitStops = LpVariable("pitStops", lowBound=1, upBound=laps, cat='Integer')

# Basic Feasible Solution Fed to Problem
# over = laps - int(laps/3)
# soft1Use.varValue = 0
# soft2Use.varValue = 1
# medUse.varValue = 1
# hardUse.varValue = 1
# soft1Laps.varValue = 0
# soft2Laps.varValue = int(laps/3)
# medLaps.varValue = int(laps/3)
# hardLaps.varValue = int(laps/3) + over

# Define objective function
prob += (
    (soft1Laps * soft["Lap Time"] + soft1Laps * soft["Degradation"]) +
    (soft2Laps * soft["Lap Time"] + soft2Laps * soft["Degradation"]) +
    (medLaps * medium["Lap Time"] + medLaps * medium["Degradation"]) +
    (hardLaps * hard["Lap Time"] + hardLaps * hard["Degradation"]) +
    pit_time * pitStops
), "Objective"

# Define equality constraint
prob += soft1Use + medUse + hardUse >= 2, "MinimumTireRule"
prob += soft1Use + soft2Use + medUse + hardUse - 1 == pitStops, "PitStops"
prob += soft1Laps >= soft1Use, "Soft1Limit"
prob += soft2Laps >= soft2Use, "Soft2Limit"
prob += medLaps >= medUse, "MediumLimit"
prob += hardLaps >= hardUse, "HardLimit"
prob += soft1Laps + soft2Laps + medLaps + hardLaps == laps, "RaceLaps"

# Solve the problem
prob.solve()

# Print the results
print("Optimal solution:")
print("soft1 =", soft1Laps.varValue)
print("soft2 =", soft2Laps.varValue)
print("medium =", medLaps.varValue)
print("hard =", hardLaps.varValue)
print("Optimal value of the objective function:", prob.objective.value())

# strategies = [[laps/3, laps/3, laps/3, 0, 1, 1, 1, 0],
#               [0, 0, laps/2, laps/2, 0, 0, 1, 1],
#               [laps/2, 0, laps/2, 0, 1, 0, 1, 0],
#               [laps/2, 0, 0, laps/2, 1, 0, 0, 1],
#               [laps/3, laps/3, 0, laps/3, 1, 1, 0, 1],
#               [laps/3, 0, laps/3, laps/3, 1, 0, 1, 1],
#               [laps/4, laps/4, laps/4, laps/4, 1, 1, 1, 1]]

# # Define the objective function to maximize
# def objective_function(x):
#     soft1Laps, soft2Laps, medLaps, hardLaps, soft1Use, soft2Use, medUse, hardUse = x
#     return (soft1Use*(soft1Laps*soft["Lap Time"] + soft["Degradation"]*laps_deg(soft1Laps)) + 
#             soft2Use*(soft2Laps*soft["Lap Time"] + laps_deg(soft2Laps)*soft["Degradation"]) + 
#             medUse*(medLaps*medium["Lap Time"] + laps_deg(medLaps)*medium["Degradation"]) + 
#             hardUse*(hardLaps*hard["Lap Time"] + laps_deg(hardLaps)*hard["Degradation"]) +
#             pit_time*(soft1Use + soft2Use + medUse + hardUse - 1))  

# # Define the constraint functions
# def minimum_rule(x):
#     soft1Laps, soft2Laps, medLaps, hardLaps, soft1Use, soft2Use, medUse, hardUse = x
#     return (soft1Use + medUse + hardUse) - 2

# def race_laps(x):
#     soft1Laps, soft2Laps, medLaps, hardLaps, soft1Use, soft2Use, medUse, hardUse = x
#     return soft1Laps + soft2Laps + medLaps + hardLaps - laps

# # These four constraints mean that if the use variable is 0, the laps should be 0 too
# def soft1(x):
#     soft1Laps, soft2Laps, medLaps, hardLaps, soft1Use, soft2Use, medUse, hardUse = x
#     return -soft1Use*soft1Laps + soft1Use

# def soft2(x):
#     soft1Laps, soft2Laps, medLaps, hardLaps, soft1Use, soft2Use, medUse, hardUse = x
#     return -soft2Use* soft2Laps + soft2Use

# def med(x):
#     soft1Laps, soft2Laps, medLaps, hardLaps, soft1Use, soft2Use, medUse, hardUse = x
#     return -medUse*medLaps + medUse

# def har(x):
#     soft1Laps, soft2Laps, medLaps, hardLaps, soft1Use, soft2Use, medUse, hardUse = x
#     return -hardUse*hardLaps + hardUse

# eps = 0
# # Define the bounds for variables
# bounds = [(0-eps, soft["Limit"]), (0-eps, soft["Limit"]), (0-eps, medium["Limit"]), (0-eps, hard["Limit"]),
#           (0-eps,1), (0-eps,1), (0-eps,1), (0-eps,1)]

# # Define the constraints
# constraints = [{'type': 'ineq', 'fun': minimum_rule},
#                {'type': 'eq', 'fun': race_laps},
#                {'type': 'eq', 'fun': soft1},
#                {'type': 'eq', 'fun': soft2},
#                {'type': 'eq', 'fun': med},
#                {'type': 'eq', 'fun': har}]

# # Solve the optimization problem
# results = []
# for guess in strategies:
#     result = minimize(objective_function, guess, bounds=bounds, constraints=constraints)
#     results.append(result)
# optimal = results[0]
# for result in results:
#     if result.fun < optimal.fun:
#         optimal = result
#         print("Local solution:")
#         print("Soft 1:", round(optimal.x[0],2))
#         print("Soft 2:", round(optimal.x[1],2))
#         print("Medium:", round(optimal.x[2],2))
#         print("Hard:", round(optimal.x[3],2))
#         print(optimal.x[4:])
#         print("Optimal value of the objective function:", round(optimal.fun,2))  # Objective function is negated
#         print("\n")

# # Print the result
# print("Optimal solution:")
# print("Soft 1:", round(optimal.x[0],2))
# print("Soft 2:", round(optimal.x[1],2))
# print("Medium:", round(optimal.x[2],2))
# print("Hard:", round(optimal.x[3],2))
# print(optimal.x[4:])
# print("Optimal value of the objective function:", round(optimal.fun,2))  # Objective function is negated
