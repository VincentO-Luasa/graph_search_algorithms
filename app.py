import random

import streamlit as st

from utils import *

min_nodes = 10
max_nodes = 150

if "seed" not in st.session_state:
    st.session_state.seed = random.randrange(10**6)

with st.sidebar:
    node_number = st.number_input(
        f"Please enter the desired amount of nodes, between {min_nodes} and {max_nodes}",
        min_value=min_nodes,
        max_value=max_nodes,
        value=40,
        step=1,
    )
    if st.button("New graph"):
        st.session_state.seed = random.randrange(10**6)
    st.divider()
    algorithm = st.radio(
        "Please select the desired search algorithm",
        (
            "Breadth-First Search",
            "Depth-First Search",
        ),
    )
    st.divider()

    graph = generate_graph(node_number, st.session_state.seed)
    first_node = 0
    last_node = len(graph.graph) - 1
    default_start, default_goal = default_endpoints(graph)
    start = st.number_input(
        f"Please enter the starting node, between {first_node} and {last_node}",
        min_value=first_node,
        max_value=last_node,
        value=default_start,
        step=1,
    )
    goal = st.number_input(
        f"Please enter the goal node, between {first_node} and {last_node}",
        min_value=first_node,
        max_value=last_node,
        value=default_goal,
        step=1,
    )
    st.divider()
    step_duration = st.slider(
        "Please select the step duration",
        min_value=0.1,
        max_value=1.5,
        value=0.5,
        step=0.1,
    )


st.header("Graph Search Algorithms")
st.divider()
st.markdown(f"**Selected search method:** {algorithm}")
st.markdown(f"**Number of nodes in the graph:** {len(graph.graph)}")
st.markdown(
    ":blue[**start**] · :red[**goal**] · :green[**explored**] · "
    ":orange[**path**]"
)

st.divider()

begin = st.button("Begin search")

plot_holder = st.empty()

plot_graph(graph, endpoint_colors(graph, start, goal), plot_holder)

if begin:
    visited, path = run_visualization(algorithm, graph, plot_holder, start, goal, step_duration)
    if path:
        st.markdown(
            f"Explored **{len(visited)}** / {len(graph.graph)} nodes · "
            f"path of **{len(path) - 1}** hops, total cost **{path_cost(graph, path)}**"
        )
    else:
        st.markdown(f"Explored **{len(visited)}** nodes · no path")
