import streamlit as st
import pandas as pd
from itertools import combinations
import io


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Product Association Analysis",
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

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #f5f7ff 0%,
            #faf7ff 100%
        );
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff;
    }

    /* Main content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Titles */
    h1, h2, h3 {
        color: #312e81 !important;
    }

    /* Hero container */
    .hero-container {
        background: linear-gradient(
            135deg,
            #eef2ff,
            #f5f3ff
        );
        border: 1px solid #ddd6fe;
        border-radius: 25px;
        padding: 40px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 35px rgba(79, 70, 229, 0.10);
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #312e81;
        margin-bottom: 10px;
    }

    .hero-title-highlight {
        color: #4f46e5;
    }

    .hero-description {
        font-size: 17px;
        color: #64748b;
        line-height: 1.7;
        max-width: 850px;
        margin: auto;
    }

    /* Cards */
    .card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
        min-height: 150px;
    }

    .card-icon {
        font-size: 34px;
    }

    .card-number {
        font-size: 30px;
        font-weight: 800;
        color: #4f46e5;
        margin-top: 8px;
    }

    .card-label {
        color: #64748b;
        font-size: 14px;
        margin-top: 5px;
    }

    /* Insight cards */
    .insight-card {
        background: #f8fafc;
        border-left: 5px solid #4f46e5;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 12px;
        color: #374151;
        line-height: 1.6;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #64748b;
        padding: 30px;
        margin-top: 40px;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        width: 100%;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.04);
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
    ["Coffee", "Sugar", "Biscuits"]
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

        count = 0

        for basket in transactions:

            if product in basket:
                count += 1

        product_frequency[product] = count

    rules = []

    for product_a, product_b in combinations(products, 2):

        pair_count = 0

        for basket in transactions:

            if (
                product_a in basket
                and
                product_b in basket
            ):
                pair_count += 1

        if pair_count == 0:
            continue

        support = (
            pair_count /
            total_transactions
        )

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
            confidence_a_to_b /
            support_b
        )

        lift_b_to_a = (
            confidence_b_to_a /
            support_a
        )

        if (
            support >= minimum_support
            and
            confidence_a_to_b >= minimum_confidence
        ):

            rules.append(
                {
                    "Product A": product_a,
                    "Product B": product_b,
                    "Support": support,
                    "Confidence": confidence_a_to_b,
                    "Lift": lift_a_to_b
                }
            )

        if (
            support >= minimum_support
            and
            confidence_b_to_a >= minimum_confidence
        ):

            rules.append(
                {
                    "Product A": product_b,
                    "Product B": product_a,
                    "Support": support,
                    "Confidence": confidence_b_to_a,
                    "Lift": lift_b_to_a
                }
            )

    rules.sort(
        key=lambda item: item["Lift"],
        reverse=True
    )

    return pd.DataFrame(rules)


# ============================================================
# READ CSV
# ============================================================

def read_csv_file(uploaded_file):

    try:

        dataframe = pd.read_csv(uploaded_file)

        columns = {
            column.lower().strip(): column
            for column in dataframe.columns
        }

        transaction_column = None

        if "transactionid" in columns:
            transaction_column = columns["transactionid"]

        elif "transaction" in columns:
            transaction_column = columns["transaction"]

        elif "transaction_id" in columns:
            transaction_column = columns["transaction_id"]

        product_column = None

        if "product" in columns:
            product_column = columns["product"]

        elif "item" in columns:
            product_column = columns["item"]

        if (
            transaction_column is None
            or
            product_column is None
        ):

            st.error(
                "CSV must contain 'TransactionID' and 'Product' columns."
            )

            return None

        transactions = (
            dataframe
            .groupby(transaction_column)[product_column]
            .apply(
                lambda products:
                list(
                    set(
                        products
                        .dropna()
                        .astype(str)
                        .str.strip()
                    )
                )
            )
            .tolist()
        )

        transactions = [
            basket
            for basket in transactions
            if basket
        ]

        return transactions

    except Exception as error:

        st.error(
            f"Could not read CSV: {error}"
        )

        return None


# ============================================================
# CREATE DOWNLOAD FILE
# ============================================================

def create_download_file(results):

    output = io.StringIO()

    results.to_csv(
        output,
        index=False
    )

    return output.getvalue()


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    """
    <div class="hero-container">

        <div style="font-size:60px;">
            🛒📊
        </div>

        <div class="hero-title">
            Retail Product
            <span class="hero-title-highlight">
                Association Analysis
            </span>
        </div>

        <div class="hero-description">
            Analyze shopping transactions and discover
            which products are frequently purchased together.
            The system uses Association Rule Mining to calculate
            Support, Confidence and Lift.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Analysis Settings")

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
        value=20
    )

    minimum_support = (
        support_percent / 100
    )

    st.markdown("### 🎯 Minimum Confidence")

    confidence_percent = st.slider(
        "Confidence (%)",
        min_value=1,
        max_value=100,
        value=30
    )

    minimum_confidence = (
        confidence_percent / 100
    )

    st.markdown("---")

    analyze_button = st.button(
        "🔍 Analyze Transactions",
        use_container_width=True
    )


# ============================================================
# DATASET OVERVIEW
# ============================================================

unique_products = get_unique_products(
    transactions
)

st.header("📁 Dataset Overview")

st.caption(
    "A quick overview of the retail data currently being analyzed."
)

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <div class="card">

            <div class="card-icon">
                🛍️
            </div>

            <div class="card-number">
                {len(transactions)}
            </div>

            <div class="card-label">
                Total Transactions
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="card">

            <div class="card-icon">
                📦
            </div>

            <div class="card-number">
                {len(unique_products)}
            </div>

            <div class="card-label">
                Unique Products
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="card">

            <div class="card-icon">
                🤖
            </div>

            <div class="card-number">
                Ready
            </div>

            <div class="card-label">
                Association Analysis
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TRANSACTION DATASET
# ============================================================

with st.expander(
    "👀 View Transaction Dataset"
):

    dataset_rows = []

    for transaction_number, basket in enumerate(
        transactions,
        start=1
    ):

        for product in basket:

            dataset_rows.append(
                {
                    "TransactionID":
                        transaction_number,
                    "Product":
                        product
                }
            )

    dataset_dataframe = pd.DataFrame(
        dataset_rows
    )

    st.dataframe(
        dataset_dataframe,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ANALYSIS
# ============================================================

results = calculate_association_rules(
    transactions,
    minimum_support,
    minimum_confidence
)


# ============================================================
# ANALYSIS DASHBOARD
# ============================================================

st.header("📊 Analysis Dashboard")

st.caption(
    "Product relationships discovered from shopping transactions."
)


# ============================================================
# STATISTICS
# ============================================================

total_rules = len(results)

if total_rules > 0:

    strong_rules = len(
        results[
            results["Lift"] > 1
        ]
    )

else:

    strong_rules = 0


stat1, stat2, stat3, stat4 = st.columns(4)


with stat1:

    st.metric(
        "🛍️ Transactions",
        len(transactions)
    )


with stat2:

    st.metric(
        "📦 Products",
        len(unique_products)
    )


with stat3:

    st.metric(
        "🔗 Association Rules",
        total_rules
    )


with stat4:

    st.metric(
        "⭐ Lift > 1 Rules",
        strong_rules
    )


# ============================================================
# PRODUCT ASSOCIATIONS
# ============================================================

st.subheader("🔗 Product Associations")


if total_rules == 0:

    st.warning(
        """
        No association rules were found with the
        current Support and Confidence settings.

        Try lowering the minimum values.
        """
    )

else:

    search = st.text_input(
        "🔎 Search Product",
        placeholder="Example: Milk"
    )

    filtered_results = results.copy()

    if search:

        search_lower = search.lower()

        filtered_results = filtered_results[
            filtered_results["Product A"]
            .str.lower()
            .str.contains(
                search_lower,
                na=False
            )
            |
            filtered_results["Product B"]
            .str.lower()
            .str.contains(
                search_lower,
                na=False
            )
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
        range(
            1,
            len(display_results) + 1
        )
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
        label="⬇️ Download Results as CSV",
        data=csv_data,
        file_name="retail_association_results.csv",
        mime="text/csv"
    )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.subheader("💡 Business Insights")

st.caption(
    "Automatically generated insights from the strongest associations."
)


if total_rules == 0:

    st.info(
        "No strong product relationships were found with the current settings."
    )

    st.info(
        "Try reducing Minimum Support or Minimum Confidence."
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
            <div class="insight-card">

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

                &nbsp; | &nbsp;

                Confidence:
                <strong>{confidence_text}</strong>

                &nbsp; | &nbsp;

                Lift:
                <strong>{lift_text}</strong>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# TOP ASSOCIATION CHART
# ============================================================

st.subheader("📈 Top Product Associations")


if total_rules > 0:

    chart_data = (
        results
        .head(8)
        .copy()
    )

    chart_data["Association"] = (
        chart_data["Product A"]
        + " + "
        + chart_data["Product B"]
    )

    chart_data = chart_data.set_index(
        "Association"
    )

    st.bar_chart(
        chart_data[["Lift"]]
    )

else:

    st.info(
        "No chart available because no rules were found."
    )


# ============================================================
# METRIC EXPLANATION
# ============================================================

with st.expander(
    "📚 Understand Support, Confidence and Lift"
):

    st.markdown(
        """
        ### Support

        Support tells us how frequently two products
        appear together in all transactions.

        **Formula:**

        Support(A,B) =
        Transactions containing A and B
        ÷
        Total Transactions


        ### Confidence

        Confidence tells us how often Product B is
        purchased when Product A is purchased.

        **Formula:**

        Confidence(A → B) =
        Transactions containing A and B
        ÷
        Transactions containing A


        ### Lift

        Lift measures how strongly two products
        are associated compared with their individual
        purchase frequencies.

        **Formula:**

        Lift(A → B) =
        Confidence(A → B)
        ÷
        Support(B)


        ### Interpretation

        **Lift > 1**

        The products have a positive association
        in the analyzed dataset.


        **Lift = 1**

        The products behave approximately independently.


        **Lift < 1**

        The products occur together less often than
        expected from their individual frequencies.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    "---"
)

st.markdown(
    """
    <div class="footer-text">

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
