import json
from pprint import pprint as pp
import pickle


def yes_no_counts(dataset, play_tennis='Yes'):
    counter = 0
    for dt in dataset:
        if dt['Play Tennis'] == play_tennis:
            counter += 1
    return counter


def yes_no_probs(c_yes, c_no):
    p_yes = c_yes/ (c_yes + c_no)
    p_no = c_no/ (c_yes + c_no)
    return {
            "p_yes": p_yes,
            "p_no": p_no
            }


def feature_counts(dataset, feature):
    feature_counts = {}
    total_class_counts = {}
    for out_dict in dataset:
        if out_dict[feature] in feature_counts:
            if out_dict['Play Tennis'] in feature_counts[out_dict[feature]]:
                feature_counts[out_dict[feature]][out_dict['Play Tennis']] += 1
                if out_dict['Play Tennis'] in total_class_counts:
                    total_class_counts[out_dict['Play Tennis']] += 1
                else:
                    total_class_counts[out_dict['Play Tennis']] = 1
            else:
                feature_counts[out_dict[feature]][out_dict['Play Tennis']] = 1
                if out_dict['Play Tennis'] in total_class_counts:
                    total_class_counts[out_dict['Play Tennis']] += 1
                else:
                    total_class_counts[out_dict['Play Tennis']] = 1
        else:
            feature_counts[out_dict[feature]] = {}
            if out_dict['Play Tennis'] in feature_counts[out_dict[feature]]:
                feature_counts[out_dict[feature]][out_dict['Play Tennis']] += 1
                if out_dict['Play Tennis'] in total_class_counts:
                    total_class_counts[out_dict['Play Tennis']] += 1
                else:
                    total_class_counts[out_dict['Play Tennis']] = 1
            else:
                feature_counts[out_dict[feature]][out_dict['Play Tennis']] = 1
                if out_dict['Play Tennis'] in total_class_counts:
                    total_class_counts[out_dict['Play Tennis']] += 1
                else:
                    total_class_counts[out_dict['Play Tennis']] = 1
    # for out_dict in dataset:
    #    new_key = f'{out_dict["Outlook"]}_{out_dict["Play Tennis"]}'
    #    if new_key in outlook_counts:
    #        outlook_counts[new_key] += 1
    #    else:
    #        outlook_counts[new_key] = 1
    # print(feature_counts) 
    return feature_counts, total_class_counts


def p_compute(feature_counts_table, total_counts_table):
    p_values = {}
    for feature, counts in feature_counts_table.items():
        p_values[feature] = {}
        for label , count in counts.items():
            p_values[feature][label] = count / total_counts_table[label]
    return p_values        
            

with open('dataset.json', 'r') as f:
    ds = json.load(f)
    yes_counts = yes_no_counts(ds, 'Yes')
    no_counts = yes_no_counts(ds, 'No')
    yes_no_probs = yes_no_probs(yes_counts, no_counts)
    features = ['Outlook', 'Temperature', 'Humidity', 'Windy']
    fx_counts, tx_counts = {}, {}
    probability_table = {}
    for each_feature in features:
        fx_counts[each_feature], tx_counts[each_feature] = feature_counts(ds, each_feature)
        probability_table[each_feature] = p_compute(fx_counts[each_feature], tx_counts[each_feature])
    
    print(probability_table)
    pickle.dump(probability_table, open('probability_table.pkl', 'wb'))
    pickle.dump(yes_no_probs, open('yes_no_prob_table.pkl', 'wb'))
# print(feature_counts)
# print(yes_counts, no_counts,yes_no_counts)

# print(p_compute(fx_counts['Outlook'], tx_counts['Outlook']))
# print(p_compute(fx_counts['Temperature'], tx_counts['Temperature']))
# print(p_compute(fx_counts['Humidity'], tx_counts['Humidity']))
# print(p_compute(fx_counts['Windy'], tx_counts['Windy']))
# print(yes_no_probs)



