import pandas_ta as ta
import numpy as np
import yfinance as yf
import pandas as pd
import datetime
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Set page config for a better looking app
st.set_page_config(
    page_title="Stock Trading Signals",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# App title and description
st.title("📊 Stock Trading Signal Analyzer")
st.markdown("""
This app analyzes stocks and classifies them as bullish or bearish.
""")

# Predefined tickers and date range
# ticker_list = ['LT.NS','TCS.NS','PIDILITIND.NS', 'LTIM.NS', 'DABUR.NS', 'PGHH.NS', 'INDIACEM.NS', 'VOLTAS.NS', 'JSL.NS', 'VIJAYA.NS']
        
ticker_list = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "SBIN.NS", 
        "INFY.NS", "LICI.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS", "BAJFINANCE.NS", "HCLTECH.NS", 
        "MARUTI.NS", "SUNPHARMA.NS", "ADANIENT.NS", "KOTAKBANK.NS", "TITAN.NS", "ONGC.NS", 
        "TATAMOTORS.NS", "NTPC.NS", "AXISBANK.NS", "DMART.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", 
        "ULTRACEMCO.NS", "ASIANPAINT.NS", "COALINDIA.NS", "BAJAJFINSV.NS", "BAJAJ-AUTO.NS", 
        "POWERGRID.NS", "NESTLEIND.NS", "WIPRO.NS", "M&M.NS", "IOC.NS", "JIOFIN.NS", "HAL.NS", 
        "DLF.NS", "ADANIPOWER.NS", "JSWSTEEL.NS", "TATASTEEL.NS", "SIEMENS.NS", "IRFC.NS", 
        "VBL.NS", "ZOMATO.NS", "PIDILITIND.NS", "GRASIM.NS", "SBILIFE.NS", "BEL.NS", "LTIM.NS", 
        "TRENT.NS", "PNB.NS", "INDIGO.NS", "BANKBARODA.NS", "HDFCLIFE.NS", "ABB.NS", "BPCL.NS", 
        "PFC.NS", "GODREJCP.NS", "TATAPOWER.NS", "HINDALCO.NS", "HINDZINC.NS", "TECHM.NS", 
        "AMBUJACEM.NS", "INDUSINDBK.NS", "CIPLA.NS", "GAIL.NS", "RECLTD.NS", "BRITANNIA.NS", 
        "UNIONBANK.NS", "ADANIENSOL.NS", "IOB.NS", "LODHA.NS", "EICHERMOT.NS", "CANBK.NS", 
        "TATACONSUM.NS", "DRREDDY.NS", "TVSMOTOR.NS", "ZYDUSLIFE.NS", "ATGL.NS", "VEDL.NS", 
        "CHOLAFIN.NS", "HAVELLS.NS", "HEROMOTOCO.NS", "DABUR.NS", "SHREECEM.NS", "MANKIND.NS", 
        "BAJAJHLDNG.NS", "DIVISLAB.NS", "APOLLOHOSP.NS", "NHPC.NS", "BOSCHLTD.NS", 
        "TORNTPHARM.NS", "ICICIPRULI.NS", "IDBI.NS", "JSWENERGY.NS", "JINDALSTEL.NS", "BHEL.NS", 
        "INDHOTEL.NS", "CUMMINSIND.NS", "ICICIGI.NS", "CGPOWER.NS", "MCDOWELL-N.NS", "HDFCAMC.NS", 
        "MAXHEALTH.NS", "SOLARINDS.NS", "MOTHERSON.NS", "INDUSTOWER.NS", "POLYCAB.NS", "OFSS.NS", 
        "SRF.NS", "IRCTC.NS", "COLPAL.NS", "LUPIN.NS", "NAUKRI.NS", "TIINDIA.NS", "INDIANB.NS", 
        "HINDPETRO.NS", "BERGEPAINT.NS", "YESBANK.NS", "TORNTPOWER.NS", "OIL.NS", "SBICARD.NS", 
        "IDEA.NS", "MARICO.NS", "GODREJPROP.NS", "AUROPHARMA.NS", "UCOBANK.NS", "BANKINDIA.NS", 
        "PERSISTENT.NS", "MUTHOOTFIN.NS", "NMDC.NS", "ALKEM.NS", "PIIND.NS", "LTTS.NS", "GICRE.NS", 
        "TATACOMM.NS", "JSL.NS", "MRF.NS", "SAIL.NS", "PGHH.NS", "SUZLON.NS", "LINDEINDIA.NS", 
        "SUPREMEIND.NS", "CONCOR.NS", "OBEROIRLTY.NS", "ASTRAL.NS", "IDFCFIRSTB.NS", "RVNL.NS", 
        "BHARATFORG.NS", "CENTRALBK.NS", "JSWINFRA.NS", "POLICYBZR.NS", "ASHOKLEY.NS", "THERMAX.NS", 
        "PHOENIXLTD.NS", "GMRINFRA.NS", "TATAELXSI.NS", "PATANJALI.NS", "SJVN.NS", "PRESTIGE.NS", 
        "ACC.NS", "NYKAA.NS", "SUNDARMFIN.NS", "UBL.NS", "ABCAPITAL.NS", "MPHASIS.NS", "BALKRISIND.NS", 
        "DIXON.NS", "MAHABANK.NS", "KALYANKJIL.NS", "SCHAEFFLER.NS", "AWL.NS", "APLAPOLLO.NS", 
        "TATATECH.NS", "SONACOMS.NS", "KPITTECH.NS", "FACT.NS", "PSB.NS", "PETRONET.NS", "L&TFH.NS", 
        "UNOMINDA.NS", "PAGEIND.NS", "MRPL.NS", "AUBANK.NS", "MAZDOCK.NS", "HUDCO.NS", "GUJGASLTD.NS", 
        "NIACL.NS", "CRISIL.NS", "AIAENG.NS", "FEDERALBNK.NS", "IREDA.NS", "VOLTAS.NS", "DALBHARAT.NS", 
        "POONAWALLA.NS", "MEDANTA.NS", "IRB.NS", "3MINDIA.NS",
        "MFSL.NS", "M&MFIN.NS", "UPL.NS", "HONAUT.NS", "BSE.NS", "FLUOROCHEM.NS", "COFORGE.NS", "LICHSGFIN.NS",
        "GLAXO.NS", "DELHIVERY.NS", "BDL.NS", "STARHEALTH.NS", "FORTIS.NS", "BIOCON.NS", "COROMANDEL.NS",
        "NLCINDIA.NS", "TATAINVEST.NS", "JKCEMENT.NS", "IPCALAB.NS", "METROBRAND.NS", "KEI.NS", "ESCORTS.NS",
        "LLOYDSME.NS", "GLAND.NS", "IGL.NS", "NAM-INDIA.NS", "APOLLOTYRE.NS", "JUBLFOOD.NS", "POWERINDIA.NS",
        "MSUMI.NS", "BANDHANBNK.NS", "DEEPAKNTR.NS", "ZFCVINDIA.NS", "AJANTPHARM.NS", "KPRMILL.NS", "SYNGENE.NS",
        "EIHOTEL.NS", "APARINDS.NS", "NATIONALUM.NS", "TATACHEM.NS", "GLENMARK.NS", "HINDCOPPER.NS", "GODREJIND.NS",
        "NH.NS", "BLUESTARCO.NS", "EXIDEIND.NS", "ENDURANCE.NS", "JBCHEPHARM.NS", "PAYTM.NS", "ANGELONE.NS",
        "MOTILALOFS.NS", "ITI.NS", "360ONE.NS", "CARBORUNIV.NS", "AARTIIND.NS", "SUNTV.NS", "KIOCL.NS", "ISEC.NS",
        "RADICO.NS", "SUNDRMFAST.NS", "CREDITACC.NS", "COCHINSHIP.NS", "HATSUN.NS", "MANYAVAR.NS", "CYIENT.NS",
        "GET&D.NS", "BRIGADE.NS", "TIMKEN.NS", "NBCC.NS", "JBMA.NS", "GILLETTE.NS", "KANSAINER.NS", "LAURUSLABS.NS",
        "GRINDWELL.NS", "FIVESTAR.NS", "SWANENERGY.NS", "CHOLAHLDNG.NS", "IRCON.NS", "SKFINDIA.NS", "BSOFT.NS",
        "ASTERDM.NS", "RELAXO.NS", "SONATSOFTW.NS", "GSPL.NS", "RATNAMANI.NS", "ABFRL.NS", "APLLTD.NS", "PFIZER.NS",
        "RAMCOCEM.NS", "SIGNATURE.NS", "PEL.NS", "ELGIEQUIP.NS", "LALPATHLAB.NS", "EMAMILTD.NS", "SANOFI.NS",
        "JYOTICNC.NS", "TRIDENT.NS", "CASTROLIND.NS", "KAJARIACER.NS", "KAYNES.NS", "CENTURYTEX.NS", "CHALET.NS",
        "DEVYANI.NS", "CDSL.NS", "KEC.NS", "SCHNEIDER.NS", "IDFC.NS", "BATAINDIA.NS", "CIEINDIA.NS", "KPIL.NS",
        "RRKABEL.NS", "SUMICHEM.NS", "NATCOPHARM.NS", "SUVENPHAR.NS", "CROMPTON.NS", "TRITURBINE.NS", "PPLPHARMA.NS",
        "INOXWIND.NS", "ACE.NS", "ATUL.NS", "CGCL.NS", "TVSHLTD.NS", "SHYAMMETL.NS", "NUVAMA.NS", "KIMS.NS",
        "CELLO.NS", "PNBHOUSING.NS", "REDINGTON.NS", "LAXMIMACH.NS", "JYOTHYLAB.NS", "CESC.NS", "GODFRYPHLP.NS",
        "NSLNISP.NS", "RITES.NS", "CONCORDBIO.NS", "INDIAMART.NS", "AEGISCHEM.NS", "OLECTRA.NS", "WHIRLPOOL.NS",
        "ANANDRATHI.NS", "NAVINFLUOR.NS", "JWL.NS", "APTUS.NS", "FINCABLES.NS", "FINPIPE.NS", "POLYMED.NS",
        "VINATIORGA.NS", "INTELLECT.NS", "JAIBALAJI.NS", "J&KBANK.NS", "KARURVYSYA.NS", "BLUEDART.NS",
        "MANAPPURAM.NS", "AFFLE.NS", "NCC.NS", "RBLBANK.NS", "TTML.NS", "BASF.NS", "VGUARD.NS", "CAMS.NS",
        "GESHIP.NS", "CENTURYPLY.NS", "CLEAN.NS", "JINDALSAW.NS", "FSL.NS", "ZENSARTECH.NS", "SOBHA.NS",
        "CHAMBLFERT.NS", "DATAPATTNS.NS", "CHENNPETRO.NS", "WELCORP.NS", "MGL.NS", "KSB.NS", "WELSPUNLIV.NS",
        "HSCL.NS", "DCMSHRIRAM.NS", "ASTRAZEN.NS", "ZEEL.NS", "BEML.NS", "HFCL.NS", "RAINBOW.NS", "ABSLAMC.NS",
        "HONASA.NS", "ASAHIINDIA.NS", "PVRINOX.NS", "ARE&M.NS", "IIFL.NS", "BLS.NS", "ALOKINDS.NS", "VTL.NS",
        "GRINFRA.NS", "HBLPOWER.NS", "WESTLIFE.NS", "RKFORGE.NS", "KIRLOSENG.NS", "TITAGARH.NS", "FINEORG.NS",
        "AMBER.NS", "BIKAJI.NS", "SWSOLAR.NS",
        "RAYMOND.NS", "IEX.NS", "SPARC.NS", "GRAPHITE.NS", "SPLPETRO.NS", "RAILTEL.NS", 
        "INGERRAND.NS", "ECLERX.NS", "JUNIPER.NS", "ERIS.NS", "RHIM.NS", "ENGINERSIN.NS", 
        "MAHSEAMLES.NS", "HAPPSTMNDS.NS", "JKTYRE.NS", "TEJASNET.NS", "PNCINFRA.NS", "NEWGEN.NS", 
        "INOXINDIA.NS", "TANLA.NS", "BIRLACORPN.NS", "BBTC.NS", "GMDCLTD.NS", "NUVOCO.NS", 
        "AKZOINDIA.NS", "CEATLTD.NS", "RPOWER.NS", "RELINFRA.NS", "GPIL.NS", "ELECON.NS", 
        "ANANTRAJ.NS", "ELECTCAST.NS", "DBREALTY.NS", "EQUITASBNK.NS", "KFINTECH.NS", "BAJAJELEC.NS", 
        "LATENTVIEW.NS", "JPPOWER.NS", "GRANULES.NS", "AAVAS.NS", "AETHER.NS", "UTIAMC.NS", 
        "LEMONTREE.NS", "JKLAKSHMI.NS", "GPPL.NS", "SFL.NS", "PCBL.NS", "MAPMYINDIA.NS", "ROUTE.NS", 
        "CANFINHOME.NS", "CUB.NS", "SAPPHIRE.NS", "CAPLIPOINT.NS", "MINDACORP.NS", "MMTC.NS", 
        "PTCIL.NS", "IFCI.NS", "PRAJIND.NS", "VOLTAMP.NS", "SCI.NS", "USHAMART.NS", "EIDPARRY.NS", 
        "RTNINDIA.NS", "ANURAS.NS", "GLS.NS", "DOMS.NS", "INFIBEAM.NS", "FORCEMOT.NS", "ZYDUSWELL.NS", 
        "STARCEMENT.NS", "GODREJAGRO.NS", "TTKPRESTIG.NS", "ALKYLAMINE.NS", "GNFC.NS", "KPIGREEN.NS", 
        "CRAFTSMAN.NS", "MAHLIFE.NS", "REDTAPE.NS", "JUBLPHARMA.NS", "NETWEB.NS", "NETWORK18.NS", 
        "PRSMJOHNSN.NS", "METROPOLIS.NS", "CERA.NS", "SBFC.NS", "GRSE.NS", "KIRLOSBROS.NS", 
        "UJJIVANSFB.NS", "SHRIPISTON.NS", "RENUKA.NS", "RATEGAIN.NS", "WOCKPHARMA.NS", "SAFARI.NS", 
        "HAPPYFORGE.NS", "TECHNOE.NS", "SHOPERSTOP.NS", "IBULHSGFIN.NS", "SYRMA.NS", "TEGA.NS", "ACI.NS", 
        "MEDPLUS.NS", "MAHSCOOTER.NS", "NEULANDLAB.NS", "AZAD.NS", "ESABINDIA.NS", "GALAXYSURF.NS", 
        "ZENTEC.NS", "JSWHL.NS", "TV18BRDCST.NS", "HOMEFIRST.NS", "MHRIL.NS", "POWERMECH.NS", 
        "KTKBANK.NS", "JLHL.NS", "MASTEK.NS", "PGHL.NS", "THOMASCOOK.NS", "CCL.NS", "GSFC.NS", 
        "RAJESHEXPO.NS", "QUESS.NS", "VARROC.NS", "TMB.NS", "MANINFRA.NS", "EASEMYTRIP.NS",
        "VIPIND.NS", "IONEXCHANG.NS", "RESPONIND.NS", "MIDHANI.NS", "EMIL.NS", "GAEL.NS", "BALRAMCHIN.NS", 
        "STAR.NS", "JUBLINGREA.NS", "SARDAEN.NS", "JMFINANCIL.NS", "SOUTHBANK.NS", "HEG.NS", 
        "CHEMPLASTS.NS", "ARVIND.NS", "RCF.NS", "NAVA.NS", "ALLCARGO.NS", "ICIL.NS", "IWEL.NS", 
        "KNRCON.NS", "FDC.NS", "RELIGARE.NS", "GRAVITA.NS", "RUSTOMJEE.NS", "MARKSANS.NS", "NIITMTS.NS", 
        "AHLUCONT.NS", "JUSTDIAL.NS", "TRIVENI.NS", "TVSSCS.NS", "GARFIBRES.NS", "VESUVIUS.NS", 
        "SAREGAMA.NS", "DBL.NS", "INDIASHLTR.NS", "BLUEJET.NS", "BALAMINES.NS", "ISGEC.NS", 
        "AVANTIFEED.NS", "INDIACEM.NS", "BECTORFOOD.NS", "CAMPUS.NS", "LTFOODS.NS", "VIJAYA.NS", 
        "GOCOLORS.NS", "BORORENEW.NS", "LXCHEM.NS", "GREENLAM.NS", "DEEPAKFERT.NS", "CMSINFO.NS", 
        "KRBL.NS", "ETHOSLTD.NS", "TEXRAIL.NS", "TCI.NS", "IBREALEST.NS", "JINDWORLD.NS", 
        "EMUDHRA.NS", "PDSL.NS", "GANESHHOUC.NS", "CSBBANK.NS", "SHAREINDIA.NS", "IFBIND.NS", 
        "PRINCEPIPE.NS", "VAIBHAVGBL.NS", "ARVINDFASN.NS", "EDELWEISS.NS", "SENCO.NS", "SPANDANA.NS", 
        "INDIGOPNTS.NS", "GENUSPOWER.NS", "SYMPHONY.NS", "HGINFRA.NS", "TIPSINDLTD.NS", "SIS.NS",
        "MSTCLTD.NS", "NESCO.NS", "SANGHVIMOV.NS", "SANDUMA.NS", "UJJIVAN.NS", "ITDCEM.NS", "CYIENTDLM.NS", 
        "EPL.NS", "SUPRAJIT.NS", "SUNTECK.NS", "HEMIPROP.NS", "MOIL.NS", "TIMETECHNO.NS", "ASTRAMICRO.NS", 
        "TRIL.NS", "WONDERLA.NS", "ASKAUTOLTD.NS", "LLOYDSENGG.NS", "GMMPFAUDLR.NS", "SURYAROSNI.NS", 
        "VSTIND.NS", "PTC.NS", "JKPAPER.NS", "SANSERA.NS", "CHOICEIN.NS", "AURIONPRO.NS", "PAISALO.NS", 
        "ITDC.NS", "HNDFDS.NS", "PARADEEP.NS", "KESORAMIND.NS", "HCC.NS", "ORCHPHARMA.NS", "JAMNAAUTO.NS", 
        "ICRA.NS", "RSYSTEMS.NS", "PRUDENT.NS", "MTARTECH.NS", "UTKARSHBNK.NS", "RAIN.NS", "DYNAMATECH.NS", 
        "JAICORPLTD.NS", "RBA.NS", "GATEWAY.NS", "PURVA.NS", "GUJALKALI.NS", "NAZARA.NS", "RALLIS.NS", 
        "VRLLOG.NS", "GABRIEL.NS", "DODLA.NS", "JKIL.NS", "ROLEXRINGS.NS", "WABAG.NS", "PRICOLLTD.NS", 
        "HCG.NS", "AGI.NS", "DBCORP.NS", "FUSION.NS", "DHANUKA.NS", "MASFIN.NS", "SULA.NS", "TDPOWERSYS.NS", 
        "GALLANTT.NS", "JAYNECOIND.NS", "GULFOILLUB.NS", "SAMHI.NS", "TEAMLEASE.NS", "KIRLPNU.NS", 
        "EPIGRAL.NS", "TIIL.NS", "GOPAL.NS", "JTEKTINDIA.NS", "HEIDELBERG.NS", "SUNDARMHLD.NS", "RTNPOWER.NS", 
        "STLTECH.NS", "JPASSOCIAT.NS", "PATELENG.NS", "ASHOKA.NS", "SINDHUTRAD.NS", "PGEL.NS", "NFL.NS", 
        "ENTERO.NS", "JSFB.NS", "GOKEX.NS", "BANCOINDIA.NS", "VMART.NS", "SHANTIGEAR.NS", "GHCL.NS", 
        "SUDARSCHEM.NS", "WELENT.NS", "FEDFINA.NS", "NOCIL.NS", "TARC.NS", "KKCL.NS", "ORIENTELEC.NS", 
        "BOROLTD.NS", "KIRLOSIND.NS", "BALMLAWRIE.NS", "FCL.NS", "GRWRHITECH.NS", "SHARDAMOTR.NS", 
        "PARKHOTELS.NS", "MAXESTATES.NS", "TI.NS", "AMIORG.NS", "ORIENTCEM.NS", "SHILPAMED.NS", "AARTIDRUGS.NS", 
        "LGBBROSLTD.NS", "AARTIPHARM.NS", "TCIEXP.NS", "WSTCSTPAPR.NS", "ADVENZYMES.NS", "PRIVISCL.NS", 
        "GREENPANEL.NS", "VENUSPIPES.NS", "BBOX.NS", "IIFLSEC.NS", "PILANIINVS.NS", "ROSSARI.NS", "KSL.NS", 
        "DCBBANK.NS", "IMAGICAA.NS", "BAJAJHIND.NS", "DCAL.NS", "HARSHA.NS", "BBL.NS", "YATHARTH.NS", 
        "ORISSAMINE.NS", "THANGAMAYL.NS", "ZAGGLE.NS", "BHARATRAS.NS", "KOLTEPATIL.NS", "KSCL.NS", 
        "MEDIASSIST.NS", "INOXGREEN.NS", "HATHWAY.NS", "SSWL.NS", "UNICHEMLAB.NS", "CIGNITITEC.NS", 
        "IMFA.NS", "ASHAPURMIN.NS", "HGS.NS", "MUTHOOTMF.NS", "SUBROS.NS", "RAMKY.NS", "SUNFLAG.NS", 
        "CARERATING.NS", "GENSOL.NS", "SKIPPER.NS", "LAOPALA.NS", "LUMAXTECH.NS", "DCXINDIA.NS", 
        "BOMDYEING.NS", "HIKAL.NS", "JISLJALEQS.NS", "CUPID.NS", "AVALON.NS", "LUXIND.NS", "NUCLEUS.NS", 
        "TASTYBITE.NS", "SOTL.NS", "ARVSMART.NS", "SANDHAR.NS", "SALASAR.NS", "NEOGEN.NS", "DATAMATICS.NS", 
        "JTLIND.NS", "ANUP.NS", "HERITGFOOD.NS", "THYROCARE.NS", "VADILALIND.NS", "NAVNETEDUL.NS", 
        "DISHTV.NS", "KDDL.NS", "KALAMANDIR.NS", "LANDMARK.NS", "INDOCO.NS", "BAJAJCON.NS", "TVSSRICHAK.NS", 
        "CARTRADE.NS", "SBCL.NS", "FIEMIND.NS", "PRAKASH.NS", "DELTACORP.NS", "RAJRATAN.NS", "IDEAFORGE.NS", 
        "MAHLOG.NS", "PFOCUS.NS", "GREAVESCOT.NS", "DOLLAR.NS", "UFLEX.NS", "UNITECH.NS", "BFUTILITIE.NS", 
        "SHARDACROP.NS", "BANARISUG.NS", "SEQUENT.NS", "GREENPLY.NS", "MAITHANALL.NS", "SHK.NS", 
        "SUNCLAY.NS", "GUFICBIO.NS", "BLSE.NS", "DIACABS.NS", "ESAFSFB.NS", "VSTTILLERS.NS", "HLEGLAS.NS", 
        "BCG.NS", "GOODLUCK.NS", "SWARAJENG.NS", "SEAMECLTD.NS", "SMLISUZU.NS", "ASHIANA.NS", "DALMIASUG.NS", 
        "HINDWAREAP.NS", "SAGCEM.NS", "SAKSOFT.NS", "APOLLO.NS", "SUPRIYA.NS", "AUTOAXLES.NS", 
        "STYLAMIND.NS", "FLAIR.NS", "VINDHYATEL.NS", "CARYSIL.NS", "THEJO.NS", "MPSLTD.NS", "MARATHON.NS", 
        "ISMTLTD.NS", "FILATEX.NS", "NRBBEARING.NS", "JCHAC.NS", "MOLDTKPAC.NS", "DREAMFOLKS.NS", 
        "GMRP&UI.NS", "SHALBY.NS", "INNOVACAP.NS", "PFS.NS", "AJMERA.NS", "HMAAGRO.NS", "NILKAMAL.NS", 
        "RPGLIFE.NS", "TATVA.NS", "STYRENIX.NS", "QUICKHEAL.NS", "ACCELYA.NS", "REPCOHOME.NS", 
        "PCJEWELLER.NS", "APOLLOPIPE.NS"
    ]

current_date = datetime.date.today()
start_date = current_date - datetime.timedelta(days=30)
end_date = current_date + datetime.timedelta(days=1)

# Single button for analysis
run_analysis = st.button("🚀 Run Analysis", type="primary", use_container_width=True)

# Function to create a TradingView URL from a ticker
def get_tradingview_url(ticker):
    # Remove .NS from the ticker
    clean_ticker = ticker.replace('.NS', '')
    return f"https://in.tradingview.com/chart/?symbol=NSE%3A{clean_ticker}"

# Function to perform the analysis
def generate_trading_signals(ticker_list, start_date, end_date):
    signal_dict = {}
    total_tickers = len(ticker_list)
    
    # Create a placeholder for the spinner text
    spinner_text = st.empty()
    # Create a progress bar
    progress_bar = st.progress(0)
    
    for i, ticker in enumerate(ticker_list):
        try:
            # Update spinner text for each ticker
            spinner_text.text(f"Processing {ticker}... ({i+1}/{total_tickers})")
            
            df = yf.download(ticker, start_date, end_date, interval="1D", progress=False)
            
            if df.empty:
                continue
                
            df.columns = df.columns.droplevel(1)
            df['res'] = df['High'].rolling(window=3).max()
            df['sup'] = df['Low'].rolling(window=3).min()
            
            # Pre-calculate the shifted columns
            df['res_shifted'] = df['res'].shift(1)
            df['sup_shifted'] = df['sup'].shift(1)
            
            # Determine the direction of the close using pre-calculated shifted columns
            df['avd'] = df.apply(lambda row: 1 if row['Close'] > row['res_shifted'] else (-1 if row['Close'] < row['sup_shifted'] else 0), axis=1)
            # Get the last non-zero value of avd
            df['avn'] = df['avd'].where(df['avd'] != 0).ffill().fillna(0)
            
            df['tsl'] = df.apply(lambda row: row['sup'] if row['avn'] == 1 else (row['res'] if row['avn'] == -1 else 0), axis=1)
            
            df['green_red'] = 0
            for j in range(1, len(df)):
                if df['Close'].iloc[j-1] < df['tsl'].iloc[j-1] and df['Close'].iloc[j] > df['tsl'].iloc[j]:
                    df.at[df.index[j], 'green_red'] = 'green'
                elif df['Close'].iloc[j-1] > df['tsl'].iloc[j-1] and df['Close'].iloc[j] < df['tsl'].iloc[j]:
                    df.at[df.index[j], 'green_red'] = 'red' 
                else:
                    df.at[df.index[j], 'green_red'] = 'Neutral'
            
            signal_dict[ticker] = {
                'green_red': df['green_red'].tail(1).values[0], 
                'last_close': df['Close'].tail(1).values[0],
                'tradingview_url': get_tradingview_url(ticker)
            }
            
            # Update progress bar
            progress_bar.progress((i + 1) / total_tickers)
            
        except Exception as e:
            st.error(f"Error processing {ticker}: {e}")
            continue
    
    # Clear spinner text and progress bar after completion
    spinner_text.empty()
    progress_bar.empty()
    
    # Convert to DataFrame and categorize
    if signal_dict:
        signals_df = pd.DataFrame.from_dict(signal_dict, orient='index')
        signals_df.reset_index(inplace=True)
        signals_df.rename(columns={'index': 'Ticker'}, inplace=True)
        
        bullish_df = signals_df[signals_df['green_red'] == 'green'].copy()
        bearish_df = signals_df[signals_df['green_red'] == 'red'].copy()
        neutral_df = signals_df[signals_df['green_red'] == 'Neutral'].copy()
        
        return bullish_df, bearish_df, neutral_df
    
    return None, None, None

# Main analysis execution
if run_analysis:
    # Ignore warnings
    import warnings
    warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)
    warnings.simplefilter(action='ignore', category=FutureWarning)
    
    # Run the analysis with spinner
    with st.spinner("Analyzing stocks..."):
        bullish_df, bearish_df, neutral_df = generate_trading_signals(
            ticker_list, 
            start_date, 
            end_date
        )
    
    # Display results
    if bullish_df is not None and bearish_df is not None:
        st.success("Analysis complete!")
        
        # Calculate counts
        bullish_count = len(bullish_df) if bullish_df is not None else 0
        bearish_count = len(bearish_df) if bearish_df is not None else 0
        neutral_count = len(neutral_df) if neutral_df is not None else 0
        total_count = bullish_count + bearish_count + neutral_count
        
        # Display smaller market summary with colored arrows
        if total_count > 0:
            st.header("📊 Market Summary", divider="rainbow")
            
            # Calculate percentages
            bullish_percent = bullish_count/total_count*100
            bearish_percent = bearish_count/total_count*100
            neutral_percent = neutral_count/total_count*100
            
            # Create a more compact market summary with colored arrows
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 5px;">
                    <span style="color: #22c55e; font-size: 24px;">▲</span>
                    <span style="font-size: 18px; margin-left: 5px;">Bullish: {bullish_count} ({bullish_percent:.1f}%)</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 5px;">
                    <span style="color: #ef4444; font-size: 24px;">▼</span>
                    <span style="font-size: 18px; margin-left: 5px;">Bearish: {bearish_count} ({bearish_percent:.1f}%)</span>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div style="text-align: center; padding: 5px;">
                    <span style="color: #ffffff; font-size: 24px;">►</span>
                    <span style="font-size: 18px; margin-left: 5px;">Neutral: {neutral_count} ({neutral_percent:.1f}%)</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Add investment calculations to bullish stocks
            if not bullish_df.empty:
                # Calculate shares per investment amount
                bullish_df['₹5,000 Shares'] = (5000 / bullish_df['last_close']).apply(lambda x: int(x))
                bullish_df['₹40,000 Shares'] = (40000 / bullish_df['last_close']).apply(lambda x: int(x))
                bullish_df['₹50,000 Shares'] = (50000 / bullish_df['last_close']).apply(lambda x: int(x))
                
                # Use the URL directly without HTML formatting
                bullish_df['Chart'] = bullish_df['tradingview_url']
                
                # Create signal indicators
                bullish_df['Signal'] = '▲'
            
            # Add signal indicators to other dataframes
            if not bearish_df.empty:
                bearish_df['Signal'] = '▼'
            
            if neutral_df is not None and not neutral_df.empty:
                neutral_df['Signal'] = '►'
            
            # Display tables for each category
            st.subheader("Stock Details", divider="gray")
            
            # Use different column layouts for bullish (wider) vs bearish and neutral
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("▲ Bullish Stocks - Investment Options")
                if not bullish_df.empty:
                    # Create a DataFrame for display with direct URL column
                    bullish_display = bullish_df[['Ticker', 'Signal', 'last_close', 'Chart', '₹5,000 Shares', '₹40,000 Shares', '₹50,000 Shares']]
                    bullish_display = bullish_display.rename(columns={
                        'last_close': 'Last Close'
                    })
                    
                    # Display the DataFrame with URL column
                    st.dataframe(
                        bullish_display,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Ticker": st.column_config.Column(
                                "Ticker",
                                width="medium",
                            ),
                            "Signal": st.column_config.Column(
                                "Signal",
                                width="small",
                            ),
                            "Last Close": st.column_config.NumberColumn(
                                "Last Close",
                                format="₹%.2f",
                            ),
                            "Chart": st.column_config.LinkColumn(
                                "Chart",
                                width="small",
                                display_text="View"
                            ),
                            "₹5,000 Shares": st.column_config.NumberColumn(
                                "Shares @ ₹5K",
                                help="How many shares you can buy with ₹5,000",
                                format="%d",
                            ),
                            "₹40,000 Shares": st.column_config.NumberColumn(
                                "Shares @ ₹40K",
                                help="How many shares you can buy with ₹40,000",
                                format="%d",
                            ),
                            "₹50,000 Shares": st.column_config.NumberColumn(
                                "Shares @ ₹50K",
                                help="How many shares you can buy with ₹50,000",
                                format="%d",
                            ),
                        }
                    )
                else:
                    st.info("No bullish stocks found.")
            
            with col2:
                # Use tabs for bearish and neutral
                tabs = st.tabs(["▼ Bearish Stocks", "► Neutral Stocks"])
                
                with tabs[0]:
                    if not bearish_df.empty:
                        # Create a DataFrame for display (without links)
                        bearish_display = bearish_df[['Ticker', 'Signal', 'last_close']]
                        bearish_display = bearish_display.rename(columns={
                            'last_close': 'Last Close'
                        })
                        
                        # Display the DataFrame
                        st.dataframe(
                            bearish_display,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Signal": st.column_config.Column(
                                    "Signal",
                                    width="small",
                                ),
                                "Last Close": st.column_config.NumberColumn(
                                    "Last Close",
                                    format="₹%.2f",
                                )
                            }
                        )
                    else:
                        st.info("No bearish stocks found.")
                
                with tabs[1]:
                    if neutral_df is not None and not neutral_df.empty:
                        # Create a DataFrame for display (without links)
                        neutral_display = neutral_df[['Ticker', 'Signal', 'last_close']]
                        neutral_display = neutral_display.rename(columns={
                            'last_close': 'Last Close'
                        })
                        
                        # Display the DataFrame
                        st.dataframe(
                            neutral_display,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Signal": st.column_config.Column(
                                    "Signal",
                                    width="small",
                                ),
                                "Last Close": st.column_config.NumberColumn(
                                    "Last Close",
                                    format="₹%.2f",
                                )
                            }
                        )
                    else:
                        st.info("No neutral stocks found.")
    else:
        st.info("Click 'Run Analysis' to analyze stock signals.")

# Add footer with additional information
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p style="font-size: 16px;">Created by amol nawale</p>
    <p style="font-size: 14px; color: #666;">Data source: Yahoo Finance | Last updated: {}</p>
</div>
""".format(datetime.date.today().strftime("%B %d, %Y")), unsafe_allow_html=True)
