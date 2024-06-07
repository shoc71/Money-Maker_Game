import random

def income(random_number_1, random_number_2):
    dollars = random.randint(random_number_1, random_number_2)
    cents = random.randint(0, 100)
    return float(f"{dollars}.{cents}")
    
# lowest - 5
# highest - 100
jobs ={
    "doctor" : income(10, 100),
    "golfer" : income(42, 69),
    "police" : income(23, 41),
    "cashier" : income(5, 15),
    "janitor" : income(10, 15),
    "manager" : income(13, 50),
    "firefighter" : income(32, 41),
    "pet groomer" : income(0, 20),
    "bridge maker" : income(45, 65)
}

# print(jobs)