# 🐦 Twitter Daily Intelligence Scraper (AI-Powered)

## 📌 Overview

This project is an **AI-powered Twitter (X) scraper and analyzer** that fetches recent tweets from any public account and generates a **daily intelligence brief** using an LLM.

Instead of just scraping tweets, the system transforms raw data into **actionable insights**, helping users understand:

* What changed since yesterday
* Market or product signals
* Risks or controversial topics
* What to investigate, monitor, or ignore

---

## 🚀 Features

* 🔍 Fetch latest tweets from any Twitter/X account
* 🕒 Automatically separates:

  * Today's tweets
  * Yesterday’s tweets
* 🧠 AI-powered summarization using OpenAI
* 📊 Generates structured daily brief:

  * Changes vs yesterday
  * Market/Product signals
  * Risk analysis
  * Actionable insights
* ⚡ Handles API rate limits (429 retry logic)
* 🌍 Timezone-aware processing

---

## 🧠 How It Works

### 1. Data Collection

* Uses `twitterapi.io` to fetch recent tweets of a user

### 2. Data Processing

* Parses tweet timestamps
* Filters retweets (optional)
* Splits tweets into:

  * Today
  * Yesterday

### 3. Formatting

* Converts tweets into structured text format for LLM

### 4. AI Analysis

* Sends structured data to OpenAI model
* Uses a custom system prompt to generate insights

### 5. Output

* Returns a clean, structured Markdown summary

---

## 📂 Project Structure

```
.
├── main.py                # Core script
├── .env                  # API keys (not included in repo)
├── README.md             # Project documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/SalamSofi/twitter-ai-scraper.git
cd twitter-ai-scraper
```

### 2. Install Dependencies

```bash
pip install requests python-dotenv openai
```

### 3. Create `.env` File

```env
TWITTERAPI_IO_KEY=your_twitter_api_key
OPENAI_API_KEY=your_openai_api_key
```

---

## ▶️ Usage

Run the script:

```bash
python main.py
```

Change the username inside the script:

```python
display_summary("elonmusk", include_retweets=True)
```

---

## 🧾 Sample Output

```
1) What changed vs yesterday?
- Increased focus on AI and Tesla updates

2) What's new product / market signal?
- Potential new AI feature announcement

3) Anything controversial/risky?
- Tweets hinting at regulatory concerns

4) Actionable items:
- Investigate: AI roadmap
- Monitor: Tesla announcements
- Ignore: Meme tweets
```

---

## 🛠️ Tech Stack

* Python
* Requests
* OpenAI API
* dotenv
* TwitterAPI.io

---

## ⚠️ Limitations

* Depends on third-party Twitter API (rate limits apply)
* Free-tier restricts request frequency
* LLM output quality depends on prompt design

---

## 💡 Future Improvements

* Add database (store historical trends)
* Build dashboard (Streamlit / React)
* Add multi-account tracking
* Real-time alerts system
* Sentiment analysis layer

---

## 🎯 Use Cases

* Market research
* Founder / investor tracking
* Competitor analysis
* Trend monitoring
* Social media intelligence

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---

## 👨‍💻 Author

Mohd. Salam Sofi

---

## ⭐ If you found this useful

Give it a star ⭐ and share it!
