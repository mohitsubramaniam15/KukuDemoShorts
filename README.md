# 🎧 Kuku Shorts — AI-Powered Audio Reels for Smarter Discovery

🚀 [Demo Video](https://drive.google.com/drive/folders/11tJp9yNECwPO2tnTASlfYYpHkBAjWNm-?usp=sharing) | 📚 [Dataset](https://www.kaggle.com/datasets/elvinrustam/books-dataset/data)  

---

## 🔍 What is Kuku Shorts?

**Kuku Shorts** is a generative AI prototype that transforms long-form audio content (books, podcasts, shows) into **90-second, engaging audio reels** — making content **easier to discover, preview, and explore.**

> 🚀 Powered by LLMs + Azure cloud + Streamlit — Built for Kuku FM’s discovery & retention goals.

---

## 🛠️ Tech Stack

| Category        | Tools Used                                                  |
|----------------|--------------------------------------------------------------|
| **Cloud**       | Azure Data Lake Gen2, Azure Data Factory                     |
| **AI/ML**       | DeepSeek LLM (OpenRouter), Bing Search V7, Azure Neural TTS |
| **Dev Tools**   | Python (Jupyter, Pandas), Streamlit                          |

---

## ⚙️ End-to-End Pipeline

### 🟤 Bronze Layer: Raw Data Ingestion
```python
# Load raw CSV from Azure Data Lake
df = spark.read.csv("/mnt/bronze/books.csv", header=True)
df.display()
```

---

### ⚪ Silver Layer: Description & Script Generation
```python
# Fill missing descriptions via Bing Search API
def get_description(title, author):
    query = f"{title} {author} book summary"
    return bing_search_api(query)

df = df.withColumn("description", when(col("description").isNull(), get_description(col("title"), col("author"))))
```

```python
# Use DeepSeek LLM to generate script
def get_summary(text):
    prompt = f"Summarize this for a 90-second audio reel: {text}"
    return deepseek_api(prompt)

df = df.withColumn("script", get_summary(col("description")))
```

---

### 🟡 Gold Layer: Audio Generation + Final Output
```python
# Generate short-form audio using Azure TTS
def generate_audio(script, voice='en-US-AriaNeural'):
    return azure_tts_api(script, voice)

df = df.withColumn("audio_url", generate_audio(col("script")))
df.write.mode("overwrite").parquet("/mnt/gold/final_reels")
```

---

## 🎛️ Streamlit Preview UI
```python
st.title("Kuku Shorts — Preview Reels")
book = st.selectbox("Choose a Book", df["title"])
st.audio(df.loc[df["title"] == book, "audio_url"].values[0])
```

---

## 📈 Key KPIs & Success Metrics

| Metric                        | Why It Matters                                      | Formula |
|------------------------------|-----------------------------------------------------|---------|
| **Avg. Session Length**      | Measures deeper engagement                          | `((Post - Pre) / Pre) * 100` |
| **App Open Frequency**       | Tracks stickiness & discovery                       | `((Open_post - Open_pre) / Open_pre) * 100` |
| **Reel Completion Rate**     | Are people finishing the 90s reel?                  | `(Completed_plays / Total_plays) * 100` |
| **Click-to-Full-Content**    | Are Shorts converting to long-form listeners?       | `(Users_day7 / Users_day0) * 100` |
| **Day 7 Retention**          | Are people coming back after their first listen?    | `(Users_day7 / Users_day0) * 100` |
| **TTS Cost Optimization**    | Is audio generation scalable?                       | `Total_TTS_Cost / #Shorts` |

---

## 🧠 Challenges Solved

- ❌ Missing Descriptions → ✔️ Filled via Bing Search V7
- ❌ Low-quality Summaries → ✔️ Prompt engineering + LLM tuning
- ❌ Robotic Voice Output → ✔️ Inflection, pause-tuning, voice variation
- ❌ Audio Storage Bloat → ✔️ Sub-1MB reels + Azure blob tiering

---

## 🧩 System Architecture

```plaintext
Kaggle CSV
   ↓
Bronze Layer (Raw)
   ↓
Silver Layer (Enriched + Summarized via Bing & LLM)
   ↓
Gold Layer (TTS + Metadata)
   ↓
Streamlit Preview UI
```

![Architecture Diagram](images/architecture.png)


---

## 📬 Contact

For questions, feedback, or collaborations:

**Mohit Subramaniam**  
📧 [mohitsubramaniam@gmail.com](mailto:mohitsubramaniam@gmail.com)  
🔗 [GitHub](https://github.com/mohitsubramaniam15)

---
