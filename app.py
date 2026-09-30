import streamlit as st
import pandas as pd
from itertools import combinations
import io
import textwrap


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
# HELPER FUNCTION FOR HTML
# ============================================================

def render_html(html):
    """
    Safely render HTML inside Streamlit without
    showing the HTML source code as text.
    """
    st.markdown(
        textwrap.dedent(html).strip(),
        unsafe_allow_html=True
    )


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ========================================================
   MAIN PAGE
======================================================== */

.stApp {
    background:
    linear-gradient(
        135deg,
        #f5f7ff,
        #faf7ff
    );
}


/* ========================================================
   HEADER
======================================================== */

.hero {
    padding: 45px 30px;
    border-radius: 25px;
    text-align: center;

    background:
    linear-gradient(
        135deg,
        #eef2ff,
        #f5f3ff
    );

    border: 1px solid #ddd6fe;
    margin-bottom: 30px;

    box-shadow:
    0 10px 35px rgba(79, 70, 229, 0.10);
}

.hero-icon {
    font-size: 60px;
    margin-bottom: 10px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #312e81;
    margin-bottom: 10px;
}

.hero-title span {
    color: #4f46e5;
}

.hero-description {
    font-size: 17px;
    color: #64748b;
    max-width: 800px;
    margin: auto;
    line-height: 1.7;
}


/* ========================================================
   INFORMATION CARDS
======================================================== */

.info-card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    text-align: center;

    border: 1px solid #e5e7eb;

    box-shadow:
    0 8px 25px rgba(0, 0, 0, 0.05);

    min-height: 150px;
}

.info-icon {
    font-size: 32px;
}

.info-number {
    font-size: 30px;
    font-weight: 800;
    color: #4f46e5;
    margin: 5px;
}

.info-label {
    color: #64748b;
    font-size: 14px;
}


/* ========================================================
   SECTION HEADINGS
======================================================== */

.section-title {
    color: #312e81;
    font-size: 28px;
    font-weight: 750;
    margin-top: 20px;
    margin-bottom: 8px;
}

.section-description {
    color: #64748b;
    margin-bottom: 20px;
}


/* ========================================================
   INSIGHT BOX
======================================================== */

.insight-box {
    background: #f8fafc;
    border-left: 5px solid #4f46e5;
    padding: 15px 18px;
    border-radius: 10px;
    margin-bottom: 12px;
    color: #374151;
    line-height: 1.6;
}


/* ========================================================
   FOOTER
======================================================== */

.footer {
    text-align: center;
    padding: 30px;
    margin-top: 40px;
    color: #64748b;
}


/* ========================================================
   SIDEBAR
======================================================== */

section[data-testid="stSidebar"] {
    background: #ffffff;
}


/* ========================================================
   BUTTON
======================================================== */

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}


/* ========================================================
   METRICS
======================================================== */

[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
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
# FUNCTION — GET UNIQUE PRODUCTS
# ============================================================

def get_unique_products(transactions):

    products = set()

    for basket in transactions:
        for product in basket:
            products.add(product)

    return sorted(list(products))


# ============================================================
# FUNCTION — CALCULATE ASSOCIATION RULES
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

    # --------------------------------------------------------
    # Count frequency of each product
    # --------------------------------------------------------

    product_frequency = {}

    for product in products:

        count = 0

        for basket in transactions:

            if product in basket:
                count += 1

        product_frequency[product] = count

    # --------------------------------------------------------
    # Create empty list for rules
    # --------------------------------------------------------

    rules = []

    # --------------------------------------------------------
    # Compare every product pair
    # --------------------------------------------------------

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

        # ----------------------------------------------------
        # SUPPORT
        # ----------------------------------------------------

        support = (
            pair_count /
            total_transactions
        )

        # ----------------------------------------------------
        # Confidence A -> B
        # ----------------------------------------------------

        if product_frequency[product_a] > 0:

            confidence_a_to_b = (
                pair_count /
                product_frequency[product_a]
            )

        else:

            confidence_a_to_b = 0

        # ----------------------------------------------------
        # Confidence B -> A
        # ----------------------------------------------------

        if product_frequency[product_b] > 0:

            confidence_b_to_a = (
                pair_count /
                product_frequency[product_b]
            )

        else:

            confidence_b_to_a = 0

        # ----------------------------------------------------
        # Support of A
        # ----------------------------------------------------

        support_a = (
            product_frequency[product_a] /
            total_transactions
        )

        # ----------------------------------------------------
        # Support of B
        # ----------------------------------------------------

        support_b = (
            product_frequency[product_b] /
            total_transactions
        )

        # ----------------------------------------------------
        # Lift A -> B
        # ----------------------------------------------------

        if support_b > 0:

            lift_a_to_b = (
                confidence_a_to_b /
                support_b
            )

        else:

            lift_a_to_b = 0

        # ----------------------------------------------------
        # Lift B -> A
        # ----------------------------------------------------

        if support_a > 0:

            lift_b_to_a = (
                confidence_b_to_a /
                support_a
            )

        else:

            lift_b_to_a = 0

        # ----------------------------------------------------
        # Rule A -> B
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Rule B -> A
        # ----------------------------------------------------

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

    # --------------------------------------------------------
    # Sort rules by highest Lift
    # --------------------------------------------------------

    rules.sort(
        key=lambda x: x["Lift"],
        reverse=True
    )

    return pd.DataFrame(rules)


# ============================================================
# FUNCTION — READ CSV
# ============================================================

def read_csv_file(uploaded_file):

    try:

        dataframe = pd.read_csv(uploaded_file)

        # Convert column names to lowercase
        columns = {
            column.lower().strip(): column
            for column in dataframe.columns
        }

        # ----------------------------------------------------
        # Find transaction column
        # ----------------------------------------------------

        transaction_column = None

        if "transactionid" in columns:

            transaction_column = (
                columns["transactionid"]
            )

        elif "transaction" in columns:

            transaction_column = (
                columns["transaction"]
            )

        elif "transaction_id" in columns:

            transaction_column = (
                columns["transaction_id"]
            )

        # ----------------------------------------------------
        # Find product column
        # ----------------------------------------------------

        product_column = None

        if "product" in columns:

            product_column = (
                columns["product"]
            )

        elif "item" in columns:

            product_column = (
                columns["item"]
            )

        # ----------------------------------------------------
        # Validate columns
        # ----------------------------------------------------

        if (
            transaction_column is None
            or
            product_column is None
        ):

            st.error(
                "CSV must contain "
                "'TransactionID' and 'Product' columns."
            )

            return None

        # ----------------------------------------------------
        # Create baskets
        # ----------------------------------------------------

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

        # Remove empty baskets
        transactions = [
            basket
            for basket in transactions
            if len(basket) > 0
        ]

        return transactions

    except Exception as error:

        st.error(
            f"Could not read CSV: {error}"
        )

        return None


# ============================================================
# FUNCTION — CREATE CSV DOWNLOAD
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

render_html(
    """
<div class="hero">

    <div class="hero-icon">
        🛒📊
    </div>

    <div class="hero-title">
        Retail Product
        <span>Association Analysis</span>
    </div>

    <div class="hero-description">
        Analyze shopping transactions and discover
        which products are frequently purchased together.

        The system uses Association Rule Mining to calculate
        Support, Confidence and Lift.
    </div>

</div>
"""
)


# ============================================================
# SIDEBAR — DATASET + SETTINGS
# ============================================================

with st.sidebar:

    st.header("⚙️ Analysis Settings")

    st.markdown("### 📁 Dataset")

    uploaded_file = st.file_uploader(
        "Upload your CSV file",
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

    st.markdown("### 🎯 Minimum Support")

    support_percent = st.slider(
        "Minimum Support (%)",
        min_value=1,
        max_value=100,
        value=20
    )

    minimum_support = (
        support_percent / 100
    )

    st.markdown("### 🎯 Minimum Confidence")

    confidence_percent = st.slider(
        "Minimum Confidence (%)",
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
# DATASET INFORMATION
# ============================================================

unique_products = get_unique_products(
    transactions
)

render_html(
    """
<div class="section-title">
    📁 Dataset Overview
</div>

<div class="section-description">
    Current retail transaction dataset used for analysis.
</div>
"""
)


# ============================================================
# INFORMATION CARDS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    render_html(
        f"""
<div class="info-card">

    <div class="info-icon">
        🛍️
    </div>

    <div class="info-number">
        {len(transactions)}
    </div>

    <div class="info-label">
        Total Transactions
    </div>

</div>
"""
    )


with col2:

    render_html(
        f"""
<div class="info-card">

    <div class="info-icon">
        📦
    </div>

    <div class="info-number">
        {len(unique_products)}
    </div>

    <div class="info-label">
        Unique Products
    </div>

</div>
"""
    )


with col3:

    render_html(
        """
<div class="info-card">

    <div class="info-icon">
        🤖
    </div>

    <div class="info-number">
        Ready
    </div>

    <div class="info-label">
        Association Analysis
    </div>

</div>
"""
    )


# ============================================================
# SHOW DATASET
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
# RUN ANALYSIS
# ============================================================

results = calculate_association_rules(
    transactions,
    minimum_support,
    minimum_confidence
)


# ============================================================
# ANALYSIS RESULTS HEADING
# ============================================================

render_html(
    """
<div class="section-title">
    📊 Analysis Dashboard
</div>

<div class="section-description">
    Product relationships discovered from shopping transactions.
</div>
"""
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
# RESULTS TABLE
# ============================================================

st.markdown("### 🔗 Product Associations")


if total_rules == 0:

    st.warning(
        """
No association rules were found with the
current Support and Confidence settings.

Try lowering the minimum values.
"""
    )

else:

    # --------------------------------------------------------
    # Search
    # --------------------------------------------------------

    search = st.text_input(
        "🔎 Search Product",
        placeholder="Example: Milk"
    )

    filtered_results = results.copy()

    if search:

        search_lower = search.lower()

        filtered_results = (
            filtered_results[
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
        )

    # --------------------------------------------------------
    # Format values for display
    # --------------------------------------------------------

    display_results = (
        filtered_results.copy()
    )

    display_results["Support"] = (
        display_results["Support"] * 100
    ).round(2).astype(str) + "%"

    display_results["Confidence"] = (
        display_results["Confidence"] * 100
    ).round(2).astype(str) + "%"

    display_results["Lift"] = (
        display_results["Lift"].round(2)
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

    # --------------------------------------------------------
    # DOWNLOAD BUTTON
    # --------------------------------------------------------

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

st.markdown("### 💡 Business Insights")


if total_rules == 0:

    render_html(
        """
<div class="insight-box">

    ⚠️ No strong product relationships
    were found with the current settings.

</div>

<div class="insight-box">

    💡 Try reducing Minimum Support or
    Minimum Confidence to discover more rules.

</div>
"""
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

        render_html(
            f"""
<div class="insight-box">

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
"""
        )


# ============================================================
# TOP ASSOCIATION CHART
# ============================================================

st.markdown("### 📈 Top Product Associations")


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
# EXPLANATION OF METRICS
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

render_html(
    """
<div class="footer">

    <h3>
        🛒 RetailAI
    </h3>

    <p>
        Retail Product Association Analysis
    </p>

    <p>
        Built with Python + Streamlit
    </p>

</div>
"""
)
