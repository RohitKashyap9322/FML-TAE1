import streamlit as st
import pandas as pd
from itertools import combinations
import io


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RetailAI | Product Association Analysis",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: linear-gradient(135deg, #f8faff 0%, #f5f3ff 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(135deg, #312e81, #4f46e5, #7c3aed);
        padding: 45px 35px;
        border-radius: 28px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 15px 40px rgba(79, 70, 229, 0.25);
    }

    .hero-icon {
        font-size: 58px;
        margin-bottom: 10px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 12px;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 17px;
        line-height: 1.7;
        max-width: 850px;
        margin: auto;
        opacity: 0.92;
    }

    /* ---------- CARDS ---------- */

    .metric-card {
        background: white;
        padding: 24px 15px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
        min-height: 145px;
    }

    .metric-icon {
        font-size: 30px;
    }

    .metric-value {
        font-size: 29px;
        font-weight: 800;
        color: #4f46e5;
        margin-top: 6px;
    }

    .metric-label {
        color: #64748b;
        font-size: 14px;
        margin-top: 4px;
    }

    /* ---------- SECTION ---------- */

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #312e81;
        margin-top: 35px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #64748b;
        font-size: 15px;
        margin-bottom: 20px;
    }

    /* ---------- INSIGHT ---------- */

    .insight {
        background: white;
        padding: 18px 20px;
        border-radius: 15px;
        border-left: 5px solid #4f46e5;
        margin-bottom: 12px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
        color: #374151;
        line-height: 1.6;
    }

    /* ---------- FEATURE ---------- */

    .feature-card {
        background: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        height: 100%;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
    }

    .feature-icon {
        font-size: 32px;
        margin-bottom: 8px;
    }

    .feature-title {
        color: #312e81;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .feature-text {
        color: #64748b;
        font-size: 14px;
        line-height: 1.6;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        margin-top: 50px;
        padding: 30px;
        color: #64748b;
        border-top: 1px solid #e5e7eb;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# BUILT-IN RETAIL DATASET
# ============================================================

BUILT_IN_DATASET = [
    ["Milk", "Bread", "Butter"],
    ["Milk", "Bread"],
    ["Milk", "Eggs"],
    ["Bread", "Butter"],
    ["Milk", "Bread", "Eggs"],
    ["Bread", "Butter", "Jam"],
    ["Milk", "Bread", "Butter"],
    ["Milk", "Eggs"],
    ["Bread", "Butter"],
    ["Milk", "Bread", "Jam"],
    ["Milk", "Bread", "Butter"],
    ["Bread", "Eggs"],
    ["Milk", "Bread"],
    ["Milk", "Butter"],
    ["Bread", "Butter", "Jam"],
    ["Milk", "Bread", "Eggs"],
    ["Milk", "Bread"],
    ["Bread", "Butter"],
    ["Milk", "Eggs", "Butter"],
    ["Milk", "Bread", "Butter"],
    ["Coffee", "Sugar"],
    ["Coffee", "Milk"],
    ["Coffee", "Sugar", "Milk"],
    ["Tea", "Sugar"],
    ["Tea", "Milk"],
    ["Coffee", "Biscuits"],
    ["Coffee", "Milk", "Sugar"],
    ["Tea", "Biscuits"],
    ["Milk", "Bread", "Butter"],
    ["Coffee", "Sugar", "Biscuits"],
]


# ============================================================
# GET UNIQUE PRODUCTS
# ============================================================

def get_unique_products(transactions):

    products = set()

    for basket in transactions:
        for product in basket:
            products.add(product)

    return sorted(products)


# ============================================================
# ASSOCIATION RULE CALCULATION
# ============================================================

def calculate_association_rules(
    transactions,
    minimum_support,
    minimum_confidence
):

    total_transactions = len(transactions)

    if total_transactions == 0:
        return pd.DataFrame(
            columns=[
                "Product A",
                "Product B",
                "Support",
                "Confidence",
                "Lift"
            ]
        )

    products = get_unique_products(transactions)

    product_frequency = {}

    for product in products:

        product_frequency[product] = sum(
            1
            for basket in transactions
            if product in basket
        )

    rules = []

    for product_a, product_b in combinations(products, 2):

        pair_count = sum(
            1
            for basket in transactions
            if product_a in basket and product_b in basket
        )

        support = pair_count / total_transactions

        if pair_count == 0:
            continue

        confidence_a_to_b = (
            pair_count /
            product_frequency[product_a]
        )

        confidence_b_to_a = (
            pair_count /
            product_frequency[product_b]
        )

        support_a = (
            product_frequency[product_a] /
            total_transactions
        )

        support_b = (
            product_frequency[product_b] /
            total_transactions
        )

        lift_a_to_b = (
            confidence_a_to_b / support_b
            if support_b > 0 else 0
        )

        lift_b_to_a = (
            confidence_b_to_a / support_a
            if support_a > 0 else 0
        )

        # A -> B

        if (
            support >= minimum_support
            and
            confidence_a_to_b >= minimum_confidence
        ):

            rules.append({
                "Product A": product_a,
                "Product B": product_b,
                "Support": support,
                "Confidence": confidence_a_to_b,
                "Lift": lift_a_to_b
            })

        # B -> A

        if (
            support >= minimum_support
            and
            confidence_b_to_a >= minimum_confidence
        ):

            rules.append({
                "Product A": product_b,
                "Product B": product_a,
                "Support": support,
                "Confidence": confidence_b_to_a,
                "Lift": lift_b_to_a
            })

    rules.sort(
        key=lambda item: item["Lift"],
        reverse=True
    )

    return pd.DataFrame(rules)


# ============================================================
# CSV READER
# ============================================================

def read_csv_file(uploaded_file):

    try:

        dataframe = pd.read_csv(uploaded_file)

        normalized_columns = {
            column.lower().strip(): column
            for column in dataframe.columns
        }

        transaction_column = None
        product_column = None

        if "transactionid" in normalized_columns:
            transaction_column = normalized_columns["transactionid"]

        elif "transaction" in normalized_columns:
            transaction_column = normalized_columns["transaction"]

        if "product" in normalized_columns:
            product_column = normalized_columns["product"]

        elif "item" in normalized_columns:
            product_column = normalized_columns["item"]

        if transaction_column is None or product_column is None:

            st.error(
                "CSV must contain 'TransactionID' and 'Product' columns."
            )

            return None

        transactions = (
            dataframe
            .groupby(transaction_column)[product_column]
            .apply(
                lambda products: list(
                    dict.fromkeys(
                        products
                        .dropna()
                        .astype(str)
                        .str.strip()
                    )
                )
            )
            .tolist()
        )

        return transactions

    except Exception as error:

        st.error(f"Could not read CSV: {error}")

        return None


# ============================================================
# CSV DOWNLOAD
# ============================================================

def create_download_file(results):

    output = io.StringIO()

    results.to_csv(
        output,
        index=False
    )

    return output.getvalue()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-icon">🛒📊</div>

        <div class="hero-title">
            Retail Product Association Analysis
        </div>

        <div class="hero-subtitle">
            Discover which products customers frequently purchase
            together using Support, Confidence and Lift.
            Turn transaction data into actionable retail insights.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Analysis Settings")

    st.markdown("### 📁 Dataset")

    uploaded_file = st.file_uploader(
        "Upload your retail CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        uploaded_transactions = read_csv_file(
            uploaded_file
        )

        if uploaded_transactions:

            transactions = uploaded_transactions

            st.success(
                "CSV loaded successfully!"
            )

        else:

            transactions = BUILT_IN_DATASET

    else:

        transactions = BUILT_IN_DATASET

        st.info(
            "Using built-in retail dataset."
        )

    st.markdown("---")

    st.markdown("### 🎯 Minimum Support")

    support_percent = st.slider(
        "Support (%)",
        min_value=1,
        max_value=100,
        value=20,
        step=1
    )

    minimum_support = support_percent / 100

    st.markdown("### 🎯 Minimum Confidence")

    confidence_percent = st.slider(
        "Confidence (%)",
        min_value=1,
        max_value=100,
        value=30,
        step=1
    )

    minimum_confidence = confidence_percent / 100

    st.markdown("---")

    st.markdown(
        """
        **Dataset format**

        Your CSV should contain:

        `TransactionID`

        `Product`

        Example:

        `1, Milk`

        `1, Bread`

        `2, Eggs`
        """
    )


# ============================================================
# DATASET VARIABLES
# ============================================================

unique_products = get_unique_products(
    transactions
)

results = calculate_association_rules(
    transactions,
    minimum_support,
    minimum_confidence
)

total_rules = len(results)

if total_rules > 0:

    strong_rules = len(
        results[
            results["Lift"] > 1
        ]
    )

else:

    strong_rules = 0


# ============================================================
# OVERVIEW
# ============================================================

st.markdown(
    """
    <div class="section-title">
        📊 Dataset Overview
    </div>

    <div class="section-description">
        A quick overview of the retail data currently being analyzed.
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">🛍️</div>
            <div class="metric-value">{len(transactions)}</div>
            <div class="metric-label">Transactions</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">📦</div>
            <div class="metric-value">{len(unique_products)}</div>
            <div class="metric-label">Unique Products</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">🔗</div>
            <div class="metric-value">{total_rules}</div>
            <div class="metric-label">Association Rules</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">⭐</div>
            <div class="metric-value">{strong_rules}</div>
            <div class="metric-label">Lift > 1 Rules</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FEATURES
# ============================================================

st.markdown(
    """
    <div class="section-title">
        🚀 What This Analysis Provides
    </div>

    <div class="section-description">
        Key metrics used to understand product relationships.
    </div>
    """,
    unsafe_allow_html=True
)


feature1, feature2, feature3 = st.columns(3)


with feature1:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Support</div>
            <div class="feature-text">
                Measures how frequently a product combination
                appears across all customer transactions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with feature2:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Confidence</div>
            <div class="feature-text">
                Shows how often customers purchasing one product
                also purchase the associated product.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with feature3:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Lift</div>
            <div class="feature-text">
                Indicates the strength of association compared
                with what would be expected from individual purchases.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TRANSACTION DATA
# ============================================================

st.markdown(
    """
    <div class="section-title">
        🧾 Transaction Dataset
    </div>

    <div class="section-description">
        The transactions currently used for association analysis.
    </div>
    """,
    unsafe_allow_html=True
)


dataset_rows = []

for transaction_number, basket in enumerate(
    transactions,
    start=1
):

    for product in basket:

        dataset_rows.append({
            "TransactionID": transaction_number,
            "Product": product
        })


dataset_dataframe = pd.DataFrame(
    dataset_rows
)


with st.expander(
    "👀 View complete transaction data"
):

    st.dataframe(
        dataset_dataframe,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# RESULTS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        🔗 Product Associations
    </div>

    <div class="section-description">
        Association rules generated from the selected support
        and confidence thresholds.
    </div>
    """,
    unsafe_allow_html=True
)


if total_rules == 0:

    st.warning(
        "No rules found. Try lowering Support or Confidence."
    )

else:

    search = st.text_input(
        "🔎 Search for a product",
        placeholder="Example: Milk"
    )

    filtered_results = results.copy()

    if search:

        search_lower = search.lower()

        filtered_results = filtered_results[
            filtered_results["Product A"]
            .str.lower()
            .str.contains(search_lower, na=False)
            |
            filtered_results["Product B"]
            .str.lower()
            .str.contains(search_lower, na=False)
        ]

    display_results = filtered_results.copy()

    display_results["Support"] = (
        display_results["Support"] * 100
    ).round(2).astype(str) + "%"

    display_results["Confidence"] = (
        display_results["Confidence"] * 100
    ).round(2).astype(str) + "%"

    display_results["Lift"] = (
        display_results["Lift"]
        .round(2)
    )

    display_results.insert(
        0,
        "#",
        range(1, len(display_results) + 1)
    )

    st.dataframe(
        display_results,
        use_container_width=True,
        hide_index=True
    )

    csv_data = create_download_file(
        filtered_results
    )

    st.download_button(
        label="⬇️ Download Association Results",
        data=csv_data,
        file_name="retail_association_results.csv",
        mime="text/csv"
    )


# ============================================================
# TOP ASSOCIATIONS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        📈 Top Product Associations
    </div>

    <div class="section-description">
        Highest-lift product relationships in the current dataset.
    </div>
    """,
    unsafe_allow_html=True
)


if total_rules > 0:

    chart_data = results.head(8).copy()

    chart_data["Association"] = (
        chart_data["Product A"]
        + " + "
        + chart_data["Product B"]
    )

    chart_data = chart_data.set_index(
        "Association"
    )

    st.bar_chart(
        chart_data["Lift"]
    )

else:

    st.info(
        "No chart available because no association rules were found."
    )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.markdown(
    """
    <div class="section-title">
        💡 Business Insights
    </div>

    <div class="section-description">
        Automatically generated insights from the strongest associations.
    </div>
    """,
    unsafe_allow_html=True
)


if total_rules == 0:

    st.markdown(
        """
        <div class="insight">
            ⚠️ No strong product relationships were found
            with the current settings.
        </div>

        <div class="insight">
            💡 Try lowering the Support or Confidence threshold.
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    top_rules = results.head(5)

    for _, rule in top_rules.iterrows():

        support_text = (
            f"{rule['Support'] * 100:.1f}%"
        )

        confidence_text = (
            f"{rule['Confidence'] * 100:.1f}%"
        )

        lift_text = (
            f"{rule['Lift']:.2f}"
        )

        st.markdown(
            f"""
            <div class="insight">

                <strong>
                    🔗 {rule['Product A']} → {rule['Product B']}
                </strong>

                <br><br>

                Customers who purchase
                <strong>{rule['Product A']}</strong>
                frequently also purchase
                <strong>{rule['Product B']}</strong>.

                <br><br>

                Support:
                <strong>{support_text}</strong>

                &nbsp;&nbsp;|&nbsp;&nbsp;

                Confidence:
                <strong>{confidence_text}</strong>

                &nbsp;&nbsp;|&nbsp;&nbsp;

                Lift:
                <strong>{lift_text}</strong>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# METRIC EXPLANATION
# ============================================================

with st.expander(
    "📚 Understand Support, Confidence and Lift"
):

    st.markdown(
        """
        ### 📈 Support

        Support measures how frequently two products
        appear together in the complete transaction dataset.

        **Support(A,B) = Transactions containing A and B ÷ Total Transactions**

        ---

        ### 🎯 Confidence

        Confidence measures how frequently B is purchased
        when A is purchased.

        **Confidence(A → B) = Transactions containing A and B ÷ Transactions containing A**

        ---

        ### 💡 Lift

        Lift compares the observed relationship between two
        products with what would be expected from their
        individual purchase frequencies.

        **Lift(A → B) = Confidence(A → B) ÷ Support(B)**

        ---

        **Lift > 1:** Positive association

        **Lift = 1:** Approximately independent

        **Lift < 1:** Lower-than-expected co-occurrence
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <h3>🛒 RetailAI</h3>

        <p>
            Retail Product Association Analysis
        </p>

        <p>
            Built with Python + Streamlit
        </p>

    </div>
    """,
    unsafe_allow_html=True
)
