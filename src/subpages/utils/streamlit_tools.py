import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


def stringify(i: int = 0) -> str:
    """Use slider interger index to pull dataframe index string."""
    return st.session_state.df_index[i]


def create_and_show_df(df, slider_value_start, slider_value_end, x_sel, y_sel):
    filt_cols = []
    if isinstance(y_sel, str):
        filt_cols.append(y_sel)
    elif isinstance(y_sel, list):
        for y in y_sel:
            filt_cols.append(y)
    for x in x_sel:
        filt_cols.append(x)
    filt_df = df[slider_value_start : slider_value_end + 1][filt_cols]

    st.dataframe(data=filt_df)

    return filt_df


def visualise_data(df):

    df_idx = df.index
    df_x = pd.DataFrame(index=df_idx)
    df_y = pd.DataFrame(index=df_idx)

    # split x and y columns into separate dfs
    for col in df.columns:
        if col[0] == "x":
            df_x[col] = df[col]
        elif col[0] == "y":
            df_y[col] = df[col]
    fig = px.line(
        df,
        x=df.index,
        y=df.columns,
        title="Interactive chart of each variable over time",
    )
    fig.update_layout(xaxis_title="Timeline", yaxis_title="Variable")
    st.plotly_chart(fig)

    df_indexed = 100 * (df / df.iloc[0, :])
    fig = px.line(
        df_indexed,
        x=df_indexed.index,
        y=df_indexed.columns,
        title="Interactive chart of each variable indexed to base-100 over time",
    )
    fig.update_layout(xaxis_title="Timeline", yaxis_title="Indexed variable")
    st.plotly_chart(fig)


def stringify_g_df(i: int = 0) -> str:
    """Use slider interger index to pull dataframe index string."""
    return st.session_state.g_df_idx[i]


def growth_df(df):
    # 4 for quarterly data
    prd = 4
    # identify columns of each type
    for df_col in df.columns:
        if st.session_state.var_dict[df_col[2:]] == "abs":
            df["g: " + df_col] = (
                df[df_col].pct_change(periods=prd) + 1
            )  # different forms of this produce
            # same coefficient but different constant
            # (e.g. pct_change + 1, or pct_change * 100, or pct_change only)
        if st.session_state.var_dict[df_col[2:]] == "pct_val_or_dummy":
            df["g: " + df_col] = np.exp(df[df_col] - df[df_col].shift(prd))
        # e.g. real toll change:
        if st.session_state.var_dict[df_col[2:]] == "pct_change":
            df["g: " + df_col] = df[df_col] + 1

        g_cols = [c for c in df.columns if c[0:2] == "g:"]
        g_df = df[g_cols].dropna(how="all")
        g_df_idx = g_df.index
    return g_df, g_df_idx


def growth_list(elements):
    return [f"g: {element}" for element in elements]
