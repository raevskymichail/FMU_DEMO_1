import streamlit as st
import time
import numpy as np
import pandas as pd
import itertools

st.set_page_config(
 page_title='Demonstration of FMPy Model Simulation',
 layout="wide",
 initial_sidebar_state="collapsed",
)

st.sidebar.markdown('''
### Sirkülasyon Testi
Yapılacak değişiklikler programı resetler.
''')

marka = st.sidebar.text_input("Pompa Markası:","FMU")
model = st.sidebar.text_input("Pompa Modeli:","Run")
mod   = st.sidebar.text_input("Çalıştırma Modu:","dP5.0")
zamandamgasi = time.strftime("]_%Y %b %d_%H.%M.%S")
isim = marka+"_"+model+"_["+mod+zamandamgasi

i = 0
t = 0

st.sidebar.write("Otomatik Vana Modunda Deney")
Dint = st.sidebar.number_input("Başlangıç Noktası:",value=15.0)
Dfin = st.sidebar.number_input("Bitiş Noktası:",value=70.0)
ds = st.sidebar.number_input("Adım Aralığı",value=0.25)
dt = st.sidebar.number_input("Adımlar Arası Periyot",value=8)

if st.sidebar.button("Otomatik Modda Kayıt Başlat"):
    kaydet = 1
else:
    kaydet = 0,
    
st.sidebar.write("Manuel Vana Ayarı")
D = st.sidebar.number_input("Vana Açıklığı [0:Kapalı -90:Açık]",value=0.0)
if st.sidebar.button("Ayarla"): 
    yaz(64,[int(D*4)])
    

    
meta_info =[
    ['Date'             ,"Date"             ,"YMD"       ,""         ],
    ['Time'             ,"Time"             ,"HMS"       ,""         ],
    ['Input_S1'         ,"Input_S1"         ,"S1"         ,"[Bar]"       ],
    ['Input_S2'         ,"Input_S2"         ,"S2"         ,"[Bar]"  ],
    ['Input_SUM'        ,"Input_SUM"        ,"SUM"         ,"[Bar]"        ],
    ['Output_y1'        ,"Output_y1"        ,"Y1"         ,"[Bar]"      ],
    # ['Output_y2'        ,"Output_y2"        ,"Y2"        ,"[Bar]"      ],
    # ['Discharge_Pressure'     ,"Basma Basıncı"          ,"P2"        ,"Bar"      ],
    # ['Voltage'                ,"Gerilim"                ,"V"         ,"V"        ],
    # ['Current'                ,"Akım"                   ,"I"         ,"A"        ],
    # ['Measured_Frequency'     ,"Ölçülen Frekans"        ,"f"         ,"Hz"       ],
    # ['Active_Power'           ,"Aktif Güç"              ,"PAP"       ,"W"        ],
    # ['Reactive_Power'         ,"Reaktif Güç"            ,"QRP"       ,"VAr"      ],
    # ['Apperent_Power'         ,"Görünür Güç"            ,"SAP"       ,"VA"       ],
    # ['Phase_Voltage_Angle'    ,"Faz Gerilim Açısı"      ,"PVA"       ,"°"        ],
    # ['Phase_Current_Angle'    ,"Faz Akım Açısı"         ,"PCA"       ,"°"        ],
    # ['Cos_Phi'                ,"Cos_Phi"                ,"PHI"       ,""         ],
    # ['Power_Factor'           ,"Güç Faktörü"            ,"PF"        ,""         ],
    # ['Differential_Pressure'  ,"Fark Basıncı"           ,"DP"        ,"Bar"      ],
    # ['Head'                   ,"Basma Yüksekliği"       ,"H"         ,"m"        ],
    # ['Hydraulic_Power'        ,"Hidrolik Güç"           ,"PHYD"      ,"W"        ],
    # ['Efficiency'             ,"Verimlilik"             ,"ETA"       ,"%"        ]
    ['Output_y2'        ,"Output_y2"        ,"Y2"        ,"[Bar]"      ]
    ]
    
varis = []
for i in meta_info: varis.append(i[0])  #meta_info ilk sütun  (Türkçe için 0 yerine 1. sütun seçilebilir.)
df = pd.DataFrame(columns=varis)
buffy = pd.DataFrame(columns=varis)



col = st.columns(4)
 

###################################### G R A F İ K L E R #############################################

col[0].subheader("Input_S1 [Bar]  \n Input variable #1")
QHt = col[0].line_chart()

col[0].subheader("Input_S2 [Bar] \n Input variable #1")
PHYDETAt = col[0].line_chart()

col[1].subheader("Output_y1 \n Output variable Y1" )
PAPQRPSAP = col[1].line_chart()

col[1].subheader("Input_SUM [Bar] \n Sum of Inputs")
P1P2t = col[1].line_chart()

col[2].subheader("Output_y2 \n Output variable Y2")
PHIPFt = col[2].line_chart()

# col[2].subheader("Faz Gerilim & Akım Açıları [°] \n Phase Voltage & Current Angles")
# PVAPCAt = col[2].line_chart()

# col[0].subheader("Debi & Basma Yüksekliği [m³/h,m]  \n Flow Rate & Head")
# QHt = col[0].line_chart()

# col[0].subheader("Hidrolik Güç & Verimlilik [W,%] \n Hydraulic Power & eta")
# PHYDETAt = col[0].line_chart()

# col[1].subheader("Emme & Basma Basınçları [Bar] \n Suction & Discharge Pressure")
# P1P2t = col[1].line_chart()

# col[1].subheader("Elektrik Güçleri [W, VA, VAr] \n Active, Reactive & Apperent Power" )
# PAPQRPSAP = col[1].line_chart()

# col[2].subheader("cos(φ) & Güç Faktörü \n cos(φ) & Power Factor")
# PHIPFt = col[2].line_chart()

# col[2].subheader("Faz Gerilim & Akım Açıları [°] \n Phase Voltage & Current Angles")
# PVAPCAt = col[2].line_chart()

###################################### M E T R İ K L E R ##############################################

col[3].write(f"Used FMU Model: \n {isim}")
YMDt = col[3].empty()
HMSt = col[3].empty()
Input_S1 = col[3].empty()
Input_S2 = col[3].empty()
Input_SUM = col[3].empty()
Output_y1 = col[3].empty()
Output_y2 = col[3].empty()
# YMDt = col[3].empty()
# HMSt = col[3].empty()
# Tt = col[3].empty()
# Dt = col[3].empty()
# Pt = col[3].empty()
# Vt = col[3].empty()
# ft = col[3].empty()

##################################### D E M O ##########################################################

df = pd.read_excel("demo_data.xlsx", index_col=0)

######################################### D Ö N G Ü ####################################################

# for i in range(len(df)):
for i in itertools.cycle(range(len(df))):
    buff=df.iloc[i]

    with YMDt:
        st.metric("Date",buff[0])
    with HMSt:
        st.metric("Time",buff[1])
    # with Tt:
    #     st.metric("Hat Sıcaklığı",f"{buff[2]} °C")
    # with Tt:
    #     st.metric("Hat Sıcaklığı",f"{buff[2]} °C")
    # with Dt:
    #     st.metric("Vana Açıklığı",f"{buff[4]} °")
    # with Pt:
    #     st.metric("Durağan Basınç",f"{buff[5]} Bar")
    # with Vt:
    #     st.metric("Gerilim",f"{buff[8]} V")
    # with ft:
    #     st.metric("Ölçülen Frekans",f"{buff[10]} Hz")
    
    QHt.add_rows([[float(buff[2])]])
    PHYDETAt.add_rows([[float(buff[3])]])
    P1P2t.add_rows([[float(buff[4])]])
    PHIPFt.add_rows([[float(buff[5])]])
    PAPQRPSAP.add_rows([[float(buff[6])]])
    # QHt.add_rows([[float(buff[3]), float(buff[19])]])
    # PHYDETAt.add_rows([[float(buff[20]), float(buff[21])]])
    # P1P2t.add_rows([[float(buff[6]), float(buff[7])]])
    # PHIPFt.add_rows([[float(buff[16]), float(buff[17])]])
    # PAPQRPSAP.add_rows([[float(buff[11]), float(buff[12]), float(buff[13])]])
    # PVAPCAt.add_rows([[float(buff[14]), float(buff[15])]])
    
    time.sleep(0.01)

    # if kaydet == 1:
    #     if t%dt==0 and Dint<Dfin:
    #         Dint=Dint+ds
    #         yaz(64,[int(Dint*4)])
    #     elif Dint>=Dfin:
    #         df.to_excel(f"{isim}.xlsx")
    #         kaydet=0
        


    
    
