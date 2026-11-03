import pandas as pd
import pickle as pk
import streamlit as st

st.set_page_config(
    page_title="Bangalore House Price Predictor",
    page_icon="🏠",
    layout="centered"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
/* Static background */
.stApp{
    background: linear-gradient(135deg, #0f172a, #1e293b, #2563eb);
}

/* Main glass card */
.main-card{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
    border-radius:20px;
    padding:30px;
    box-shadow:0 8px 32px rgba(0,0,0,.35);
}

/* Header */
h1{
    text-align:center;
    color:white !important;
    font-size:40px;
}

/* Labels */
label{
    color:white !important;
    font-weight:600;
}

/* Rounded input fields */
div[data-baseweb="select"],
div[data-baseweb="input"]{
    border-radius:12px;
}

/* Button */
.stButton>button{
    width:100%;
    background:linear-gradient(90deg,#ff512f,#dd2476);
    color:white;
    border:none;
    border-radius:15px;
    padding:14px;
    font-size:18px;
    font-weight:bold;
    box-shadow:0 0 15px rgba(255,82,47,.4);
    transition:all .25s ease;
}

/* Hover effect */
.stButton>button:hover{
    transform:translateY(-3px) scale(1.02);
    box-shadow:0 0 25px rgba(255,82,47,.8);
}

/* Click effect */
.stButton>button:active{
    transform:scale(.96);
}

/* Result card */
.result-card{
    background:linear-gradient(135deg,#00c853,#64dd17);
    color:white;
    padding:22px;
    border-radius:18px;
    text-align:center;
    margin-top:20px;
    animation: popIn .8s cubic-bezier(.18,.89,.32,1.28);
}

/* Pop animation */
@keyframes popIn{
    0%{
        opacity:0;
        transform:translateY(40px) scale(.85);
    }
    60%{
        opacity:1;
        transform:translateY(-8px) scale(1.03);
    }
    100%{
        transform:translateY(0) scale(1);
    }
}

/* Price pulse animation */
.result-card h1{
    animation:pulse 1.4s ease-in-out infinite alternate;
}

@keyframes pulse{
    from{
        transform:scale(1);
        text-shadow:0 0 5px rgba(255,255,255,.4);
    }
    to{
        transform:scale(1.05);
        text-shadow:0 0 18px rgba(255,255,255,.8);
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- MODEL ----------
model = pk.load(open('House_prediction_model.pkl','rb'))
data = pd.read_csv('Cleaned_data.csv')

# ---------- UI ----------

st.markdown("""
    <div class='main-card'>
        <h1>🏠 Bangalore House Price Predictor</h1>
        <p style='text-align:center;color:#e2e8f0;'>Estimate your property's price instantly using Machine Learning</p>
        """
    ,unsafe_allow_html=True
)

st.divider()

# Inputs
loc = st.selectbox("📍 Choose Location", sorted(data['location'].unique()))

sqft = st.number_input("📐 Enter Total Sqft", min_value=100, value=1000)
beds = st.number_input("🛏 Enter No. of Bedrooms", min_value=1, value=2)
bath = st.number_input("🚿 Enter No. of Bathrooms", min_value=1, value=2)
balc = st.number_input("🌿 Enter No. of Balconies", min_value=0, value=1)

st.divider()

# Input dataframe
input_df = pd.DataFrame(
    [[loc, sqft, bath, balc, beds]],
    columns=['location', 'total_sqft', 'bath', 'balcony', 'bedroom']
)

# Prediction
if st.button("✨ Predict Price"):
    with st.spinner("Calculating property value..."):
        output = model.predict(input_df)

    st.balloons()
    import locale
    try: 
        locale.setlocale(locale.LC_ALL,'en_IN')
    except locale.Error:
        locale.setlocale(locale.LC_ALL,'hi_IN')

    amount = locale.currency(output[0]*100000,grouping=True)

    st.html(f"""
    <div class='result-card'>
        <h2>Estimated Price</h2>
        <h1> {amount}</h1>
        <p>Your dream home's estimated market value.</p>
    </div>
    """)


st.markdown("</div>", unsafe_allow_html=True)  # Close main-card div