x = ["2024-11-20 : user_123 : PageVisited-Home,TimeSpent-120",
"2024-11-20 : user_456 : PageVisited-Products,TimeSpent-300",
"2024-11-20 : Debug : PageVisited-Contact,TimeSpent-1",
"2024-11-21 : user_342 : PageVisited-Home,TimeSpent-150",
"2024-11-21 : admin_1 : PageVisited-Products,TimeSpent-200",
"Log-Level-DB - Warn - PageVisited-About,TimeSpent-7",
"125-11-44 : user_342 : PageVisited-Contact,TimeSpent-0,Param-UserConstant",
"2024-11-21 : user_12 : PageVisited-Products,TimeSpent-200"]


from datetime import datetime

def validate_date(date_string):
    try:
        # Attempt to create a datetime object
        datetime.strptime(date_string, "%Y-%m-%d ")
        return True  # If successful, the date is valid
    except ValueError:
        return False  # If an error occurs, the date is invalid
    
    
res = []
total_Sum = 0
product_count = 0
date_count = []
for val in x:
    array = val.split(':')
    #check date format
    try:
        valid = validate_date(array[0])
    except Exception as e:
        valid = False
    
    
    if len(array)>1 and valid:
        if 'user' in array[1]:
            try:
                # import pdb;pdb.set_trace()
                time = array[2].split(',')[1].split('-')[1]
                # import pdb;pdb.set_trace()
                if 'product' in array[2].split(',')[0].lower():
                    product_count += int(time)
                total_Sum += int(time)
            except:
                import pdb;pdb.set_trace()
                
            res.append({array[1]:time})
            date_count.append({array[0]:time})
            pass

date_val = 0
for item in date_count:
    for key,val in item.items():
        import pdb;pdb.set_trace()
    if '2024-11-20 ' in item :
        date_val +=  int(item['2024-11-20 '])
                

print(res)
print(f"Total sum : {total_Sum}")
print(f"Product count : {product_count}")
print(f"Date count : {date_count}")
print(f"Count of specific date : {date_val}")
