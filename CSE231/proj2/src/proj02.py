__author__ = 'Brian Cong'
num = int(input('Input an integer: '))
output = num
count = 0
while (output > 10):
    num = output
    holder = 0
    length = len(str(num))
    for x in range(length):
        holder += int(num/10**(length-(x+1)))
        num -= int(num/10**(length-(x+1))) * 10**(length-(x+1))
    output = holder
    count += 1
    print ('Sum number', count, 'is',output)
print('Summed number is:',int(output))
print('Length of number was:',length)



