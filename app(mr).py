import streamlit as st
import pandas as pd
from io import BytesIO

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MDC Multi Rack Customization",
    page_icon="🏭",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("🏭 MDC – Multi Rack Customization")

st.markdown(
    """
    Configure a **Multi Rack MDC** according to the customer's
    requirements.

    **Customization workflow only**
    """
)

st.divider()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def utility_rack_from_quantity(rack_quantity):
    """
    Utility Rack rule:

    1–3 Server Racks  -> 600
    More than 3       -> 800
    """

    if rack_quantity <= 3:
        return "600"
    else:
        return "800"


def create_bom_excel(bom_df):
    """
    Creates Excel file containing the customized BOM.
    """

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        bom_df.to_excel(
            writer,
            index=False,
            sheet_name="Customized BOM"
        )

    output.seek(0)
    return output


# ============================================================
# SESSION STATE
# ============================================================

if "custom_bom" not in st.session_state:
    st.session_state.custom_bom = []


# ============================================================
# 1. SERVER RACK
# ============================================================

st.header("1. Server Rack")

st.write(
    "Select the required Server Rack type."
)

server_rack = st.radio(
    "Server Rack",
    options=[
        "600",
        "800"
    ],
    horizontal=True,
    key="server_rack"
)

st.info(
    f"Selected Server Rack: **{server_rack}**"
)


# ============================================================
# SERVER RACK QUANTITY
# ============================================================

st.subheader("Server Rack Requirement")

st.caption(
    "The Server Rack selection above is the rack size/type. "
    "Rack quantity is handled separately and is used to determine "
    "the Utility Rack requirement."
)

rack_quantity = st.number_input(
    "Number of Server Racks Required",
    min_value=1,
    max_value=20,
    value=1,
    step=1,
    key="rack_quantity"
)


# ============================================================
# 2. UTILITY RACK
# ============================================================

st.header("2. Utility Rack")

utility_rack = utility_rack_from_quantity(
    rack_quantity
)

st.success(
    f"Utility Rack automatically selected: **{utility_rack}**"
)

if rack_quantity <= 3:
    st.caption(
        f"{rack_quantity} Server Rack(s) → Utility Rack **600**"
    )
else:
    st.caption(
        f"{rack_quantity} Server Rack(s) → Utility Rack **800**"
    )


# ============================================================
# UTILITY RACK RULE DISPLAY
# ============================================================

with st.expander("Utility Rack Selection Rule"):

    utility_rule = pd.DataFrame({
        "Server Rack Quantity": [
            "1 Rack",
            "2 Racks",
            "3 Racks",
            "More than 3 Racks"
        ],
        "Utility Rack": [
            "600",
            "600",
            "600",
            "800"
        ]
    })

    st.dataframe(
        utility_rule,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 3. LOAD
# ============================================================

st.header("3. Load")

load_options = [
    "10 kW",
    "15 kW",
    "20 kW",
    "25 kW",
    "30 kW",
    "35 kW",
    "40 kW",
    "50 kW"
]

selected_load = st.selectbox(
    "Select Required Load",
    load_options,
    key="selected_load"
)


# ============================================================
# LOAD RANGE
# ============================================================

st.subheader("Load Range")

load_range_options = [
    "20–25 kW",
    "25–35 kW",
    "35–50 kW"
]

selected_load_range = st.selectbox(
    "Select Load Range",
    load_range_options,
    key="selected_load_range"
)


# ============================================================
# 4. FIRE SUPPRESSION
# ============================================================

st.header("4. Fire Suppression")

fire_suppression = st.radio(
    "Fire Suppression Required?",
    [
        "No",
        "Yes"
    ],
    horizontal=True,
    key="fire_suppression"
)

if fire_suppression == "Yes":

    st.warning(
        "Fire Suppression selected. Required supporting "
        "components must be included in the final BOM."
    )

    fire_options = st.multiselect(
        "Select Fire Suppression Option(s)",
        [
            "External Fire Suppression",
            "Rack Mount Fire Suppression",
            "Smoke Sensor"
        ],
        key="fire_options"
    )

else:

    fire_options = []


# ============================================================
# 5. CAMERA
# ============================================================

st.header("5. Camera")

camera_required = st.radio(
    "Camera Required?",
    [
        "No",
        "Yes"
    ],
    horizontal=True,
    key="camera_required"
)

if camera_required == "Yes":

    st.warning(
        "Camera selected. Required camera supporting "
        "components must be included in the final BOM."
    )

    camera_options = st.multiselect(
        "Select Camera Requirement(s)",
        [
            "Camera",
            "POE Switch",
            "Network Cable",
            "Hard Disk"
        ],
        key="camera_options"
    )

else:

    camera_options = []


# ============================================================
# 6. OPTIONAL ACCESSORIES
# ============================================================

st.header("6. Optional Accessories")

st.caption(
    "Select any additional accessories required by the customer "
    "and specify the quantity."
)

optional_accessories = [
    "PDU - Basic",
    "PDU - Metered",
    "PDU - Managed",
    "UPS",
    "DCIM",
    "VESDA",
    "Branch Circuit Monitoring"
]

selected_accessories = []

for index, accessory in enumerate(optional_accessories):

    col1, col2 = st.columns([5, 1])

    with col1:

        selected = st.checkbox(
            accessory,
            key=f"accessory_{index}"
        )

    with col2:

        quantity = st.number_input(
            "Qty",
            min_value=1,
            max_value=100,
            value=1,
            step=1,
            disabled=not selected,
            key=f"accessory_qty_{index}"
        )

    if selected:

        selected_accessories.append({
            "component": accessory,
            "quantity": quantity
        })


# ============================================================
# CUSTOMIZATION SUMMARY
# ============================================================

st.divider()

st.header("📋 Customization Summary")

summary = pd.DataFrame({
    "Requirement": [
        "Server Rack",
        "Server Rack Quantity",
        "Utility Rack",
        "Load",
        "Load Range",
        "Fire Suppression",
        "Camera"
    ],
    "Selection": [
        server_rack,
        rack_quantity,
        utility_rack,
        selected_load,
        selected_load_range,
        fire_suppression,
        camera_required
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# OPTIONAL COMPONENT SUMMARY
# ============================================================

if fire_options:

    st.subheader("Fire Suppression Components")

    fire_df = pd.DataFrame({
        "Component": fire_options
    })

    st.dataframe(
        fire_df,
        use_container_width=True,
        hide_index=True
    )


if camera_options:

    st.subheader("Camera Components")

    camera_df = pd.DataFrame({
        "Component": camera_options
    })

    st.dataframe(
        camera_df,
        use_container_width=True,
        hide_index=True
    )


if selected_accessories:

    st.subheader("Optional Accessories")

    accessory_df = pd.DataFrame(
        selected_accessories
    )

    st.dataframe(
        accessory_df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# BUILD BOM
# ============================================================

st.divider()

st.header("📦 Customized Multi Rack BOM")

bom_rows = []


# ------------------------------------------------------------
# SERVER RACK
# ------------------------------------------------------------

bom_rows.append({
    "Category": "Base Configuration",
    "Component": "Server Rack",
    "Specification": f"{server_rack}",
    "Quantity": rack_quantity,
    "Part Number": "XXX"
})


# ------------------------------------------------------------
# UTILITY RACK
# ------------------------------------------------------------

bom_rows.append({
    "Category": "Base Configuration",
    "Component": "Utility Rack",
    "Specification": f"{utility_rack}",
    "Quantity": 1,
    "Part Number": "XXX"
})


# ------------------------------------------------------------
# LOAD
# ------------------------------------------------------------

bom_rows.append({
    "Category": "Requirement",
    "Component": "IT Load",
    "Specification": selected_load,
    "Quantity": 1,
    "Part Number": "XXX"
})


# ------------------------------------------------------------
# LOAD RANGE
# ------------------------------------------------------------

bom_rows.append({
    "Category": "Requirement",
    "Component": "Load Range",
    "Specification": selected_load_range,
    "Quantity": 1,
    "Part Number": "XXX"
})


# ------------------------------------------------------------
# FIRE SUPPRESSION
# ------------------------------------------------------------

if fire_suppression == "Yes":

    for component in fire_options:

        bom_rows.append({
            "Category": "Fire Suppression",
            "Component": component,
            "Specification": "Required",
            "Quantity": 1,
            "Part Number": "XXX"
        })


# ------------------------------------------------------------
# CAMERA
# ------------------------------------------------------------

if camera_required == "Yes":

    for component in camera_options:

        bom_rows.append({
            "Category": "Camera",
            "Component": component,
            "Specification": "Required",
            "Quantity": 1,
            "Part Number": "XXX"
        })


# ------------------------------------------------------------
# OPTIONAL ACCESSORIES
# ------------------------------------------------------------

for accessory in selected_accessories:

    bom_rows.append({
        "Category": "Optional Accessory",
        "Component": accessory["component"],
        "Specification": "Customer Selected",
        "Quantity": accessory["quantity"],
        "Part Number": "XXX"
    })


# ============================================================
# BOM DATAFRAME
# ============================================================

bom_df = pd.DataFrame(
    bom_rows,
    columns=[
        "Category",
        "Component",
        "Specification",
        "Quantity",
        "Part Number"
    ]
)

st.dataframe(
    bom_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# DOWNLOAD BOM
# ============================================================

st.divider()

st.subheader("⬇️ Export")

excel_file = create_bom_excel(
    bom_df
)

st.download_button(
    label="📥 Download Customized Multi Rack BOM",
    data=excel_file,
    file_name="Multi_Rack_Customized_BOM.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
)