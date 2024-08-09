import pandas as pd
import streamlit as st
import statsmodels.api as sm
from subpages.utils.process_inputs import (
    growth_df,
    show_df,
)  # pylint: disable=import-error
from subpages.utils.process_inputs import visualise_data
from subpages.utils.process_inputs import stringify, stringify_g_df


def show_dataframe(df, y_sel, x_sel, slider_value_start, slider_value_end):
    filt_cols = []
    filt_cols.append(y_sel)
    for x in x_sel:
        filt_cols.append(x)
    st.dataframe(data=df[slider_value_start:slider_value_end][filt_cols])
    st.session_state.r_df = df[slider_value_start:slider_value_end][filt_cols]


def main():
    st.set_page_config(page_title="Linear Regression on growth rates")
    st.sidebar.success("In this page, the user will run the linear regressions")
    st.header("Linear regression on growth data:")
    prd = None
    if st.session_state.g_df is None and prd is None:
        # prd_key = st.selectbox(label='Select data period:', options=st.session_state.prd_dict.keys())
        # prd = st.session_state.prd_dict[prd_key]
        st.session_state.g_df, st.session_state.g_df_idx = growth_df(
            st.session_state.df
        )
    # st.dataframe(data=st.session_state.g_df[st.session_state.slider_value_start:st.session_state.slider_value_end])

    x_cols = [x for x in st.session_state.g_df.columns if x[3] == "x"]
    y_cols = [y for y in st.session_state.g_df.columns if y[3] == "y"]
    st.session_state.y_sel_g = st.selectbox(
        "Choose the dependent (endogenous) variable:", options=y_cols
    )
    st.session_state.x_sel_g = st.multiselect(
        "Choose independent (exogenous) variables:", options=x_cols
    )  # ,on_change=show_df,
    # args=(st.session_state.g_df[st.session_state.slider_value_start:st.session_state.slider_value_end],
    #      st.session_state.x_sel_g,st.session_state.y_sel_g))

    constant_sel = st.selectbox("Add constant?:", options=["Yes", "No"])
    st.session_state.slider_value_start, st.session_state.slider_value_end = (
        st.select_slider(
            "Choose the range of points to be plotted",
            options=range(0, len(st.session_state.g_df)),
            value=(0, len(st.session_state.g_df) - 1),
            format_func=stringify_g_df,
        )
    )
    print("y sel: ", st.session_state.y_sel_g)
    print("x sel: ", st.session_state.x_sel_g)
    print("start sel: ", st.session_state.slider_value_start)
    print("end sel: ", st.session_state.slider_value_end)
    # print('var dict: ', st.session_state.var_dict)

    # print('g_df head: ', st.session_state.g_df.head())
    # print('g_df length: ', len(st.session_state.g_df))

    if st.button("Update dataframe"):
        show_dataframe(
            st.session_state.g_df,
            st.session_state.y_sel_g,
            st.session_state.x_sel_g,
            st.session_state.slider_value_start,
            st.session_state.slider_value_end,
        )
    try:
        if st.session_state.y_sel_g != None and st.session_state.x_sel_g != None:
            if st.session_state.r_df is not None:
                y = st.session_state.r_df[st.session_state.y_sel_g][
                    st.session_state.slider_value_start : st.session_state.slider_value_end
                ]
                if constant_sel == "Yes":
                    X = st.session_state.r_df[st.session_state.x_sel_g][
                        st.session_state.slider_value_start : st.session_state.slider_value_end
                    ]
                    X = sm.add_constant(X, prepend=False)
                else:
                    X = st.session_state.r_df[st.session_state.x_sel_g][
                        st.session_state.slider_value_start : st.session_state.slider_value_end
                    ]

                model = sm.OLS(y, X).fit()
                st.text(model.summary())
                st.session_state.model_params = dict(model.params)
                print(model.params)
    except ValueError:
        st.error(f"Please make sure you chose at least one independent (x) variable.")
    except KeyError:
        st.error(f"Please click the Update Dataframe button to reload the data.")


if __name__ == "__page__":
    main()
