import os, json, joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── Paths ──────────────────────────────────────
DATA_DIR   = "data/processed"
MODEL_DIR  = "models"

FEATURE_LIST = [
    'HighBP','HighChol','CholCheck','BMI','Smoker','Stroke','HeartDiseaseorAttack',
    'PhysActivity','Fruits','Veggies','HvyAlcoholConsump','AnyHealthcare','NoDocbcCost',
    'GenHlth','MentHlth','PhysHlth','DiffWalk','Sex','Age','Education','Income',
    'Obesity','PoorGenHlth','FrequentMentalDistress','FrequentPhysicalDistress'
]

# ── Load data once at startup ──────────────────
def _csv(name):
    try: return pd.read_csv(os.path.join(DATA_DIR, name))
    except: return pd.DataFrame()

prevalence_df   = _csv("disease_prevalence.csv")
cluster_df      = _csv("cluster_summary.csv")
full_df         = _csv("processed_full_data.csv")
rules_df        = _csv("association_rules_diabetes.csv")
try:
    jaccard_df = pd.read_csv(os.path.join(DATA_DIR, "jaccard_matrix.csv"), index_col=0)
except:
    jaccard_df = pd.DataFrame()
importance_df   = _csv("feature_importance.csv")

try:
    with open(os.path.join(DATA_DIR, "model_metrics.json")) as f:
        model_metrics = json.load(f)
except:
    model_metrics = {"accuracy": 0, "roc_auc": 0}

try:
    model_path = os.path.join(MODEL_DIR, "random_forest_model.pkl")
    scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except Exception as e:
    model, scaler = None, None

# ── Helpers ────────────────────────────────────
def is_model_valid(m):
    """Return True only if m is a real sklearn estimator."""
    if m is None: return False
    # If it's a numpy array/list of strings — it's the feature name list bug
    if isinstance(m, (list, np.ndarray)):
        first = m[0] if isinstance(m, list) else m.flat[0]
        if isinstance(first, str): return False
    return hasattr(m, 'predict_proba') or hasattr(m, 'predict')

def heuristic_risk(inputs: dict) -> float:
    flags = [
        inputs.get('HighBP', 0),
        inputs.get('HighChol', 0),
        1 if inputs.get('BMI', 25) >= 30 else 0,
        inputs.get('Smoker', 0),
        1 - inputs.get('PhysActivity', 1),
        1 - inputs.get('Fruits', 1),
        1 - inputs.get('Veggies', 1),
        inputs.get('HvyAlcohol', 0),
        1 if inputs.get('GenHlth', 3) >= 4 else 0,
        inputs.get('DiffWalk', 0),
        1 if inputs.get('Age', 5) >= 9 else 0,
    ]
    return min(sum(flags) / len(flags) * 1.2, 0.99)


# ═══════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════

@app.route('/')
def overview():
    prev_data = []
    for _, r in prevalence_df.sort_values('Prevalence', ascending=False).iterrows():
        prev_data.append({'condition': r['Condition'], 'pct': round(r['Prevalence'] * 100, 1)})

    diabetes_pct  = prevalence_df[prevalence_df['Condition']=='Diabetes_binary']['Prevalence'].values
    hypert_pct    = prevalence_df[prevalence_df['Condition']=='HighBP']['Prevalence'].values
    obesity_pct   = prevalence_df[prevalence_df['Condition']=='Obesity']['Prevalence'].values

    return render_template('overview.html',
        prevalence   = prev_data,
        diabetes_pct = f"{float(diabetes_pct[0])*100:.1f}" if len(diabetes_pct) else "—",
        hypert_pct   = f"{float(hypert_pct[0])*100:.1f}"  if len(hypert_pct)    else "—",
        obesity_pct  = f"{float(obesity_pct[0])*100:.1f}" if len(obesity_pct)   else "—",
        accuracy     = f"{model_metrics.get('accuracy',0)*100:.1f}",
        roc_auc      = f"{model_metrics.get('roc_auc',0):.3f}",
    )


@app.route('/prediction')
def prediction():
    return render_template('prediction.html')


@app.route('/api/predict', methods=['POST'])
def api_predict():
    d = request.json or {}
    yn = lambda k: int(bool(d.get(k, False)))

    bmi      = float(d.get('bmi', 25))
    gen_hlth = int(d.get('gen_hlth', 3))
    age      = int(d.get('age', 5))
    edu      = 6
    income   = 8

    inp = {
        'HighBP': yn('high_bp'), 'HighChol': yn('high_chol'), 'CholCheck': 1,
        'BMI': bmi, 'Smoker': yn('smoker'), 'Stroke': 0, 'HeartDiseaseorAttack': 0,
        'PhysActivity': yn('phys_activity'), 'Fruits': yn('fruits'), 'Veggies': yn('veggies'),
        'HvyAlcoholConsump': yn('hvy_alcohol'), 'AnyHealthcare': 1, 'NoDocbcCost': 0,
        'GenHlth': gen_hlth, 'MentHlth': 0, 'PhysHlth': 0, 'DiffWalk': yn('diff_walk'),
        'Sex': 0, 'Age': age, 'Education': edu, 'Income': income,
        'Obesity': 1 if bmi >= 30 else 0,
        'PoorGenHlth': 1 if gen_hlth >= 4 else 0,
        'FrequentMentalDistress': 0, 'FrequentPhysicalDistress': 0,
    }
    features = [inp.get(f, 0) for f in FEATURE_LIST]

    demo = False
    prob = None
    # Hello
    if is_model_valid(model):
        try:
            prob = float(model.predict_proba([features])[0][1])
        except Exception as e:
            demo = True
    else:
        demo = True

    if demo or prob is None:
        prob = heuristic_risk({**inp, 'HvyAlcohol': yn('hvy_alcohol')})

    if prob < 0.20:
        level = "Low Risk";      color = "low"
        interp = "Your profile suggests a low risk of diabetes. Maintain a healthy lifestyle."
    elif prob < 0.50:
        level = "Moderate Risk"; color = "mod"
        interp = "Moderate risk indicated. Consider consulting a healthcare provider and monitoring your lifestyle."
    else:
        level = "High Risk";     color = "high"
        interp = "High risk of diabetes indicated. Please consult a medical professional promptly."

    return jsonify(prob=round(prob, 4), pct=round(prob*100, 1),
                   level=level, color=color, interp=interp, demo=demo)


@app.route('/clusters')
def clusters():
    profiles = cluster_df.to_dict(orient='records') if not cluster_df.empty else []

    # Scatter sample (JSON for Plotly)
    sample = full_df.sample(min(3000, len(full_df)), random_state=42) if not full_df.empty else pd.DataFrame()
    color_col = 'Cluster' if 'Cluster' in sample.columns else 'Diabetes_binary'
    scatter = []
    if not sample.empty:
        for _, r in sample.iterrows():
            scatter.append({'x': float(r.get('Age',0)),
                            'y': float(r.get('BMI',0)),
                            'g': str(int(r.get(color_col, 0)))})

    return render_template('clusters.html', profiles=profiles, scatter=json.dumps(scatter))


@app.route('/associations')
def associations():
    top_rules = []
    if not rules_df.empty:
        for _, r in rules_df.sort_values('lift', ascending=False).head(10).iterrows():
            top_rules.append({
                'ant': str(r['antecedents'])[:35],
                'con': str(r['consequents'])[:25],
                'sup': round(r['support'], 3),
                'conf': round(r['confidence'], 3),
                'lift': round(r['lift'], 2),
                'hi_lift': r['lift'] > 1.5,
            })

    # Jaccard for heatmap — index_col=0 means rows are labeled, all remaining cols are numeric
    jac = jaccard_df
    if not jac.empty:
        jac_labels = jac.index.tolist()          # row labels (disease names)
        jac_cols   = jac.columns.tolist()        # column labels
        # Ensure all values are float (fill NaN with 0)
        jac_values = jac.fillna(0).astype(float).values.tolist()
    else:
        jac_labels, jac_values, jac_cols = [], [], []

    return render_template('associations.html',
        rules=top_rules,
        jac_labels=json.dumps(jac_labels),
        jac_values=json.dumps(jac_values),
        jac_cols=json.dumps(jac_cols),
    )


@app.route('/importance')
def importance():
    top = importance_df.sort_values('Importance', ascending=False).head(10) if not importance_df.empty else pd.DataFrame()
    max_val = float(top['Importance'].max()) if not top.empty else 1
    features = []
    for rank, (_, r) in enumerate(top.iterrows(), 1):
        features.append({
            'rank': f"{rank:02d}",
            'name': r['Feature'],
            'score': round(r['Importance'], 4),
            'width': round(r['Importance'] / max_val * 100, 1),
        })

    return render_template('importance.html',
        features = features,
        accuracy = f"{model_metrics.get('accuracy',0)*100:.1f}",
        roc_auc  = f"{model_metrics.get('roc_auc',0):.3f}",
    )


if __name__ == '__main__':
    # Use Railway assigned port if available
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
