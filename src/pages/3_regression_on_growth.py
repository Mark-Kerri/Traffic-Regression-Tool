import pandas as pd
import streamlit as st
import statsmodels.api as sm
from pages.utils.process_inputs import growth_df,show_df  # pylint: disable=import-error
from pages.utils.process_inputs import visualise_data
from pages.utils.process_inputs import stringify


def refresh_plot(df,y_sel,x_sel,slider_value_start,slider_value_end):
    filt_cols = []
    filt_cols.append(y_sel)
    for x in x_sel:
        filt_cols.append(x)
    st.dataframe(data=df[slider_value_start:slider_value_end][filt_cols])

def main():
    st.set_page_config(page_title="Linear Regression on growth rates")
    st.sidebar.success(
        "In this page, the user will run the linear regressions"
    )
    st.header("Linear regression on growth data:")
    if st.session_state.g_df is None:
        st.session_state.g_df = growth_df(st.session_state.df)
    # st.dataframe(data=st.session_state.g_df[st.session_state.slider_value_start:st.session_state.slider_value_end])

    x_cols = [x for x in st.session_state.g_df.columns if x[3]=='x']
    y_cols = [y for y in st.session_state.g_df.columns if y[3]=='y']
    st.session_state.y_sel = st.selectbox('Choose the dependent (endogenous) variable:',options=y_cols)
    st.session_state.x_sel = st.multiselect('Choose independent (exogenous) variables:',options=x_cols) #,on_change=show_df,
                               #args=(st.session_state.g_df[st.session_state.slider_value_start:st.session_state.slider_value_end],
                               #      st.session_state.x_sel,st.session_state.y_sel))

    constant_sel = st.selectbox('Add constant?:',options=['Yes','No'])
    st.session_state.slider_value_start, st.session_state.slider_value_end = st.select_slider(
        "Choose the range of points to be plotted",
        options=range(0, len(st.session_state.g_df)), value=(0, len(st.session_state.g_df) - 1),
        format_func=stringify)
    print('y sel: ', st.session_state.y_sel)
    print('x sel: ', st.session_state.x_sel)
    print('start sel: ', st.session_state.slider_value_start)
    print('end sel: ', st.session_state.slider_value_end)
    print('var dict: ', st.session_state.var_dict)

    # print('g_df head: ', st.session_state.g_df.head())
    # print('g_df length: ', len(st.session_state.g_df))

    if st.button('Show dataframe'):
        refresh_plot(st.session_state.g_df,st.session_state.y_sel,st.session_state.x_sel,st.session_state.slider_value_start,st.session_state.slider_value_end)
    if st.session_state.y_sel != None and st.session_state.x_sel != None:
        y = st.session_state.g_df[st.session_state.y_sel][st.session_state.slider_value_start:st.session_state.slider_value_end]
        # print(y[0:3])
        if constant_sel == 'Yes':
            X = st.session_state.g_df[st.session_state.x_sel][st.session_state.slider_value_start:st.session_state.slider_value_end]
            # print(st.session_state.x_sel)
            # print(st.session_state.g_df.head())
            # print('df: ', X)

            X = sm.add_constant(X, prepend=False)
        else:
            X = st.session_state.g_df[st.session_state.x_sel][st.session_state.slider_value_start:st.session_state.slider_value_end]

        model = sm.OLS(y, X).fit()
        st.text(model.summary())
if __name__ == "__main__":
    main()