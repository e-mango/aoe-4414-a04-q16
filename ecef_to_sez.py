# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
#  This converts the ECEF frame into the SEZ frame
# Parameters:
#  o_x_km: The ECEF origin x component of the SEZ frame in km
#  o_y_km: The ECEF origin y component of the SEZ frame in km
#  o_z_km: The ECEF origin z component of the SEZ frame in km
#  x_km: The ECEF x component of the SEZ frame in km
#  y_km: The ECEF y component of the SEZ frame in km
#  z_km: The ECEF z component of the SEZ frame in km
# Output:
#  s_km: S component of the SEZ frame in km
#  e_km: E component of the SEZ frame in km
#  z_km: Z component of the SEZ frame in km

# Written by Evan Schlein
# Other contributors: None

# import Python modules
import sys 
import math

# "constants"
R_E_KM = 6378.137
E_E    = 0.081819221456

# helper functions

# calculated denominator
def calc_denom(E_E, lat_rad):
  return math.sqrt(1.0-(E_E**2)*(math.sin(lat_rad)**2))

# initialize script arguments
o_x_km = float('nan')  # The ECEF origin x component of the SEZ frame in km
o_y_km = float('nan')  # The ECEF origin y component of the SEZ frame in km
o_z_km = float('nan')  # The ECEF origin z component of the SEZ frame in km
x_km = float('nan')    # The ECEF x component of the SEZ frame in km
y_km = float('nan')    # The ECEF y component of the SEZ frame in km
z_km = float('nan')    # The ECEF z component of the SEZ frame in km

# parse script arguments
if len(sys.argv) == 7:
    o_x_km = float(sys.argv[1])
    o_y_km = float(sys.argv[2])
    o_z_km = float(sys.argv[3])
    x_km = float(sys.argv[4])
    y_km = float(sys.argv[5])
    z_km = float(sys.argv[6])
else:
    print(
        'Usage: '
        'python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'
    )
    exit()

# write script below this line

# Calcualte Reference position
ECEF_x_km = x_km - o_x_km
ECEF_y_km = y_km - o_y_km
ECEF_z_km = z_km - o_z_km

r_x_km = o_x_km
r_y_km = o_y_km
r_z_km = o_z_km

# Calculate LLH Frame

# calculate longitude
lon_rad = math.atan2(r_y_km,r_x_km)
lon_deg = lon_rad*180.0/math.pi

# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(r_z_km/math.sqrt(r_x_km**2+r_y_km**2+r_z_km**2))
r_lon_km = math.sqrt(r_x_km**2+r_y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(E_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((r_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1

# Rotation
sez_vector = [-ECEF_z_km*math.cos(lat_rad) + ECEF_x_km*math.cos(lon_rad)*math.sin(lat_rad) + ECEF_y_km*math.sin(lat_rad)*math.sin(lon_rad), ECEF_y_km*math.cos(lon_rad) - ECEF_x_km*math.sin(lon_rad), ECEF_x_km*math.cos(lat_rad)*math.cos(lon_rad) + ECEF_z_km*math.sin(lat_rad) + ECEF_y_km*math.cos(lat_rad)*math.sin(lon_rad)]

s_km = sez_vector[0]
e_km = sez_vector[1]
z_km = sez_vector[2]

print(s_km)
print(e_km)
print(z_km)
