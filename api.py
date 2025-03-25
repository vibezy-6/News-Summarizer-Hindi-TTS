import streamlit as st
import requests
from gtts import gTTS
from googletrans import Translator
import tempfile

st.set_page_config(page_title="News Summarizer", layout="wide")
st.title("📰 News Summarizer")
st.write("Enter a **company name** below to fetch and analyze the latest news summaries.")

query = st.text_input("🔎 Company Name", placeholder="e.g. Spotify, Tata, Microsoft")

if st.button("Get News Summary"):
    if not query:
        st.warning("Please enter a company name.")
    else:
        with st.spinner("Fetching news from API..."):
            API_URL = "http://localhost:8000/summarize"  # Update for Hugging Face when deployed

            try:
                response = requests.get(API_URL, params={"company": query})
                result = response.json()
            except Exception as e:
                st.error(f"Error fetching from API: {e}")
                result = {}

        if "error" in result:
            st.error(result["error"])
            if "available_count" in result:
                st.info(f"✅ Total links checked: {result['total_links_checked']}, usable summaries found: {result['available_count']}")
        else:
            translator = Translator()
            st.subheader(f"🔹 News Summaries for: {result['company']}")

            for i, news in enumerate(result["news_summaries"], 1):
                with st.expander(f"📄 News {i}", expanded=False):
                    st.write(f"🔗 [Source Link]({news['source']})")
                    st.write(f"📝 **English Summary**: {news['summary']}")
                    st.write(f"📊 **Sentiment**: {news['sentiment']}")
                    st.write(f"📌 **Topics**: {', '.join(news['topics'])}")

                    # Translate summary to Hindi
                    hindi_translation = translator.translate(news['summary'], src='en', dest='hi').text
                    st.markdown("#### 🌐 **हिंदी सारांश:**")
                    st.write(hindi_translation)

                    # Play Hindi TTS
                    st.markdown("#### 🔊 हिंदी में सुनिए:")
                    try:
                        tts = gTTS(hindi_translation, lang='hi')
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                            tts.save(tmpfile.name)
                            st.audio(tmpfile.name, format="audio/mp3")
                    except Exception as e:
                        st.error(f"Couldn't generate Hindi audio: {e}")

            # Comparative Analysis Section
            st.subheader("📊 Comparative Analysis")
            analysis = result["comparative_analysis"]
            st.write("🟢 **Sentiment Distribution**:", analysis["sentiment_distribution"])
            st.write("🧠 **Top Topics**:", ", ".join(analysis["top_topics"]))
            st.write("🌐 **Top Sources**:", ", ".join(analysis["top_sources"]))

            if "example_negative_summary" in analysis:
                st.warning("🚨 Sample Negative Coverage")
                st.write(analysis["example_negative_summary"])

            if "overall_summary" in analysis:
                st.success("📝 Overall Summary")
                st.write(analysis["overall_summary"])

                # Translate and Speak Overall Summary
                st.markdown("### 🌐 **हिंदी सारांश (Overall Summary):**")
                try:
                    hindi_summary = translator.translate(analysis["overall_summary"], src='en', dest='hi').text
                    st.write(hindi_summary)

                    st.markdown("### 🔊 हिंदी में सुनिए (Overall Summary):")
                    tts = gTTS(text=hindi_summary, lang='hi')
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                        tts.save(tmpfile.name)
                        st.audio(tmpfile.name, format="audio/mp3")
                except Exception as e:
                    st.error(f"Couldn't generate Hindi translation or audio: {e}")
