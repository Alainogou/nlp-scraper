# NLP-Enriched News Intelligence Platform

## Project Overview
The goal of this project is to develop a platform that integrates Natural Language Processing (NLP) techniques to provide insightful analysis of news articles. The platform connects to a news data source, processes the articles through various NLP tasks, and outputs enriched data. It performs the following core tasks:

1. **Entity Detection** - Identifies and categorizes organizations (companies) mentioned in the articles.
2. **Topic Detection** - Classifies news articles into predefined topics such as Tech, Sport, Business, Entertainment, or Politics.
3. **Sentiment Analysis** - Assesses the sentiment (positive, negative, or neutral) of each article.
4. **Scandal Detection** - Detects potential environmental scandals associated with the companies mentioned in the articles.



## Setup Instructions

### Prerequisites
- Python 3.10
- Install required dependencies by running:
  
  ```bash
  conda create --name env --file requirements.txt
  ```

### Scraper Setup

The **scraper_news.py** script is responsible for fetching news articles from a designated source and saving them into a  SQL database. The scraper should collect at least 300 articles over the past week for analysis.

Run the scraper:

```bash
python3 scraper_news.py
```

### NLP Engine Setup

The **nlp_enriched_news.py** script processes the collected news articles by applying various NLP techniques. These include entity detection, topic classification, sentiment analysis, and scandal detection. It outputs a CSV file (`enhanced_news.csv`) with enriched information for each article.

Run the NLP processing:

```bash
python3 nlp_enriched_news.py
```

### Output

After running the NLP engine, you will get the enriched data stored in `enhanced_news.csv`. The file will include the following columns:

- **Unique ID**: Unique identifier for the article.
- **URL**: URL of the article.
- **Date**: Date when the article was scraped.
- **Headline**: Headline of the article.
- **Body**: Body of the article.
- **Org**: List of companies/organizations detected.
- **Topics**: List of topics classified (Tech, Sport, Business, Entertainment, Politics).
- **Sentiment**: Sentiment score (float).
- **Scandal_distance**: Metric indicating the likelihood of an environmental scandal.
- **Top_10**: Boolean flag marking the top 10 articles based on scandal detection.

### Example Output:
```
Unique ID | URL             | Date        | Headline              | Org               | Topics      | Sentiment | Scandal_distance | Top_10
---------------------------------------------------------------------------------------------
1         | www.news1.com    | 2025-02-05  | Tech Company X hits a new milestone | ['Company X']    | ['Tech']   | 0.7        | 0.05            | False
2         | www.news2.com    | 2025-02-05  | Environmental Disaster caused by Company Y | ['Company Y']    | ['Business'] | -0.8       | 0.95            | True
...
```

## Core Features

### 1. **Entity Detection**

This task extracts organizations (ORG entities) mentioned in the article's body and headline. We use **SpaCy** for Named Entity Recognition (NER) to identify companies and organizations.

### 2. **Topic Detection**

The classifier categorizes articles into topics using a pre-trained model based on a labeled dataset. The available topics include:
- Tech
- Sport
- Business
- Entertainment
- Politics

The classifier is trained using `scikit-learn`, and its learning curves are saved to `learning_curves.png`.

### 3. **Sentiment Analysis**

Sentiment analysis classifies each article as positive, negative, or neutral. We use a **pre-trained NLTK model** for sentiment analysis to quickly analyze the sentiment without needing to train a custom model.

### 4. **Scandal Detection**

Scandal detection identifies potential environmental disasters involving companies. This is achieved by:
- Defining keywords (e.g., pollution, deforestation) related to environmental scandals.
- Calculating the distance between the keywords' embeddings and the detected entities.
- Flagging articles that meet the scandal threshold (top 10 articles).

### 5. **Source Analysis** (Optional)

This optional feature generates insights into the news sources, such as:
- The proportion of topics per day.
- Sentiment per company.
- The most mentioned companies.

These insights are plotted and saved in the `results/` folder.

## Learning Objectives

By working through this project, you will:
- Set up an NLP-focused Python environment.
- Implement essential text preprocessing techniques such as tokenization, stop-word removal, and stemming.
- Build a complete text preprocessing pipeline.
- Apply machine learning models for topic classification and sentiment analysis.
- Understand how to use pre-trained models for NLP tasks.
- Perform advanced NLP techniques, including entity recognition and scandal detection.

## How to Run the Project

1. **Run the Scraper**: Collect at least 300 articles by running `scraper_news.py`.

   ```bash
   python scraper_news.py
   ```

2. **Process the Articles**: Use `nlp_enriched_news.py` to process the scraped articles.

   ```bash
   python nlp_enriched_news.py
   ```

3. **Review the Results**: Check the `results/` folder for the CSV file containing the enriched data and the saved model files.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

This README should provide you with all the information you need to understand and run the project. Happy coding!