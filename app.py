import random

import pandas as pd
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
        tuple(algorithms),
    )
    st.divider()
    mode = st.radio(
        "Please select the edge costs",
        ("Weighted", "Unweighted"),
        help="Weighted: each edge costs its length. Unweighted: every edge costs 1.",
    )
    st.divider()

    graph = generate_graph(node_number, st.session_state.seed)
    graph.weighted = mode == "Weighted"
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
st.markdown(descriptions[algorithm])
if graph.weighted:
    st.markdown("The graph is **weighted**: each edge costs its length, shown on the path once found.")
else:
    st.markdown("The graph is **unweighted**: every edge costs 1, so the fewest hops is also the cheapest path.")
st.markdown(f"**Number of nodes in the graph:** {len(graph.graph)}")
st.markdown(
    ":blue[**start**] · :red[**goal**] · :green[**explored**] · "
    ":violet[**explored from the goal**] · :orange[**path**]"
)

st.divider()

col1, col2 = st.columns(2)
begin = col1.button("Begin search")
race_all = col2.button("Race all six")

plot_holder = st.empty()

plot_graph(graph, endpoint_colors(graph, start, goal), plot_holder)

if begin:
    visited, path = run_visualization(algorithm, graph, plot_holder, start, goal, step_duration)
    if path:
        st.markdown(
            f"Explored **{len(visited)}** / {len(graph.graph)} nodes · "
            f"path of **{len(path) - 1}** hops"
            + (f", total cost **{path_cost(graph, path)}**" if graph.weighted else "")
        )
    else:
        st.markdown(f"Explored **{len(visited)}** nodes · no path")

if race_all:
    results = race(graph, start, goal)
    plot_race(graph, start, goal, results, plot_holder)
    columns = ["explored", "hops", "cost"] if graph.weighted else ["explored", "hops"]
    table = pd.DataFrame(results).T[columns].astype(int)
    st.dataframe(table.style.highlight_min(props="font-weight: bold"))
    if graph.weighted:
        st.markdown(
            "Same start, same goal, **weighted** graph. **Bold** marks the best in each column. "
            "BFS and bidirectional always find the fewest hops; Dijkstra and A* always find the "
            "lowest cost (A* by exploring less); greedy is frugal but carries no guarantee, and DFS wanders."
        )
    else:
        st.markdown(
            "Same start, same goal, **unweighted** graph: every edge costs 1. **Bold** marks the best "
            "in each column. BFS, bidirectional, Dijkstra and A* all find the fewest hops; they differ "
            "only in how much they explore. Greedy and DFS carry no guarantee."
        )
