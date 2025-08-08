import streamlit as st
import json
import pickle

# ========== Helper Functions ==========

def yes_no_counts(dataset, play_tennis='Yes'):
    return sum(1 for dt in dataset if dt['Play Tennis'] == play_tennis)

def yes_no_probs(c_yes, c_no):
    total = c_yes + c_no
    return {"p_yes": c_yes / total, "p_no": c_no / total}

def feature_counts(dataset, feature):
    feature_counts = {}
    total_class_counts = {}
    for item in dataset:
        f_val = item[feature]
        label = item['Play Tennis']
        if f_val not in feature_counts:
            feature_counts[f_val] = {}
        if label not in feature_counts[f_val]:
            feature_counts[f_val][label] = 0
        feature_counts[f_val][label] += 1

        if label not in total_class_counts:
            total_class_counts[label] = 0
        total_class_counts[label] += 1
    return feature_counts, total_class_counts

def p_compute(feature_counts_table, total_counts_table):
    p_values = {}
    for feature, counts in feature_counts_table.items():
        p_values[feature] = {}
        for label , count in counts.items():
            p_values[feature][label] = count / total_counts_table[label]
    return p_values  

def train_model(dataset):
    yes_counts = yes_no_counts(dataset, 'Yes')
    no_counts = yes_no_counts(dataset, 'No')
    yes_no_prob = yes_no_probs(yes_counts, no_counts)
    
    features = ['Outlook', 'Temperature', 'Humidity', 'Windy']
    fx_counts, tx_counts = {}, {}
    probability_table = {}
    for each_feature in features:
        fx_counts[each_feature], tx_counts[each_feature] = feature_counts(dataset, each_feature)
        probability_table[each_feature] = p_compute(fx_counts[each_feature], tx_counts[each_feature])

    return probability_table, yes_no_prob

def predict(test_set, probability_table, yes_no_prob_table, target_class):
    probs = []
    for each_sample in test_set:
        prob_val = 1.0
        for each_feature in each_sample:
            try:
                prob_val *= probability_table[each_feature][each_sample[each_feature]][target_class]
            except KeyError:
                prob_val *= 0  # Unseen value
        prob_val *= yes_no_prob_table['p_yes'] if target_class == 'Yes' else yes_no_prob_table['p_no']
        probs.append(prob_val)
    return probs

# ========== Streamlit UI ==========

st.title("🎾 Naive Bayes - Play Tennis Predictor")

uploaded_file = st.file_uploader("Upload your dataset (dataset.json)", type="json")

if uploaded_file is not None:
    data = json.load(uploaded_file)
    probability_table, yes_no_prob_table = train_model(data)

    st.success("Model Trained Successfully!")

    st.subheader("Enter a Test Sample")
    outlook = st.selectbox("Outlook", ['Sunny', 'Overcast', 'Rainy'])
    temperature = st.selectbox("Temperature", ['Hot', 'Mild', 'Cool'])
    humidity = st.selectbox("Humidity", ['High', 'Normal'])
    windy = st.radio("Windy", [True, False])

    test_sample = [{
        'Outlook': outlook,
        'Temperature': temperature,
        'Humidity': humidity,
        'Windy': windy
    }]

    if st.button("Predict"):
        yes_probs = predict(test_sample, probability_table, yes_no_prob_table, 'Yes')
        no_probs = predict(test_sample, probability_table, yes_no_prob_table, 'No')

        st.write("✅ **Prediction Result**")
        if yes_probs[0] > no_probs[0]:
            st.success("🎾 Play Tennis: **Yes**")
        else:
            st.error("🏖️ Play Tennis: **No**")

        st.write("🔍 Yes Probability:", yes_probs[0])
        st.write("🔍 No Probability:", no_probs[0])

    # Optional: Run on predefined test set
    if st.checkbox("Run on default test set"):
        test_set = [
            {'Outlook': 'Overcast', 'Temperature': 'Mild', 'Humidity': 'Normal', 'Windy': False},
            {'Outlook':'Sunny', 'Temperature':'Cool', 'Humidity':'High', 'Windy':False},
            {'Outlook': 'Rainy', 'Temperature': 'Mild', 'Humidity': 'Normal', 'Windy': False},
            {'Outlook': 'Sunny', 'Temperature': 'Hot', 'Humidity': 'High', 'Windy': True}
        ]
        yes_probs = predict(test_set, probability_table, yes_no_prob_table, 'Yes')
        no_probs = predict(test_set, probability_table, yes_no_prob_table, 'No')

        st.write("### 📋 Batch Test Results")
        for i, sample in enumerate(test_set):
            result = "Yes" if yes_probs[i] > no_probs[i] else "No"
            st.write(f"Sample {i+1}: {sample} => Play Tennis: **{result}**")

else:
    st.warning("📂 Please upload a dataset JSON file to continue.")
