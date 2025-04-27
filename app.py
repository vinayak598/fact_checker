import streamlit as st
from news_fetcher import fetch_news_articles
from claim_verifier import verify_claim
from utils import extract_article_texts
from report_generator import generate_pdf_report
from fever_bert import bert_fact_check

# Universal facts dictionary
UNIVERSAL_FACTS = {
    "the sun rises in the east": "True",
    "water boils at 100°c at sea level": "True",
    "earth revolves around the sun": "True",
    "humans need oxygen to survive": "True",
    "light travels faster than sound": "True",
    "gravity pulls objects toward the earth": "True"
}

st.set_page_config(page_title="Fact Checker", layout="centered")
st.title("🧠 AI Fact Checker")
st.write("Enter a claim, and we’ll compare it with reliable, relevant news sources.")

claim = st.text_input("Enter your claim here:")

if st.button("Check Fact"):
    if claim.strip() == "":
        st.warning("Please enter a claim.")
    else:
        with st.spinner("Analyzing your claim..."):
            normalized_claim = claim.lower().strip()

            # ✅ Check for universal facts
            if normalized_claim in UNIVERSAL_FACTS:
                verdict = "✅ True"
                score = 1.00
                st.subheader("🧾 Verdict:")
                st.success(f"{verdict} (Confidence: {score:.2f})")
                st.info("Identified as a universally accepted fact. No need for news verification.")
            else:
                articles = fetch_news_articles(claim)
                if not articles:
                    st.error("No relevant news found.")
                else:
                    texts = extract_article_texts(articles, claim)
                    verdict, score = verify_claim(claim, texts)

                    st.subheader("🧾 Verdict:")
                    st.success(f"{verdict} (Confidence: {score:.2f})")

                    st.subheader("🧠 BERT-based Fact Classification:")
                    results = bert_fact_check(claim, texts)
                    for result in results:
                        st.markdown(f"**Evidence:** {result['evidence'][:200]}...")
                        st.write(f"- {result['label']}: {result['score']:.2f}")
                        st.markdown("---")

                    st.subheader("🔍 Sources Used:")
                    urls = []
                    for art in articles:
                        st.markdown(f"- [{art['title']}]({art['url']})")
                        urls.append(art['url'])

                    if st.button("Generate PDF Report"):
                        file_path = generate_pdf_report(claim, verdict, score, urls)
                        with open(file_path, "rb") as file:
                            st.download_button("📄 Download Report", file, file_name=file_path)
