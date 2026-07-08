"""
Analytics component.

Renders conversation statistics in the sidebar.
"""

from datetime import datetime

# Third-Party
import streamlit as st


def render_metric_rows(
    metrics: list[tuple[str, str | int | float]],
) -> None:
    """
    Render a list of metric rows.
    """

    for label, value in metrics:

        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                padding:6px 0;
                border-bottom:1px solid rgba(255,255,255,0.08);
            ">
                <span>{label}</span>
                <span style="font-weight:bold;">
                    {value}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_current_session() -> None:
    """
    Render current session insights.
    """

    st.divider()

    st.markdown("#### 💬 Current Session")

    message_count = len(st.session_state.messages)

    character_count = 0
    word_count = 0

    for message in st.session_state.messages:
        content = message["content"]

        character_count += len(content)

        word_count += len(content.split())

    session_start = datetime.strptime(
        st.session_state.created_at,
        "%Y-%m-%d %H:%M:%S",
    )

    session_duration = datetime.now() - session_start

    duration_seconds = int(session_duration.total_seconds())

    if duration_seconds < 60:
        duration = "Just now"

    elif duration_seconds < 3600:
        minutes = duration_seconds // 60
        duration = f"{minutes} min"

    else:
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        duration = f"{hours}h {minutes}m"

    session_metrics = [
        (
            "💬 Messages",
            message_count,
        ),
        (
            "🔤 Characters",
            f"{character_count:,}",
        ),
        (
            "📖 Words",
            f"{word_count:,}",
        ),
        (
            "⏱ Duration",
            duration,
        ),
    ]

    render_metric_rows(session_metrics)


def render_conversation_statistics(
    statistics: dict,
) -> None:
    """
    Render overall conversation statistics.
    """
    metrics = [
        (
            "💬 Conversations",
            statistics["total_conversations"],
        ),
        (
            "💬 Messages",
            statistics["total_messages"],
        ),
        (
            "👤 User",
            statistics["user_messages"],
        ),
        (
            "🤖 Assistant",
            statistics["assistant_messages"],
        ),
        (
            "📈 Avg / Chat",
            statistics["average_messages_per_conversation"],
        ),
        (
            "📤 Exports",
            statistics["total_exports"],
        ),
    ]

    render_metric_rows(metrics)


def render_analytics(
    statistics: dict,
) -> None:
    """
    Render conversation analytics in the sidebar.
    """

    st.divider()

    st.markdown("### 📊 Analytics")

    render_conversation_statistics(statistics)

    render_current_session()
