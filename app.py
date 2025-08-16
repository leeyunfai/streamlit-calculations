# Start app with: streamlit run app.py in bash
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Robust DataFrame Calculator with a Form")
st.info("💡 Make any changes you want in the table below. Your edits will only be saved and calculated when you click the 'Save and Update' button.", icon="ℹ️")

# --- INITIALIZATION (No changes needed here) ---
if 'df' not in st.session_state:
    initial_data = {
        'Column A': [100, 200, 50, 400],
        'Column B': [10, 50, 20, 80],
        'Column C': [0.0, 0.0, 0.0, 0.0],
        'Column D': [0.0, 0.0, 0.0, 0.0]
    }
    df = pd.DataFrame(initial_data)
    df['Column C'] = df['Column A'] * df['Column B']
    df['Column D'] = df.apply(
        lambda row: (row['Column B'] / row['Column A']) if row['Column A'] != 0 else 0,
        axis=1
    )
    st.session_state.df = df

# --- CALCULATION FUNCTION (No changes needed here) ---
def update_calculations(dataframe):
    # This function now takes a dataframe as an argument
    df = dataframe.copy() # Work on a copy to avoid side effects
    df['Column C'] = df['Column A'] * df['Column B']
    df['Column D'] = df.apply(
        lambda row: (row['Column B'] / row['Column A']) if row['Column A'] != 0 else 0,
        axis=1
    )
    return df

# --- KEY CHANGE: WRAP THE EDITOR AND BUTTON IN A FORM ---
with st.form(key="data_editor_form"):
    st.subheader("Editable Data Table")
    st.caption("Edit values, add/delete rows, then click the button at the bottom.")
    
    # The data editor is now inside the form
    edited_df = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        column_config={
            "Column A": st.column_config.NumberColumn("Value A", required=True),
            "Column B": st.column_config.NumberColumn("Value B", required=True),
            "Column C": st.column_config.NumberColumn("A * B", disabled=True, format="%.2f"),
            "Column D": st.column_config.NumberColumn("B as % of A", disabled=True, format="%.2f%%")
        }
    )

    # The submit button is also inside the form
    submitted = st.form_submit_button("✅ Save and Update Calculations")


# --- PROCESS THE FORM SUBMISSION ---
# This block of code only runs when the 'submitted' button is clicked
if submitted:
    # On submission, run the calculation on the edited dataframe
    updated_df = update_calculations(edited_df)
    
    # Save the fully updated dataframe back to session state
    st.session_state.df = updated_df
    
    st.success("Changes saved and calculations updated successfully!")
    
    # Optional but recommended: st.rerun() to ensure the UI refreshes
    # and displays the new state cleanly.
    st.rerun()


st.subheader("How the Form-Based Logic Works:")
st.markdown("""
1.  **Wrapping in a Form**: The `st.data_editor` and the `st.form_submit_button` are both placed inside a `with st.form(...)` block.
2.  **Batching Edits**: You can now edit multiple cells, add rows, or delete rows. None of these changes are sent to the Python script yet. They are all buffered in your browser.
3.  **Atomic Submission**: When you click the **'Save and Update Calculations'** button, the *entire state* of the `st.data_editor` (with all your uncommitted edits) is sent to the Streamlit server in a single, atomic action.
4.  **Processing**: The `if submitted:` block becomes `True`. The code inside it executes:
    * It takes the `edited_df`, which now reliably contains all your latest changes.
    * It runs the `update_calculations` function on this fresh data.
    * It saves the final, calculated result back into `st.session_state.df`.
5.  **Clean Refresh**: `st.rerun()` is called to force an immediate refresh of the page, ensuring the data table you see is perfectly in sync with the saved state. This prevents any UI weirdness and guarantees your changes are applied and displayed.
""")