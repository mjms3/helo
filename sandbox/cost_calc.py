# cost of 1 implies 1 radian covered in unit time
# 1 radian = radius of the earth = 6371 km
# london to glasgow as the crow flies is 556 km
# consider calculating this using the given data (change triangle weights to 1)
# (heloesp) ➜  sandbox git:(master) ✗ python gb_map.py -0.05 0.96 0.0 0.9
# {"COST": 0.0783040165594597, "POINTS": [[-0.05, 0.96], [-0.03866666666666667, 0.946], [-0.025, 0.933], [-0.005, 0.907666
# 6371*0.0783 = 498.8 km (reasonable given the points aren't exactly london and glasgow)
# so time is 6371*cost/speed_of_helicopter