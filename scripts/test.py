import random
insertDickInto = ['microwave', 'toaster', 'toaster oven', 'mailbox', '2008 Ford F-150', 'lawn mower']
randomObject = random.randint(0,len(insertDickInto) - 1)

print(insertDickInto[randomObject])

traits = ['keep_job', 'best_job', 'card_count', 'finese_the_dealer', 'slight_of_hand']
ALL_BITCH_TRAITS = ['keep_job', 'best_job', 'card_count', 'finese_the_dealer', 'slight_of_hand']
for trait in traits:
    ALL_BITCH_TRAITS.remove(trait)
if len(ALL_BITCH_TRAITS) != 0:
    traits.append(ALL_BITCH_TRAITS[random.randint(0,len(ALL_BITCH_TRAITS) - 1)])
print(traits)