import pandas as pd
import streamlit as st
import plotly.express as px
from subpages.utils.streamlit_tools import stringify


def main():
    # 4 for quarterly data
    prd = st.session_state.prd_dict["Quarterly"]

    print(prd)
    st.set_page_config(page_title="Backcast")
    st.sidebar.success(
        "In this page, the user will use the linear regression coefficients to backcast traffic"
    )
    st.header("Backcast traffic based on regression coefficients")

    # x_cols = [x for x in st.session_state.df.columns if x[0] == "x"]
    y_cols = [y for y in st.session_state.df.columns if y[0] == "y"]
    st.session_state.y_sel = st.selectbox(
        "Choose the dependent (endogenous) variable:", options=y_cols
    )
    # st.session_state.x_sel =
    #   st.multiselect('Choose independent (exogenous) variables:', options=x_cols)
    # st.header("Base year data:")
    st.session_state.slider_value_start, st.session_state.slider_value_end = (
        st.select_slider(
            "Select the range of points to be used as base year",
            options=range(0, len(st.session_state.df)),
            value=(0, len(st.session_state.df) - 1),
            # on_change=visualise_data,
            args=(
                st.session_state.df,
                st.session_state.slider_value_start,
                st.session_state.slider_value_end,
            ),
            format_func=stringify,
        )
    )
    base_year_start = st.session_state.slider_value_start
    base_year_end = st.session_state.slider_value_end
    # base year
    print(
        st.session_state.df[st.session_state.y_sel][base_year_start : base_year_end + 1]
    )

    for key in st.session_state.model_params:
        if not isinstance(st.session_state.model_params[key], list):
            st.session_state.model_params[key] = [st.session_state.model_params[key]]
    test_df = pd.DataFrame(st.session_state.model_params)
    # st.dataframe(test_df)
    edited_df = st.data_editor(test_df, num_rows="dynamic")
    # print(edited_df)
    # print(base_year_start)
    # print('original df: ',st.session_state.df[st.session_state.x_sel][:base_year_start])
    # print('original df: ',st.session_state.g_df[st.session_state.x_sel_g][:base_year_start])

    # print(st.session_state.g_df.columns)
    st.header("Base year data:")
    st.dataframe(
        st.session_state.df[st.session_state.y_sel][base_year_start : base_year_end + 1]
    )
    st.header("Growth rates:")
    # growth rate of GDP
    elast_df = (
        st.session_state.g_df[st.session_state.x_sel_g]
        ** edited_df[st.session_state.x_sel_g].iloc[0][st.session_state.x_sel_g]
    )
    st.dataframe(elast_df)
    # st.write(edited_df[st.session_state.x_sel_g].iloc[0][st.session_state.x_sel_g])
    st.header("Backcast:")
    st.session_state.bc_df = pd.DataFrame(
        data=elast_df.shift(periods=-prd), index=st.session_state.df.index
    )
    # print(st.session_state.bc_df[:prd])
    st.session_state.bc_df[:prd] = elast_df[:prd]
    st.session_state.bc_df["Cumulative Growth"] = None
    # set the final four timesteps to one #to-do: this needs to be more flexible
    st.session_state.bc_df.loc[
        st.session_state.bc_df.index[-prd:], "Cumulative Growth"
    ] = 1

    # print(len(st.session_state.bc_df))
    # print('GDP col:', st.session_state.x_sel_g)
    for col in st.session_state.x_sel_g:
        print(col)
        st.session_state.bc_df.loc[st.session_state.bc_df.index[-prd:], col] = 1
    df_reset = st.session_state.bc_df.reset_index()

    for col in st.session_state.x_sel_g:
        for i in range(len(st.session_state.bc_df) - 5, -1, -4):
            df_reset.loc[i, "Cumulative Growth"] = (
                df_reset.loc[i, col] * df_reset.loc[i + 4, col]
            )
            df_reset.loc[i - 1, "Cumulative Growth"] = (
                df_reset.loc[i - 1, col] * df_reset.loc[i + 3, col]
            )
            df_reset.loc[i - 2, "Cumulative Growth"] = (
                df_reset.loc[i - 2, col] * df_reset.loc[i + 2, col]
            )
            df_reset.loc[i - 3, "Cumulative Growth"] = (
                df_reset.loc[i - 3, col] * df_reset.loc[i + 1, col]
            )
        # df_reset.loc[i, 'Cumulative Growth'] =
        #   df_reset.loc[i, 'g: x:GDP'] * df_reset.loc[i + 4, 'g: x:GDP']
        # df_reset.loc[i - 1, 'Cumulative Growth'] =
        #   df_reset.loc[i - 1, 'g: x:GDP'] * df_reset.loc[i + 3, 'g: x:GDP']
        # df_reset.loc[i - 2, 'Cumulative Growth'] =
        #   df_reset.loc[i - 2, 'g: x:GDP'] * df_reset.loc[i + 2, 'g: x:GDP']
        # df_reset.loc[i - 3, 'Cumulative Growth'] =
        #   df_reset.loc[i - 3, 'g: x:GDP'] * df_reset.loc[i + 1, 'g: x:GDP']
    st.session_state.bc_df = df_reset
    # st.dataframe(st.session_state.bc_df)
    # calcs for back casting
    df_reset["Predicted y"] = None
    for i in range(0, len(st.session_state.bc_df)):
        df_reset.loc[i, "Predicted y"] = (
            df_reset.loc[i, "Cumulative Growth"]
            * st.session_state.df[st.session_state.y_sel][i]
        )
    df_reset["Predicted y"] = df_reset["Predicted y"].astype(float)
    st.session_state.bc_df = st.session_state.bc_df.set_index("index")
    st.session_state.bc_df[st.session_state.y_sel] = st.session_state.df[
        st.session_state.y_sel
    ]
    st.dataframe(st.session_state.bc_df)
    # visualise_data(st.session_state.bc_plot_df,0,len(st.session_state.bc_plot_df)-1)
    # to-do: Either modify the visualise_data function to be more flexbile (e.g. add input title)
    #   or create a new visualisation funciton
    st.session_state.bc_plot_df = st.session_state.bc_df[
        ["Predicted y", st.session_state.y_sel]
    ]
    fig = px.line(
        st.session_state.bc_plot_df,
        x=st.session_state.bc_plot_df.index,
        y=st.session_state.bc_plot_df.columns,
        title=f"Backcasting {st.session_state.y_sel} over time",
    )
    fig.update_layout(xaxis_title="Year", yaxis_title="Variable")
    st.plotly_chart(fig)


if __name__ == "__page__":
    main()
