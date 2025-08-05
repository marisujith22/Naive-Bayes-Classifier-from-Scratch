import pickle

probability_table = pickle.load(open('probability_table.pkl', 'rb'))
probability_table['Outlook']['Overcast']['No'] = 0.0
yes_no_prob_table = pickle.load(open('yes_no_prob_table.pkl', 'rb'))

test_set = [
    {'Outlook': 'Overcast', 'Temperature': 'Mild', 'Humidity': 'Normal', 'Windy': False},
    {'Outlook':'Sunny', 'Temperature':'Cool', 'Humidity':'High', 'Windy':False},
    {'Outlook': 'Rainy', 'Temperature': 'Mild', 'Humidity': 'Normal', 'Windy': False},
    {'Outlook': 'Sunny', 'Temperature': 'Hot', 'Humidity': 'High', 'Windy': True}
    
]

#print(probability_table)
#print(yes_no_prob_table)

# def predicition(each_feature, yes_no_probs, yes_counts, no_counts, test_set):
#     play_tennis = {}
#     for test in test_set.items():
#         yes_counts = yes_no_probs["Yes"]
#         no_counts = yes_no_probs["No"]
#         for feature value in each_feature.items():

def prediction(yes_no):
    probs = []
    for each_sample in test_set:
        prob_val = 1.0
        for each_feature in each_sample:
            if yes_no == 'Yes':
                prob_val *= probability_table[each_feature][each_sample[each_feature]]['Yes']
            elif yes_no == 'No':
                prob_val *= probability_table[each_feature][each_sample[each_feature]]['No']
        if yes_no == 'Yes':
            prob_val *= yes_no_prob_table['p_yes']
        else:
            prob_val *= yes_no_prob_table['p_no']
        probs.append(prob_val)
                       
    return probs

yes_probs = prediction('Yes')
no_probs = prediction('No')


for i in range(0,4):
    if yes_probs[i] > no_probs[i]:
        print("Play Tennis : Yes")
    else:
        print("Play Tennis : No")

print(yes_probs)
print(no_probs)