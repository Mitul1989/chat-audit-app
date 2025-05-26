
import streamlit as st
import re

st.set_page_config(page_title="Chat Audit Tool", layout="wide")
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Viking_helmet_icon.svg/512px-Viking_helmet_icon.svg.png", width=60)
st.title("Chat Audit Tool (v1) – VikingCloud")

st.markdown("Paste the **chat transcript** below. The tool will auto-detect the agent and audit the chat.")
chat_input = st.text_area("Chat Transcript", height=300)

agent_name_manual = st.text_input("If known, enter Agent's Name (optional)")

if st.button("Run Audit"):
    if not chat_input.strip():
        st.warning("Please paste a chat transcript first.")
    else:
        # Extract agent name
        agent_pattern = re.search(r'(Agent|Rep|Representative)[\s:]+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)', chat_input)
        detected_name = agent_pattern.group(2) if agent_pattern else None
        agent_name = agent_name_manual or detected_name or "Agent"

        st.success(f"✅ Agent identified as: **{agent_name}**")

        # Simulated audit
        audit_results = []
        if "?" not in chat_input:
            audit_results.append("⚠️ No questions were asked. May indicate low engagement.")
        if "bear with me" in chat_input.lower() and "wait" not in chat_input.lower():
            audit_results.append("⚠️ Agent asked to 'bear with me' but didn't follow up soon.")

        if "btw" in chat_input.lower() or "brb" in chat_input.lower():
            audit_results.append("❌ Shorthand used (e.g. 'btw', 'brb').")

        if any(word.isupper() and len(word) > 3 for word in chat_input.split()):
            audit_results.append("❌ Message includes ALL CAPS words.")

        if any(e in chat_input for e in [":)", "😂", "👍", "❤️", "😉"]):
            audit_results.append("❌ Emojis are not allowed.")

        if not audit_results:
            audit_results.append("✅ No critical issues detected in chat.")

        st.subheader("Audit Results")
        for item in audit_results:
            st.markdown(f"- {item}")
