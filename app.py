
import json
from pathlib import Path

import pandas as pd
import streamlit as st


LOG_PATH = Path("logs/episodes.jsonl")


st.set_page_config(
    page_title="Laya DOOM Agent",
    layout="wide",
)

st.title("Laya DOOM Agent")
st.caption(
    "Inspect observations, decisions, rewards and inference latency."
)


def load_transitions():
    if not LOG_PATH.exists():
        return []

    records = []

    with LOG_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            if record.get("event") == "transition":
                records.append(record)

    return records


records = load_transitions()

if not records:
    st.info(
        "No transitions found. Run main.py first."
    )
else:
    df = pd.DataFrame(records)

    latest = df.iloc[-1]

    state = latest.get("state", {})

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Health",
        state.get("health", "Unknown"),
    )

    col2.metric(
        "Ammunition",
        state.get("ammo", "Unknown"),
    )

    col3.metric(
        "Latest action",
        str(latest.get("executed_action", "Unknown")),
    )

    latency = latest.get("inference_seconds")

    col4.metric(
        "Inference latency",
        (
            f"{latency * 1000:.0f} ms"
            if isinstance(latency, (int, float))
            else "Unknown"
        ),
    )

    st.subheader("Decision history")

    table = pd.DataFrame({
        "Step": df["step"],
        "Proposed action": df["proposed_action"],
        "Executed action": df["executed_action"],
        "Valid": df["action_valid"],
        "Reward": df["reward"],
        "Inference seconds": df["inference_seconds"],
    })

    st.dataframe(
        table,
        use_container_width=True,
    )

    st.subheader("Reward per decision")

    reward_chart = df.set_index("step")[["reward"]]
    st.line_chart(reward_chart)

    st.subheader("Action frequency")

    action_counts = df["executed_action"].value_counts()
    st.bar_chart(action_counts)

    st.subheader("Raw latest transition")
    st.json(latest.to_dict())

    st.caption(
        "Refresh the page to reload new records."
    )
