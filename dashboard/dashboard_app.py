# dashboard/dashboard_app.py
# Minimal Streamlit dashboard for Phase-1 demo

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Security Dashboard - Prototype", layout="wide")
st.title("Security Dashboard — Prototype")

st.markdown("**Recent logs (sample)**")
logs_path = "data/sample_logs.csv"
if os.path.exists(logs_path):
    df = pd.read_csv(logs_path)
    st.dataframe(df.tail(20))
else:
    st.warning("No sample logs found. Run simulate_attack.py")

st.markdown("**Mitigation log**")
mit_log = "results/mitigation_log.txt"
if os.path.exists(mit_log):
    with open(mit_log, "r") as f:
        lines = f.read().splitlines()
    if lines:
        for line in lines[-10:]:
            st.success(line) if "AUTO-MITIGATION" in line else st.write(line)
    else:
        st.info("Mitigation log empty")
else:
    st.info("No mitigation log yet. Run detect_and_mitigate.py")

st.markdown("---")
st.markdown("**Quick actions (demo only)**")
if st.button("Generate sample logs"):
    import subprocess, sys
    subprocess.run([sys.executable, "../simulate_attack.py"], check=False)
    st.experimental_rerun()

st.write("Note: This is a Phase-1 prototype. Production deployment requires staging, policy checks, and IAM controls.")
