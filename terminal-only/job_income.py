import random

def income(random_number_1, random_number_2):
    dollars = random.randint(random_number_1, random_number_2)
    cents = random.randint(0, 100)
    return float(f"{dollars}.{cents}")
    
# lowest - 5
# highest - 100
jobs ={
    "boss" : income(16, 73),
    "witch" : income(7, 33),
    "actor" : income(15, 50),
    "golfer" : income(42, 69),
    "police" : income(23, 41),
    "wizard" : income(17, 77),
    "lawyer" : income(60, 79),
    "doctor" : income(10, 100),
    "cashier" : income(5, 15),
    "janitor" : income(10, 15),
    "manager" : income(13, 50),
    "associate" : income(1, 100),
    "baby maker" : income(1, 10),
    "pet groomer" : income(0, 20),
    "bridge maker" : income(45, 65),
    "fire fighter" : income(32, 41)
}

# print(jobs)