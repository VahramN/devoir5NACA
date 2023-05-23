# This program calculates the NACA symmetric airfoil data and plot the airfoil.
# The program takes as input the NACA number, which las 2 digits present the thickness in percentage,
# as well it takes as input the plot points number and the plot poits type, r linear or  Glauert transformation.
import math
import numpy as np
import matplotlib.pyplot as plt

naca_numbers = "" # input: NACA profile number
cord = 0.0 # input: cord in meters
nb_points = 0 # input: number of points for plot
type_points_linear = -1 # input: is linear or not
def start_inputs():
    global naca_numbers, cord, nb_points, type_points_linear

    while((len(naca_numbers) != 4) or not naca_numbers.isdigit()):
        naca_numbers = input("Enter the NACA profile in 4 digits: ")

    while (cord == 0.0):
        entry = input("Enter the cord in meters: ")
        if entry.replace(".", "").isnumeric():
            cord = float(entry)

    while (nb_points < 10):
        entry = input("Enter the number of points (minimum 10): ")
        if entry.isdigit():
            nb_points = int(entry)

    while (not(0 <= type_points_linear <= 1)):
        entry = input("Enter the points type. Linear -> 1, Non-linear -> 0: ")
        if entry.isdigit() and len(entry) == 1:
            type_points_linear = int(entry)


# calculated in meters
def calculate_cord_thickness(_naca_numbers):
    last_2_numbers = int(_naca_numbers) % 100
    # return thickness percentage
    return last_2_numbers/100


#
def get_variation_array_teta(_nb_points):
    teta = np.linspace(0, math.pi, num=_nb_points)
    return 0.5 * (1 - np.cos(teta))


#
def get_variation_array_liear(_nb_points):
    return np.linspace(0, 1, num=_nb_points)


# Plot Extrados, Intrados and the max thickness
def plot(x_Extrados, y_Extrados, x_intrados, y_intrados, thick_max_index):
    # quelques parametre pour le graphique
    plt.rcParams['font.size'] = 10
    plt.rcParams['figure.autolayout'] = True
    plt.rcParams['figure.dpi'] = 110

    # Bloc de code pour le trace
    plt.plot(x_Extrados, y_Extrados, label='Extrados')
    plt.plot(x_intrados, y_intrados, label='Intrados', linestyle='--')
    # construct thickness line
    thikness_x = [x_Extrados[thick_max_index], x_intrados[thick_max_index]]
    thikness_y = [y_Extrados[thick_max_index], y_intrados[thick_max_index]]
    thickness_text = (f"Max thickness: {round(y_Extrados[thick_max_index]-y_intrados[thick_max_index], 2)}m, "
                      f"distance from the leading edge: {round(x_Extrados[thick_max_index],2)}m")
    plt.plot(thikness_x, thikness_y, label=thickness_text)

    plt.xlabel('X - airfoil length in meter')
    plt.ylabel('Y - airfoil thickness in meter')
    plt.axis('equal')
    plt.legend(title=f"Cord length: {cord}m. Plot points: Linear.") if type_points_linear == 1 else plt.legend(title=f"Cord length: {cord}m. Plot points: Glauert transformation.")
    plt.grid()
    plt.title(f"NACA{naca_numbers} symmetric airfoil")
    plt.show()


#read the inputs and set the global variables
start_inputs()

# calculate cord max thickness from the NACA number
cord_thickness = calculate_cord_thickness(naca_numbers)
#print(f"Calculated thickness: {cord_thickness}")

# Xc is the array of the [0, 1] points. It is constructed or liear, or Glauert transformation
Xc = np.zeros(nb_points)
if type_points_linear == 1:
    Xc = get_variation_array_liear(nb_points)
else:
    Xc = get_variation_array_teta(nb_points)
#print(f"Xc variations [0,1] are: {Xc}")

# Yt is half thickness of the cord
Yt = np.zeros(nb_points)
Yt = 5 * cord_thickness * (0.2969 * np.sqrt(Xc) -
                           0.1260 * Xc -
                           0.3516 * Xc**2 +
                           0.2843 * Xc**3 -
                           0.1036 * Xc**4)
#print(f"Yt coordinates are: {Yt}")

# Extrados values
Xup = Xc * cord
Yup = Yt * cord
# Intrados values
Xdown = Xc * cord
Ydown = -1 * Yt * cord

# index where the Y is maximal, the thickness will be also maximal, because it is an symmetric airfoil.
max_index = np.argmax(Yup)
# plot
plot(Xup, Yup, Xdown, Ydown, max_index)
