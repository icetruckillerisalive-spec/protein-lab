import streamlit as st
import pandas as pd
import py3Dmol
import streamlit.components.v1 as components
from pathlib import Path

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

page = st.sidebar.radio(
    "NAVIGATION",
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
        "Length (aa)": 285,
        "Prediction": "Complete",
        "TM-score": 0.9823,
        "RMSD (Å)": 0.843,
    },
    {
        "Protein ID": "21FM",
        "Protein": "Human dUTPase",
        "Length (aa)": 161,
        "Prediction": "Pending",
        "TM-score": None,
        "RMSD (Å)": None,
    },
    {
        "Protein ID": "28NK",
        "Protein": "Phosphopantetheine adenylyltransferase",
        "Length (aa)": 162,
        "Prediction": "Pending",
        "TM-score": None,
        "RMSD (Å)": None,
    },
    {
        "Protein ID": "29LB",
        "Protein": "L-DOPA extradiol dioxygenase",
        "Length (aa)": 278,
        "Prediction": "Pending",
        "TM-score": None,
        "RMSD (Å)": None,
    },
    {
        "Protein ID": "29SV",
        "Protein": "Carbonic anhydrase XII",
        "Length (aa)": 263,
        "Prediction": "Pending",
        "TM-score": None,
        "RMSD (Å)": None,
    },
])

# OVERVIEW
if page == "Overview":
    st.header("Project Overview")

    st.write(
        "Comparative evaluation of computational tools for "
        "3D protein structure prediction using machine learning "
        "and deep learning."
    )

    completed = int(
        (proteins["Prediction"] == "Complete").sum()
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Reference proteins", len(proteins))
    c2.metric("Completed predictions", completed)
    c3.metric("Methods with results", 1)

    st.subheader("Preliminary result — 24FX")

    c1, c2, c3 = st.columns(3)
    c1.metric("TM-score", "0.9823")
    c2.metric("TM-align RMSD", "0.843 Å")
    c3.metric("Sequence length", "285 aa")

    st.caption(
        "Preliminary result for one protein. Additional validation "
        "and assessment of possible template bias are required."
    )

    st.subheader("Protein analysis status")
    st.dataframe(
        proteins,
        use_container_width=True,
        hide_index=True,
    )

# STRUCTURE LAB
elif page == "Structure Lab":
    st.header("3D Protein Structure")

    st.write(
        "Inspect a predicted protein structure by uploading "
        "its PDB file."
    )

    uploaded_pdb = st.file_uploader(
        "Upload predicted PDB structure",
        type=["pdb"],
        key="structure_upload",
    )

    pdb_text = None

    if uploaded_pdb is not None:
        pdb_text = uploaded_pdb.getvalue().decode(
            "utf-8",
            errors="replace",
        )
    else:
        possible_paths = [
            Path("data/24FX_rank_001.pdb"),
            Path("24FX_rank_001.pdb"),
            Path("data/24FX.pdb"),
        ]

        for pdb_path in possible_paths:
            if pdb_path.exists():
                pdb_text = pdb_path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )
                st.success(f"Loaded structure: {pdb_path}")
                break

    if pdb_text:
        has_atoms = any(
            line.startswith(("ATOM  ", "HETATM"))
            for line in pdb_text.splitlines()
        )

        if not has_atoms:
            st.error(
                "This file does not appear to contain "
                "valid PDB atom records."
            )
        else:
            view_style = st.selectbox(
                "Structure representation",
                ["Cartoon", "Stick", "Sphere"],
            )

            color_style = st.selectbox(
                "Color scheme",
                ["Spectrum", "Chain"],
            )

            if view_style == "Cartoon":
                if color_style == "Spectrum":
                    structure_style = {
                        "cartoon": {"color": "spectrum"}
                    }
                else:
                    structure_style = {
                        "cartoon": {"color": "chain"}
                    }
            elif view_style == "Stick":
                structure_style = {"stick": {}}
            else:
                structure_style = {
                    "sphere": {"scale": 0.3}
                }

            viewer = py3Dmol.view(
                width=900,
                height=550,
            )

            viewer.addModel(pdb_text, "pdb")
            viewer.setStyle(structure_style)
            viewer.zoomTo()

            components.html(
                viewer._make_html(),
                height=570,
                scrolling=False,
            )

            st.download_button(
                "Download PDB structure",
                data=pdb_text,
                file_name="protein_structure.pdb",
                mime="chemical/x-pdb",
            )
    else:
        st.info(
            "Upload the 24FX rank-001 PDB file to display "
            "the interactive 3D structure."
        )

    st.caption(
        "The viewer displays supplied coordinates. It does not "
        "perform a new prediction or structural validation."
    )

# PROTEIN LIBRARY
elif page == "Protein Library":
    st.header("Protein Library")

    search = st.text_input(
        "Search by protein ID or name"
    )

    if search:
        filtered = proteins[
            proteins.apply(
                lambda row: search.lower() in " ".join(
                    row.fillna("").astype(str)
                ).lower(),
                axis=1,
            )
        ]
    else:
        filtered = proteins

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
    )

    selected = st.selectbox(
        "Select a protein",
        proteins["Protein ID"].tolist(),
    )

    row = proteins[
        proteins["Protein ID"] == selected
    ].iloc[0]

    st.subheader(row["Protein"])

    c1, c2, c3 = st.columns(3)
    c1.metric("Protein ID", selected)
    c2.metric("Length", f"{row['Length (aa)']} aa")
    c3.metric("Prediction status", row["Prediction"])

    if pd.notna(row["TM-score"]):
        st.metric(
            "Preliminary TM-score",
            f"{row['TM-score']:.4f}",
        )
        st.metric(
            "Preliminary RMSD",
            f"{row['RMSD (Å)']:.3f} Å",
        )
    else:
        st.info(
            "Structural comparison metrics are not available yet."
        )

# METHOD COMPARISON
elif page == "Method Comparison":
    st.header("Prediction Method Comparison")

    methods = pd.DataFrame([
        {
            "Method": "ColabFold / AlphaFold2",
            "Status": "Initial prediction completed for 24FX",
        },
        {
            "Method": "ESMFold",
            "Status": "Not yet evaluated",
        },
        {
            "Method": "MODELLER",
            "Status": "Not yet evaluated",
        },
    ])

    st.dataframe(
        methods,
        use_container_width=True,
        hide_index=True,
    )

    st.warning(
        "A comparative ranking requires results from the same "
        "benchmark proteins and a consistent evaluation protocol."
    )

# PROJECT INFORMATION
elif page == "Project Information":
    st.header("Project Information")

    st.write(
        "**Project title:** Comparative Performance Analysis "
        "of Computational Tools for 3D Protein Structure "
        "Prediction Using Machine Learning and Deep Learning"
    )

    st.write(
        "**Current prediction pipeline:** ColabFold / AlphaFold2"
    )
    st.write("**Initial benchmark:** 24FX")
    st.write("**Structural comparison tool:** TM-align")

    st.subheader("Evaluation plan")

    st.markdown("""
    - Predict structures for the selected reference proteins.
    - Compare predicted and reference structures consistently.
    - Report structural similarity and RMSD with clear definitions.
    - Evaluate confidence scores and computational requirements.
    - Assess possible template or training-data bias.
    """)

    st.subheader("Current limitations")

    st.markdown("""
    - Only one protein prediction has been completed.
    - Additional prediction methods have not yet been evaluated.
    - Sequence-mapped RMSD remains to be calculated.
    - Conclusions are preliminary until the benchmark is complete.
    """)
