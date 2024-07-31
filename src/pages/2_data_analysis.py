import pandas as pd
import streamlit as st
import statsmodels.api as sm

def show_df(df,x_sel,y_sel):
    # def quarter_to_datetime(quarter_str):
    #     year, quarter = quarter_str.split(' Q')
    #     month = (int(quarter) - 1) * 3 + 1  # January for Q1, April for Q2, etc.
    #     return pd.Timestamp(f"{year}-{month:02d}-01")
    # print('x_sel: ',x_sel)
    # print('y_sel: ',y_sel,'/n')
    filt_cols = []
    filt_cols.append(y_sel)
    for x in x_sel:
        filt_cols.append(x)

    st.dataframe(data=st.session_state.df[st.session_state.slider_value_start:st.session_state.slider_value_end][filt_cols])
    # df['date'] = df.index.map(quarter_to_datetime)


    # df['annual_growth'] = df.groupby(df['date'].dt.quarter)['traffic'].pct_change(periods=4) * 100
    # print(g_df.head())

def main():
    st.set_page_config(page_title="Linear Regression setup")
    # initialize_session_state()
    st.sidebar.success(
        "In this page, the user will define the parameters/setup for the linear regressions"
    )
    st.header("Data preview:")
    # df = pd.read_csv(st.session_state.export_file_path)
    if st.session_state.df is not None:
        # st.dataframe(data=st.session_state.df[st.session_state.slider_value_start:st.session_state.slider_value_end])
        # show_df(st.session_state.df[st.session_state.slider_value_start:st.session_state.slider_value_end])
        # print(st.session_state.var_dict)
        # print(st.session_state.df.columns)
        # st.session_state.g_df = growth_df(st.session_state.df)

        x_cols = [x for x in st.session_state.df.columns if x[0]=='x']
        y_cols = [y for y in st.session_state.df.columns if y[0]=='y']
        st.session_state.y_sel = st.selectbox('Choose the dependent (endogenous) variable:',options=y_cols)
        st.session_state.x_sel = st.multiselect('Choose independent (exogenous) variables:',options=x_cols,on_change=show_df,
                               args=(st.session_state.df[st.session_state.slider_value_start:st.session_state.slider_value_end],
                                     st.session_state.x_sel,st.session_state.y_sel))

        constant_sel = st.selectbox('Add constant?:',options=['Yes','No'])
        print('y sel: ', st.session_state.y_sel)
        print('x sel: ', st.session_state.x_sel)


        # if st.session_state.y_sel[0] !='g':
        #     st.session_state.y_sel = 'g: ' + st.session_state.y_sel
        # for idx, x in enumerate(st.session_state.x_sel):
        #     if not x.startswith('g: '):
        #         st.session_state.x_sel[idx] = 'g: ' + x

        # print('y sel: ', st.session_state.y_sel)
        # print('x sel: ', st.session_state.x_sel)
        if st.session_state.y_sel!=None and st.session_state.x_sel!=None:
           y = st.session_state.df[st.session_state.y_sel]
           if constant_sel=='Yes':
               X = st.session_state.df[st.session_state.x_sel]
               # print(st.session_state.x_sel)
               # print(st.session_state.g_df.head())
               # print('df: ', X)

               X = sm.add_constant(X,prepend=False)
           else:
               X = st.session_state.df[st.session_state.x_sel]

           model = sm.OLS(y,X).fit()
           st.text(model.summary())
           if st.button('Export summary outputs'):
               LRresult = (model.summary2().tables[1])
               st.dataframe(
                   data=LRresult)
               x_sel_str = [x[2:] for x in st.session_state.x_sel]
               print(x_sel_str)
               LRresult.to_csv(f'outputs/reg_{st.session_state.y_sel[2:]}_{x_sel_str}_con_{constant_sel}.csv')
    else:
        st.write('No data is loaded. Use the previous page to load the input data.')


if __name__ == "__main__":
    main()

    #()