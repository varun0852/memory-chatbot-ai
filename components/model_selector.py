import streamlit as st

from config import AVAILABLE_MODELS


def render_model_selector(current_model: str) -> str | None:
    """
    Render the model selector.

    Returns
    -------
    str | None
        Selected model id if Apply is clicked.
        Otherwise None.
    """

    current = next(model for model in AVAILABLE_MODELS if model["id"] == current_model)

    st.success(f"**{current['name']}**\n\n" f"{current['description']}")

    st.divider()

    names = [model["name"] for model in AVAILABLE_MODELS]

    current_index = names.index(current["name"])

    selected_name = st.selectbox(
        "Select Model",
        names,
        index=current_index,
    )

    selected = next(
        model for model in AVAILABLE_MODELS if model["name"] == selected_name
    )

    st.info(
        "Applying a new model will clear the current conversation "
        "and start a new session."
    )

    if (
        st.button(
            "🚀 Apply Model",
            use_container_width=True,
        )
        and selected["id"] != current_model
    ):
        return selected["id"]

    return None
