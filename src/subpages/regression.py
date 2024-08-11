import streamlit as st
import statsmodels.api as sm
from subpages.utils.streamlit_tools import growth_df, stringify_g_df, create_and_show_df


def main():
    st.title("Regression Control")
    st.sidebar.success(
        "In this page, the user sets the dependent variable and timeline"
        " for the linear regressions"
    )
    st.header("Define Regression Parameters:")

    prd = None
    if st.session_state.g_df is None and prd is None:
        st.session_state.g_df, st.session_state.g_df_idx = growth_df(
            st.session_state.df
        )

    x_cols = [x for x in st.session_state.g_df.columns if x[3] == "x"]
    y_cols = [y for y in st.session_state.g_df.columns if y[3] == "y"]
    st.session_state.y_sel_g = st.selectbox(
        "Choose the dependent (endogenous) variable:", options=y_cols
    )
    st.session_state.x_sel_g = st.multiselect(
        "Choose independent (exogenous) variables:", options=x_cols
    )

    constant_sel = st.selectbox("Add constant?:", options=["Yes", "No"])
    st.session_state.slider_value_start, st.session_state.slider_value_end = (
        st.select_slider(
            "Choose the range of points to be plotted",
            options=range(0, len(st.session_state.g_df)),
            value=(0, len(st.session_state.g_df) - 1),
            format_func=stringify_g_df,
        )
    )

    if st.button("Update dataframe"):
        st.session_state.r_df = create_and_show_df(
            st.session_state.g_df,
            st.session_state.slider_value_start,
            st.session_state.slider_value_end,
            st.session_state.x_sel_g,
            st.session_state.y_sel_g,
        )
    try:
        if (
            st.session_state.x_sel_g is not None
            and st.session_state.y_sel_g is not None
        ):
            if st.session_state.r_df is not None:
                y = st.session_state.r_df[st.session_state.y_sel_g][
                    st.session_state.slider_value_start : st.session_state.slider_value_end
                ]
                if constant_sel == "Yes":
                    x = st.session_state.r_df[st.session_state.x_sel_g][
                        st.session_state.slider_value_start : st.session_state.slider_value_end
                    ]
                    x = sm.add_constant(x, prepend=False)
                else:
                    x = st.session_state.r_df[st.session_state.x_sel_g][
                        st.session_state.slider_value_start : st.session_state.slider_value_end
                    ]

                model = sm.OLS(y, x).fit()
                st.text(model.summary())
                st.session_state.model_params = dict(model.params)
    except ValueError:
        st.error("Please make sure you chose at least one independent (x) variable.")
    except KeyError:
        st.error("Please click the Update Dataframe button to reload the data.")


if __name__ == "__page__":
    main()
