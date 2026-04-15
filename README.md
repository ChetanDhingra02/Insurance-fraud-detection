#  Insurance Fraud Detection System

Insurance fraud is a significant financial problem, costing companies millions every year.  
This project aims to build a machine learning system that not only detects fraudulent claims, but also helps understand the patterns behind them and translates those insights into a usable decision-support tool.

Rather than treating this as a simple classification task, the project approaches fraud detection as a **business problem**, where the cost of missing a fraudulent claim is far greater than incorrectly flagging a legitimate one. This perspective guided every decision in modeling, evaluation, and deployment.

---

##  Understanding the Data

The dataset consists of insurance claims containing customer details, policy information, incident characteristics, and claim amounts. The target variable indicates whether a claim is fraudulent.

During exploratory data analysis, several important patterns emerged.

![Correlation Heatmap](images/correlation.png)

There is strong correlation between claim-related variables such as injury, property, and vehicle claims with total claim amount, indicating some redundancy in financial features.

Another key observation came from analyzing incident severity.

![Incident Severity vs Fraud](images/severity.png)

Fraudulent claims are significantly more common in cases involving major damage or total loss, suggesting that fraud tends to occur in high-impact situations.

These early insights helped guide the modeling approach.

---

##  Modeling Approach

To ensure robustness and reproducibility, a full preprocessing pipeline was built using scikit-learn. Numerical features were imputed and scaled, while categorical variables were encoded using one-hot encoding.

Three models were trained and compared:

- Logistic Regression as a baseline
- Random Forest for capturing non-linear relationships
- XGBoost as an advanced boosting method

The performance of these models was evaluated using ROC curves.

![ROC Curve](images/roc.png)

All models performed similarly, with Random Forest slightly outperforming others. Given its balance of performance and interpretability, Random Forest was selected for further optimization.

---

##  Threshold Tuning and Business Trade-offs

A critical part of this project was moving beyond default model settings.

By default, classification models use a threshold of 0.5. However, this resulted in poor fraud detection, missing a large number of fraudulent cases.

Different thresholds were tested to better align the model with business priorities. Lowering the threshold significantly improved recall, meaning more fraud cases were correctly identified.

At a threshold of **0.25**, the model achieved the best balance between detecting fraud and maintaining reasonable accuracy.

![Confusion Matrix](images/confusion.png)

This step highlights a key insight:  
**Model performance is not just about accuracy, but about choosing the right trade-off for the problem.**

---

##  Model Interpretability

Understanding *why* the model makes predictions is just as important as the predictions themselves.

Feature importance analysis from the Random Forest model revealed the most influential variables.

![Feature Importance](images/importance.png)

The model heavily relies on:
- Incident severity
- Claim amounts
- Incident-related features

To go deeper, SHAP (SHapley Additive exPlanations) was used with the XGBoost model.

![SHAP Summary](images/shap.png)

SHAP provides insight into how each feature influences predictions. It also revealed some unexpected patterns (such as certain categorical variables appearing important), highlighting the possibility of spurious correlations and reinforcing the need for careful interpretation.

---

##  Key Insights

From the analysis, several consistent patterns emerged:

- Fraud is more likely in high-value claims  
- Severe incidents are strong indicators of fraud  
- Claims involving multiple vehicles, injuries, or witnesses tend to be more suspicious  

These insights align well with real-world intuition and demonstrate that the model is capturing meaningful patterns.

---

##  Deployment as a Real-World Tool

While the original model used many features, it was not practical for deployment due to the complexity of input requirements.

To address this, a **simplified deployment model** was created using a reduced set of important features. This allowed the system to remain effective while significantly improving usability.

The final model was deployed as an interactive Streamlit application.

![App Screenshot](images/app.png)

The application allows users to:
- Enter claim and incident details  
- View fraud probability in real time  
- See risk classification (Low, Medium, High)  
- Receive recommended actions (process, review, investigate)  
- Understand key risk drivers behind the prediction  

This transforms the model from a theoretical exercise into a **practical decision-support system**.

---

##  Technologies Used

- Python  
- Pandas & NumPy  
- Scikit-learn  
- XGBoost  
- SHAP  
- Streamlit  

---

## Disclaimer

This project is intended as a portfolio demonstration.  
It illustrates how machine learning can support fraud detection, but it is not a replacement for real-world fraud investigation systems.



## Final Thoughts

This project demonstrates more than just building a machine learning model. It shows how to:

- Frame a real-world problem correctly  
- Make data-driven decisions  
- Balance business trade-offs  
- Interpret model behavior  
- Deploy a usable application  

The goal was not just to predict fraud, but to build a system that can **support better decision-making in practice**.
