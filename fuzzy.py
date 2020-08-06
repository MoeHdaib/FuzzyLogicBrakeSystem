import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
from skfuzzy import control as ctrl

# Declare global variables: 
# Distance with a range (0, 10) m, Speed with a range (0, 10) m/s, and Brake woth a range (o, 24) N. 
dist = np.arange(0, 11, 1)
speed = np.arange(0, 11, 1)
Brake_F = np.arange(0, 25, 1)

# Declare fuzzy functions
Dist_very_close = fuzz.trimf(dist, [0, 0, 4])
Dist_close = fuzz.trapmf(dist, [2, 4, 6, 8])
Dist_far = fuzz.trimf(dist, [6, 10, 10])
speed_too_slow = fuzz.trapmf(speed, [0, 0, 1, 2])
speed_slow = fuzz.trapmf(speed, [1, 2, 3, 4])
speed_optimal = fuzz.trapmf(speed, [3, 4, 5, 6])
speed_fast = fuzz.trapmf(speed, [5, 6, 7, 8])
speed_too_fast = fuzz.trapmf(speed, [7, 8, 10,10])
Dec_brake_highly = fuzz.trimf(Brake_F, [0, 4, 8])
Dec_brake_lightly = fuzz.trimf(Brake_F, [4, 8, 12])
No_brake = fuzz.trimf(Brake_F, [8, 12, 16])
Inc_brake_lightly = fuzz.trimf(Brake_F, [12, 16, 20])
Inc_brake_highly = fuzz.trimf(Brake_F, [16, 20, 24])

# Visualize the functions 
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(10, 10))
ax0.plot(dist, Dist_very_close, 'b', linewidth=1.5, label='Very-Close')
ax0.plot(dist, Dist_close, 'g', linewidth=1.5, label='Close')
ax0.plot(dist, Dist_far, 'r', linewidth=1.5, label='Far')
ax0.set_title('Vehicle distance')
ax0.legend()
ax1.plot(speed, speed_too_slow, 'b', linewidth=1.5, label='Too Slow')
ax1.plot(speed, speed_slow, 'y', linewidth=1.5, label='Slow')
ax1.plot(speed, speed_optimal, 'g', linewidth=1.5, label='optimal')
ax1.plot(speed, speed_fast, 'r', linewidth=1.5, label='Fast')
ax1.plot(speed, speed_too_fast, 'k', linewidth=1.5, label='Too Fast')
ax1.set_title('Speed')
ax1.legend()
ax2.plot(Brake_F, Dec_brake_lightly, 'b', linewidth=1.5, label='Dec-lightly')
ax2.plot(Brake_F, Dec_brake_highly, 'y', linewidth=1.5, label='Dec-Highly')
ax2.plot(Brake_F, No_brake, 'g', linewidth=1.5, label='No_brake')
ax2.plot(Brake_F, Inc_brake_lightly, 'r', linewidth=1.5, label='Inc_lightly')
ax2.plot(Brake_F, Inc_brake_highly, 'k', linewidth=1.5, label='Inc_Highly')
ax2.set_title('Brake force')
ax2.legend()

# delete top and right axes
for ax in (ax0, ax1, ax2):
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.get_xaxis().tick_bottom()
	ax.get_yaxis().tick_left()

plt.tight_layout()
plt.show()

distance = ctrl.Antecedent(dist, 'distance')
speed = ctrl.Antecedent(speed, 'speed')
Brake_F = ctrl.Consequent(Brake_F,'Brake_F')


# Generate fuzzy membership functions
distance['very_close'] = fuzz.trimf(distance.universe, [0, 0, 4])
distance['close'] = fuzz.trapmf(distance.universe, [2, 4, 6, 8])
distance['far'] = fuzz.trimf(distance.universe, [6, 10, 10])

speed['too_slow'] = fuzz.trapmf(speed.universe, [0, 0, 1, 2])
speed['slow'] = fuzz.trapmf(speed.universe, [1, 2, 3, 4])
speed['optimal'] = fuzz.trapmf(speed.universe, [3, 4, 5, 6])
speed['fast'] = fuzz.trapmf(speed.universe, [5, 6, 7, 8])
speed['too_fast'] = fuzz.trapmf(speed.universe, [7, 8, 10,10])

Brake_F['Dec-Highly'] = fuzz.trimf(Brake_F.universe, [0, 4, 8])
Brake_F['Dec-lightly'] = fuzz.trimf(Brake_F.universe, [4, 8, 12])
Brake_F['No_brake'] = fuzz.trimf(Brake_F.universe, [8, 12, 16])
Brake_F['Inc_lightly'] = fuzz.trimf(Brake_F.universe, [12, 16, 20])
Brake_F['Inc_Highly'] = fuzz.trapmf(Brake_F.universe, [16, 20, 24, 24])


# The fuzzy design rules

rule1 = ctrl.Rule(distance['very_close'] , Brake_F['Inc_Highly'])
rule2 = ctrl.Rule(distance['close'] & speed['too_fast'] , Brake_F['Inc_lightly'])
rule3 = ctrl.Rule(distance['close'] & speed['optimal'] , Brake_F['Inc_lightly'])
rule4 = ctrl.Rule(distance['far'] & speed['optimal'] , Brake_F['No_brake'])
rule5 = ctrl.Rule(distance['far'] & speed['slow'] , Brake_F['Dec-lightly'])
rule6 = ctrl.Rule(distance['far'] & speed['too_slow'] , Brake_F['Dec-Highly'])
brake_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
braking = ctrl.ControlSystemSimulation(brake_ctrl)

# Passing inputs in distance and speed.
braking.input['distance'] = 8
braking.input['speed'] = 3

# Compute and visulise the output 
braking.compute()
print (braking.output['Brake_F'])
Brake_F.view(sim=braking)
input("Press enter to exit.")
