import streamlit as st
import pandas as pd
import py3Dmol
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PROTEIN//LAB",
    page_icon="🧬",
    layout="wide",
)

st.markdown("""
<style>
.stApp {
    background: #070a12;
    color: #e6f7ff;
}
[data-testid="stSidebar"] {
    background: #0b1220;
    border-right: 1px solid #193749;
}
h1, h2, h3 {
    color: #00e5ff;
}
div[data-testid="stMetric"] {
    background: #101b2a;
    border: 1px solid #214456;
    padding: 18px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("PROTEIN//LAB")
st.caption("COMPUTATIONAL STRUCTURAL BIOINFORMATICS")

st.sidebar.title("NAVIGATION")
page = st.sidebar.radio(
    "Open section",
    [
        "Overview",
        "Structure Lab",
        "Protein Library",
        "Method Comparison",
        "Project Information",
    ],
)

proteins = pd.DataFrame([
    {
        "Protein ID": "24FX",
        "Protein": "Verruculogen synthase",
        "Length": 285,
        "Status": "Prediction complete",
    },
    {
        "Protein ID": "21FM",
        "Protein": "Human dUTPase",
        "Length": 161,
        "Status": "Pending",
    },
    {
        "Protein ID": "28NK",
        "Protein": "Phosphopantetheine adenylyltransferase",
        "Length": 162,
        "Status": "Pending",
    },
    {
        "Protein ID": "29LB",
        "Protein": "L-DOPA extradiol dioxygenase",
        "Length": 278,
        "Status": "Pending",
    },
    {
        "Protein ID": "29SV",
        "Protein": "Carbonic anhydrase XII",
        "Length": 263,
        "Status": "Pending",
    },
])

if page == "Overview":
    st.header("Project Overview")
    st.write(
        "Comparative performance analysis of computational tools "
        "for 3D protein structure prediction using machine learning "
        "and deep learning."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Candidate proteins", "5")
    c2.metric("Completed predictions", "1")
    c3.metric("Methods tested", "1")

    st.subheader("Preliminary result — 24FX")

    c1, c2, c3 = st.columns(3)
    c1.metric("TM-score", "0.9823")
    c2.metric("TM-align RMSD", "0.843 Å")
    c3.metric("Sequence length", "285 aa")

    st.caption(
        "Preliminary structural comparison. Further validation "
        "and leakage assessment remain necessary."
    )

    st.subheader("Protein status")
    st.dataframe(proteins, use_container_width=True, hide_index=True)

elif page == "Structure Lab":
    st.header("3D Protein Structure")
    st.write("Explore the available 24FX predicted structure.")

    st.info(
        "The predicted PDB file must be added to the GitHub repository "
        "before the hosted viewer can load it."
    )

    st.code(
        "results/test_24FX/"
        "24FX_Verruculogen_synthase_unrelaxed_rank_001_"
        "alphafold2_ptm_model_5_seed_000.pdb"
    )

elif page == "Protein Library":
    st.header("Protein Library")

    search = st.text_input("Search by protein ID or name")
    filtered = proteins[
        proteins.apply(
            lambda row: search.lower() in " ".join(
                row.astype(str)
            ).lower(),
            axis=1,
        )
    ] if search else proteins

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
    )

    selected = st.selectbox(
        "Select a protein",
        proteins["Protein ID"].tolist(),
    )

    row = proteins[proteins["Protein ID"] == selected].iloc[0]
    st.subheader(row["Protein"])
    st.write(f"Protein ID: {selected}")
    st.write(f"Sequence length: {row['Length']} amino acids")
    st.write(f"Status: {row['Status']}")

elif page == "Method Comparison":
    st.header("Prediction Method Comparison")

    methods = pd.DataFrame([
        {
            "Method": "ColabFold / AlphaFold2",
            "Status": "One prediction completed",
        },
        {
            "Method": "ESMFold",
            "Status": "Not yet tested",
        },
        {
            "Method": "MODELLER",
            "Status": "Not yet tested",
        },
    ])

    st.dataframe(
        methods,
        use_container_width=True,
        hide_index=True,
    )

    st.warning(
        "A comparative performance ranking cannot be established "
        "until additional experiments have been completed."
    )

elif page == "Project Information":
    st.header("Project Information")

    st.write("**Project:** Protein Structure Prediction and Evaluation")
    st.write("**Primary method tested:** ColabFold / AlphaFold2-based")
    st.write("**Current benchmark protein:** 24FX")
    st.write("**Reference comparison:** TM-align")

    st.subheader("Current limitations")
    st.markdown("""
    - Only one protein prediction has been completed.
    - Additional prediction methods have not yet been evaluated.
    - Sequence-mapped RMSD remains to be calculated.
    - Potential template and training-data leakage needs assessment.
    """)
