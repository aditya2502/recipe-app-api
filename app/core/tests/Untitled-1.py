Input str="12345"
Expected out
12345
23451
34512
45123
51234


def output(num_str)
    result =[]
    result.append(num_str)
    
num_str ='12345'
for i in range(1,len(str)):
    num1 = num_str[1:] + num_str[:1]
    result.append(num1)
    
output(result)
     
    