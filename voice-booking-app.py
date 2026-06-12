import streamlit as st
import speech_recognition as sr
import tempfile
import re

st.set_page_config(page_title="Voice Ticket Booking", page_icon="🎤")

st.title("🎤 Voice Travel Ticket Booking")

st.write("Record your voice and the system will fill the booking details.")

# Voice input
audio_file = st.audio_input("Record your voice")

if audio_file is not None:

    # Save audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        audio_path = tmp.name

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)

        st.success("Voice Recognized Successfully")
        st.write("**You said:**", text)

        # Extract source and destination
        source = ""
        destination = ""

        from_match = re.search(r"from\s+([a-zA-Z]+)", text, re.IGNORECASE)
        to_match = re.search(r"to\s+([a-zA-Z]+)", text, re.IGNORECASE)

        if from_match:
            source = from_match.group(1)

        if to_match:
            destination = to_match.group(1)

        st.session_state["source"] = source
        st.session_state["destination"] = destination

    except Exception as e:
        st.error(f"Error: {e}")

# Booking Form
with st.form("ticket_form"):

    name = st.text_input("Passenger Name")

    source = st.text_input(
        "From",
        value=st.session_state.get("source", "")
    )

    destination = st.text_input(
        "To",
        value=st.session_state.get("destination", "")
    )

    travel_date = st.date_input("Travel Date")

    passengers = st.number_input(
        "Number of Passengers",
        min_value=1,
        value=1
    )

    submit = st.form_submit_button("Book Ticket")

    if submit:
        st.success("✅ Ticket Booked Successfully")

        st.write("### Booking Details")
        st.write("**Name:**", name)
        st.write("**From:**", source)
        st.write("**To:**", destination)
        st.write("**Date:**", travel_date)
        st.write("**Passengers:**", passengers)