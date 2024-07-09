import pandas as pd
import os
import openpyxl
import plotly.express as px
import plotly.graph_objects as go

# Assumptions for the following script to work:
# Column D only has values for dependent and independent variables and no other content (otherwise any column D text will be assumed a new variable)
# Data for each variable found in Column D is being read from column G onwards until an empty cell is found (None)
# Output dataframe will name each variable before "Independent Variables" cell as X:{variable name} and every variable after "Independent Variables" cell as Y:{variable name}
def spreadsheet_to_df(file_name= 'A32 LV Traffic Forecast Regression Inputs Filled.xlsx'):
    file_path = os.path.join('data','reg_input')
    file_name = 'A32 LV Traffic Forecast Regression Inputs Filled.xlsx'
    full_path = os.path.join(file_path,file_name)
    workbook = openpyxl.load_workbook(full_path, data_only=True)
    sheet = workbook.active


    # Read column names and row names so that the dataframe is filled
    df_cols = []
    dependent_flag =1
    col = 4 # start from Column D for variable names
    for row in range(1,sheet.max_row+1):
        if sheet.cell(row=row, column=col).value != None:
            # if sheet.cell(row=row, column=col).value != 'Dependent Variables' and  sheet.cell(row=row, column=col).value != 'Independent Variables' :
            if sheet.cell(row=row, column=col).value == 'Dependent Variables':
                dependent_flag = 1
                continue
            if sheet.cell(row=row, column=col).value == 'Independent Variables':
                dependent_flag = 0
                continue
            if dependent_flag ==1:
                df_cols.append('x:' + sheet.cell(row=row, column=col).value)
            elif dependent_flag ==0:
                df_cols.append('y:' + sheet.cell(row=row, column=col).value)

    # Build dataframe by iterating over the columns for each variable
    df = pd.DataFrame(columns = df_cols)
    for c in df_cols:
        temp_list = []
        print(c)
        for row in range(1, sheet.max_row + 1):
            if sheet.cell(row=row, column=col).value == c[2:]:
                start_row = row
                break
        cell_names = sheet[start_row]
        for cellObj in cell_names[6:]:
            try:
                val = float(str(cellObj.value))
                temp_list.append(val)
            except ValueError:
                break
        df[c] = temp_list

    return df

    # fig = go.Figure()
    #
    # fig.add_trace(go.Scatter(x=df["x:Traffic (AADT)"], y=df["y:Cong_IC2"], mode='markers', name="x:Traffic (AADT) vs y:Cong_IC2"))
    # fig.add_trace(go.Scatter(x=df["x:Traffic (AADT) v2"], y=df["y:Cong_IC2"], mode='markers', name="x:Traffic (AADT) v2 vs y:Cong_IC2"))
    # fig.add_trace(go.Scatter(x=df["x:Traffic (AADT)"], y=df["y:Cong_A20"], mode='markers', name="x:Traffic (AADT) vs y:Cong_A20"))
    # fig.add_trace(go.Scatter(x=df["x:Traffic (AADT) v2"], y=df["y:Cong_A20"], mode='markers', name="x:Traffic (AADT) v2 vs y:Cong_A20"))
    #
    # # Set title and labels
    # fig.update_layout(
    #     title="Traffic (AADT) vs Cong_IC2 and Cong_A20",
    #     xaxis_title="Traffic (AADT)",
    #     yaxis_title="Congestion"
    # )
    #
    # # Show plot
    # fig.show()
    #
    #
    # # Create scatter plots
    # fig = px.scatter(df, x="x:Traffic (AADT)", y="y:Cong_IC2", title="x:Traffic (AADT) vs y:Cong_IC2")
    # fig.add_scatter(x=df["x:Traffic (AADT) v2"], y=df["y:Cong_IC2"], mode='markers', name="x:Traffic (AADT) v2 vs y:Cong_IC2")
    # fig.add_scatter(x=df["x:Traffic (AADT)"], y=df["y:Cong_A20"], mode='markers', name="x:Traffic (AADT) vs y:Cong_A20")
    # fig.add_scatter(x=df["x:Traffic (AADT) v2"], y=df["y:Cong_A20"], mode='markers', name="x:Traffic (AADT) v2 vs y:Cong_A20")
    #
    # # Show plot
    # fig.show()
    #
    import pandas as pd
    import matplotlib as plt
    import numpy as np
    import cufflinks as cf
    # import plotly.express as px
    #
    # fig = px.line(df)
    # fig.show()