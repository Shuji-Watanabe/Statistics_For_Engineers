import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px 

data_list0 =[ f"{i+1}" for i in range(10) ]
data_list1 =[ f"学生{i+1}" for i in range(10) ]
data_list2 =[ 33,42,49,51,54,63,68,72,80,98 ]
data_list3 =[ 1 for i in range(10) ]
data_df = pd.DataFrame({"番号":data_list0
                        ,"学生":data_list1
                        ,"点数":data_list2
                        ,"y ":data_list3})

data_df = pd.read_csv("./data/data02.csv")

def vis_quartile(dataframe
                 ,graphtype=1
                 ,tics_num=9
                 ,font_size = 13
                 ,tics_font_size = 18
                 ,annotation_font_size = 20
                 ,vline_width = 2
                 ,disp_width=800,disp_height=200
                 ):
    """dataframe: No,label,data,1  
       graphtype: 1:consecutive number, 2:data
    """

    data_df=dataframe
    data_keys = list(data_df.keys())
    data_size = len(data_df)
    qu_rate_list = [0.0, 0.25, 0.50, 0.75, 1.00]
    n_qu_list = []

    #Set parameter of this function
    fsize = font_size
    ticsfsize = tics_font_size
    annotation_fsize = annotation_font_size
    vline_width = vline_width
    disp_width= disp_width
    disp_height = disp_height


    for qu_index in qu_rate_list:
        tmp_n = 1 + qu_index*(data_size-1)
        x_a = int(tmp_n)
        x_rate = tmp_n - x_a
        n_qu_list.append([tmp_n,x_a,x_rate])
    
    if graphtype==1:
        fig = px.scatter(data_df
                        ,x=data_keys[0]
                        ,y=data_keys[3]
                        ,text=data_keys[2]
                        )
        fig.update_yaxes(showticklabels=False
                        ,range=[0.5, 1.5]
                        ,linecolor='black', linewidth=1, mirror=True)
        fig.update_xaxes(range=[0, data_size+1]
                        ,tickvals=list(np.linspace(1, data_size, tics_num))
                        ,linecolor='black', linewidth=1, mirror=True
                        )

        for i, tmp in enumerate(n_qu_list):
            border = tmp[0]
            fig.add_vline(x=border
                        ,line_width=vline_width , line_dash="dot", line_color="red"
                        ,annotation_text=f"$n_{i}={tmp[0]}$"
                        ,annotation_position="top"
                        ,annotation_font_size=annotation_fsize
                        ,annotation_font_color = "red"
                        ,annotation_x=border
                        ,annotation_y=1+0.1)
            
            
        fig.update_traces(textposition="top center")
        fig.update_layout(font=dict(size=fsize)
                        ,yaxis_title=""
                        ,width=disp_width, height=disp_height
                        ,xaxis = dict(
                                       tickfont = dict(size=ticsfsize)
                                       )
                        )

    elif graphtype==2:
        data_text = data_df[data_keys[0]]
        data_x = data_df[data_keys[2]]
        data_y = [1]*data_size
        data_max = data_x.max()
        data_min = data_x.min()
        data_range = data_max - data_min
        data_margin = int(0.1*data_range)
        qu_list = []
        for num, tmp_list in enumerate(n_qu_list):
            print(f"num={num}")
            if num==0 or num == len(n_qu_list)-1:
                tmp_qu = data_x[tmp_list[1]-1]
                qu_list.append(tmp_qu)
            else:
                x_n = tmp_list[1]-1
                r   = tmp_list[2]
                tmp_qu = data_x[x_n]+ r*(data_x[x_n+1]-data_x[x_n])
                qu_list.append(tmp_qu)

        fig = px.scatter(data_df, 
                         x=data_x, y=data_y, text=data_text
                        )
        fig.update_yaxes(showticklabels=False
                        ,range=[0.5, 1.5]
                        ,linecolor='black', linewidth=1, mirror=True)
        fig.update_xaxes(range=[data_min-data_margin, data_max+data_margin]
                        ,dtick=1
                        ,tickvals=list(np.linspace(int(data_min),int(data_max),tics_num))
                        ,linecolor='black', linewidth=1, mirror=True
                        )
        for i,tmp in enumerate(qu_list):
            border = tmp
            fig.add_vline(x=border
                        ,line_width=2, line_dash="dash", line_color="red"
                        ,annotation_text=f'$Q_{i}={border}$'
                        ,annotation_position="top"
                        ,annotation_font_size=annotation_fsize
                        ,annotation_font_color = "red"
                        ,annotation_x=border
                        ,annotation_y=1+0.1)
        fig.update_traces(textposition="bottom right")
        fig.update_layout(font=dict(size=fsize)
                        ,yaxis_title=""
                        ,xaxis = dict(
                                        tickfont = dict(size=ticsfsize)
                                        )
                        ,width=disp_width, height=disp_height
                        )
    return fig

disp_col = st.columns([1,1,1,1,1])
with disp_col[0]:
    ntics = st.number_input("横軸の刻みの個数",value=9,min_value=1,key="disp1")
fig = vis_quartile(dataframe=data_df
            ,graphtype=1
            ,tics_num=ntics)
st.components.v1.html(fig.to_html(include_mathjax='cdn'),width=820,height=220)


disp_col = st.columns([1,1,1,1,1])

with disp_col[1]:
    ntics = st.number_input("横軸の刻みの個数",value=9,min_value=1,key="disp2")
fig = vis_quartile(dataframe=data_df
            ,graphtype=2
            ,tics_num=ntics)
st.components.v1.html(fig.to_html(include_mathjax='cdn')
                      ,width=820
                      ,height=220)