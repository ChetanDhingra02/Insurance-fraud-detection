from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from config import MODEL_FILE, TEMPLATE_FILE


@st.cache_resource
def load_artifacts():
    """Load the trained model and input template from files in the repo root."""
    base_dir = Path(__file__).resolve().parent
    model_path = base_dir / MODEL_FILE
    template_path = base_dir / TEMPLATE_FILE

    if not model_path.exists():
        raise FileNotFoundError(f"Missing model file: {model_path.name}")
    if not template_path.exists():
        raise FileNotFoundError(f"Missing input template file: {template_path.name}")

    return joblib.load(model_path), joblib.load(template_path)


def get_template_columns(template, model=None):
    """Infer the exact feature order expected by the trained model."""
    if isinstance(template, pd.DataFrame):
        return list(template.columns)
    if isinstance(template, pd.Series):
        return list(template.index)
    if isinstance(template, dict):
        return list(template.keys())
    if isinstance(template, (list, tuple)):
        return list(template)
    if hasattr(template, "columns"):
        return list(template.columns)
    if model is not None and hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)
    raise ValueError("Could not infer feature columns from deploy_input_template.pkl")


def make_input_dataframe(template, model, values):
    """Create a one-row model input using the template's exact columns/order."""
    columns = get_template_columns(template, model)

    if isinstance(template, pd.DataFrame):
        input_df = template.iloc[[0]].copy() if len(template) > 0 else pd.DataFrame([{col: 0 for col in columns}])
    elif isinstance(template, pd.Series):
        input_df = pd.DataFrame([template.to_dict()])
    elif isinstance(template, dict):
        input_df = pd.DataFrame([template])
    else:
        input_df = pd.DataFrame([{col: 0 for col in columns}])

    for col in columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[columns]

    for key, value in values.items():
        if key in input_df.columns:
            input_df.at[input_df.index[0], key] = value

    if "policy_deductible" in input_df.columns:
        input_df.at[input_df.index[0], "policy_deductible"] = values["policy_deductable"]
    if "policy_deductable" in input_df.columns:
        input_df.at[input_df.index[0], "policy_deductable"] = values["policy_deductable"]

    # Activate matching one-hot columns if the template is already one-hot encoded.
    for categorical_col in ["incident_severity", "incident_type"]:
        selected_value = str(values[categorical_col])
        clean_val = selected_value.lower().replace(" ", "_").replace("-", "_").replace("/", "_")
        for col in input_df.columns:
            clean_col = str(col).lower()
            if categorical_col in clean_col and clean_val in clean_col:
                input_df.at[input_df.index[0], col] = 1

    return input_df


def predict_fraud_probability(model, input_df) -> float:
    """Return probability for the fraud/positive class when possible."""
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_df)
        classes = getattr(model, "classes_", None)
        if classes is None and hasattr(model, "named_steps"):
            final_step = list(model.named_steps.values())[-1]
            classes = getattr(final_step, "classes_", None)

        if classes is not None and 1 in list(classes):
            fraud_index = list(classes).index(1)
        elif probs.shape[1] > 1:
            fraud_index = 1
        else:
            fraud_index = 0

        return float(probs[0][fraud_index])

    pred = model.predict(input_df)[0]
    try:
        return float(pred)
    except Exception:
        return 1.0 if str(pred).lower() in {"1", "true", "fraud", "yes"} else 0.0
