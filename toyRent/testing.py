# # # import requests

# # # data = requests.get('http://127.0.0.1:8000/api/productAPI/').json()

# # # if data:
# # #     print(data)
# # # else:
# # #     print('no data found')


# # def sum(a:int,b:int):
# #     return a+b



# # def sum(a:int,b:float):
# #     return a-b



# # print(sum(5,5))
# from datetime import datetime, timedelta

# # Get the current date
# current_date = datetime.now()

# # Specify the number of days to subtract
# days_to_subtract = 1237  # You can change this to any number of days you want

# # Subtract the days using timedelta
# new_date = current_date - timedelta(days=days_to_subtract)

# # Print the new date
# print("Current Date:", current_date.strftime('%Y-%m-%d'))
# print(f"Date {days_to_subtract} days ago:", new_date.strftime('%Y-%m-%d'))
