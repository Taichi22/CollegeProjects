__author__ = 'Brian'
num_Speed = float(input ('Enter wind speed in MPH, rounded to nearest whole number.'))
num_Temp = float(input('Enter temperature in deg. Fahrenheit, rounded to nearest tenth.'))
print('The wind speed is: ', num_Speed, ' and the temperature is ', num_Temp)
print('The windchill index is ', round(35.74 + 0.621*num_Temp - (35.75*(num_Speed**0.16)) + (0.4275*num_Temp*(num_Speed**0.16)), 3), 'rounded to three digits.')
yescheck = str(input('Would you like to see the full set of digits?'))
if('y' or 'Y' in yescheck):
    print('The windchill index is ', 35.74 + 0.621*num_Temp - (35.75*(num_Speed**0.16)) + (0.4275*num_Temp*(num_Speed**0.16)))
else:
    print('Close.')
