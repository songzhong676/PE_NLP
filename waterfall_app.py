import streamlit as st
import graphviz

st.set_page_config(page_title="PE-Priority-Cascade UI", layout="wide")
st.title("PE Priority Cascade: Proposed Hierarchy")
st.markdown("Toggle the NLP flags on the left. Watch the logic flow on the right.")
st.divider()

import streamlit as st
import graphviz

st.set_page_config(page_title="PE NLP Final Architecture", layout="wide")
st.title("🌊 PE Priority Cascade: Final Architecture")
st.markdown("Features: **Global Critical Bypass**, **Split-Limitations**, and **Entity-Level Contradiction Safety**.")
st.divider()

# ==========================================
# 1. UI LAYOUT
# ==========================================
col_controls, col_graph = st.columns([1, 2.5])

with col_controls:
    st.subheader("Extracted NLP Flags")
    
    st.markdown("**Attending Addendum**")
    a_crit = st.checkbox("🚨 Critical Result (Acute)", key="a_cr")
    a_central = st.checkbox("Central Only", key="a_cen")
    a_ent_lim = st.checkbox("Entity Limitation", key="a_el")
    a_acute = st.checkbox("Acute PE", key="a_a")
    a_chronic = st.checkbox("Chronic PE", key="a_c")
    a_neg = st.checkbox("Negated", key="a_n")
    a_hypo = st.checkbox("Hypothetical", key="a_h")
    a_macro_lim = st.checkbox("Macro Limitation", key="a_ml")
    
    st.markdown("**Primary Report**")
    p_crit = st.checkbox("🚨 Critical Result (Acute)", key="p_cr")
    p_central = st.checkbox("Central Only ", key="p_cen")
    p_ent_lim = st.checkbox("Entity Limitation ", key="p_el")
    p_acute = st.checkbox("Acute PE ", key="p_a")
    p_chronic = st.checkbox("Chronic PE ", key="p_c")
    p_neg = st.checkbox("Negated ", key="p_n")
    p_hypo = st.checkbox("Hypothetical ", key="p_h")
    p_macro_lim = st.checkbox("Macro Limitation ", key="p_ml")

# ==========================================
# 2. EVALUATE THE FINAL CASCADE LOGIC
# ==========================================
winner = None

# 0. GLOBAL CRITICAL BYPASS
if a_crit: winner = "a_crit"
elif p_crit: winner = "p_crit"

# 1. ATTENDING CASCADE
elif a_central: winner = "a_central"
elif a_ent_lim: winner = "a_ent_lim"
elif a_acute: winner = "a_acute"
elif a_chronic: winner = "a_chronic"  # Freed from 'and not' locks!
elif a_neg: winner = "a_neg"
elif a_hypo: winner = "a_hypo"
elif a_macro_lim: winner = "a_macro_lim"

# 2. PRIMARY CASCADE
elif p_central: winner = "p_central"
elif p_ent_lim: winner = "p_ent_lim"
elif p_acute: winner = "p_acute"
elif p_chronic: winner = "p_chronic"  # Freed from 'and not' locks!
elif p_neg: winner = "p_neg"
elif p_hypo: winner = "p_hypo"
elif p_macro_lim: winner = "p_macro_lim"

else: winner = "default"

# ==========================================
# 3. BUILD THE DYNAMIC GRAPHVIZ CHART
# ==========================================
def get_node_style(node_id, current_winner):
    cascade_order = [
        "a_crit", "p_crit",
        "a_central", "a_ent_lim", "a_acute", "a_chronic", "a_neg", "a_hypo", "a_macro_lim",
        "p_central", "p_ent_lim", "p_acute", "p_chronic", "p_neg", "p_hypo", "p_macro_lim",
        "default"
    ]
    
    if current_winner == "default" and node_id != "default":
        return {"color": "black", "fillcolor": "white", "style": "filled"}
        
    node_idx = cascade_order.index(node_id)
    winner_idx = cascade_order.index(current_winner)
    
    if node_idx < winner_idx:
        return {"color": "blue", "fillcolor": "#e6f2ff", "style": "filled"}
    elif node_idx == winner_idx:
        return {"color": "green", "fillcolor": "#d9f2d9", "style": "filled,bold"}
    else:
        return {"color": "gray", "fillcolor": "#f2f2f2", "style": "filled", "fontcolor": "gray"}

with col_graph:
    st.subheader("Logic Flow")
    
    dot = graphviz.Digraph(graph_attr={'rankdir': 'TB'})
    
    dot.node("start", "Start Document", shape="ellipse", style="filled", fillcolor="black", fontcolor="white")
    
    # Critical Bypass Nodes (At the very top)
    dot.node("a_crit", "Attending: CRITICAL\n(3a. Acute PE)", shape="box", **get_node_style("a_crit", winner))
    dot.node("p_crit", "Primary: CRITICAL\n(3a. Acute PE)", shape="box", **get_node_style("p_crit", winner))
    
    # Attending Nodes 
    dot.node("a_central", "Attending: Central\n(1b. Only Central)", shape="box", **get_node_style("a_central", winner))
    dot.node("a_ent_lim", "Attending: Entity Lim\n(2. Limited Study)", shape="box", **get_node_style("a_ent_lim", winner))
    dot.node("a_acute", "Attending: Acute\n(3a. Clearly Pos)", shape="box", **get_node_style("a_acute", winner))
    dot.node("a_chronic", "Attending: Chronic\n(3b. Clearly Pos)", shape="box", **get_node_style("a_chronic", winner))
    dot.node("a_neg", "Attending: Negated\n(1a. Clearly Neg)", shape="box", **get_node_style("a_neg", winner))
    dot.node("a_hypo", "Attending: Hypo\n(1d. Indication)", shape="box", **get_node_style("a_hypo", winner))
    dot.node("a_macro_lim", "Attending: Macro Lim\n(2. Limited Study)", shape="box", **get_node_style("a_macro_lim", winner))
    
    # Primary Nodes 
    dot.node("p_central", "Primary: Central\n(1b. Only Central)", shape="box", **get_node_style("p_central", winner))
    dot.node("p_ent_lim", "Primary: Entity Lim\n(2. Limited Study)", shape="box", **get_node_style("p_ent_lim", winner))
    dot.node("p_acute", "Primary: Acute\n(3a. Clearly Pos)", shape="box", **get_node_style("p_acute", winner))
    dot.node("p_chronic", "Primary: Chronic\n(3b. Clearly Pos)", shape="box", **get_node_style("p_chronic", winner))
    dot.node("p_neg", "Primary: Negated\n(1a. Clearly Neg)", shape="box", **get_node_style("p_neg", winner))
    dot.node("p_hypo", "Primary: Hypo\n(1d. Indication)", shape="box", **get_node_style("p_hypo", winner))
    dot.node("p_macro_lim", "Primary: Macro Lim\n(2. Limited Study)", shape="box", **get_node_style("p_macro_lim", winner))
    
    dot.node("default", "No Mention\n(1c. Default)", shape="ellipse", **get_node_style("default", winner))

    # Connect the nodes
    dot.edges([
        ("start", "a_crit"), ("a_crit", "p_crit"), ("p_crit", "a_central"),
        
        ("a_central", "a_ent_lim"), ("a_ent_lim", "a_acute"), ("a_acute", "a_chronic"), 
        ("a_chronic", "a_neg"), ("a_neg", "a_hypo"), ("a_hypo", "a_macro_lim"), 
        ("a_macro_lim", "p_central"), 
        
        ("p_central", "p_ent_lim"), ("p_ent_lim", "p_acute"), ("p_acute", "p_chronic"), 
        ("p_chronic", "p_neg"), ("p_neg", "p_hypo"), ("p_hypo", "p_macro_lim"), 
        ("p_macro_lim", "default")
    ])
    
    st.graphviz_chart(dot)
