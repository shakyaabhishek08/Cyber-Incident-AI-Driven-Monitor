import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class HeadlineRecommender:
    def __init__(self, csv_file):
        # Load data
        self.data = pd.read_csv(csv_file)
        
        # Ensure necessary columns exist
        required_columns = {"Headline", "Link", "Date"}
        if not required_columns.issubset(self.data.columns):
            raise ValueError(f"CSV file must contain columns: {required_columns}")

        # Initialize TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer(stop_words='english')

        # Fit and transform headlines
        self.headline_vectors = self.vectorizer.fit_transform(self.data['Headline'])

    def recommend(self, keyword):
        # Transform user keyword into vector
        keyword_vector = self.vectorizer.transform([keyword])

        # Compute cosine similarity
        similarities = cosine_similarity(keyword_vector, self.headline_vectors).flatten()

        # Get the index of the most similar headline
        most_similar_idx = similarities.argmax()

        # Retrieve the most relevant headline and metadata
        result = {
            "Headline": self.data.iloc[most_similar_idx]['Headline'],
            "Link": self.data.iloc[most_similar_idx]['Link'],
            "Date": self.data.iloc[most_similar_idx]['Date'],
            "Similarity Score": similarities[most_similar_idx]
        }

        return result

# Usage Example
if __name__ == "__main__":
    # Initialize recommender with CSV file
    recommender = HeadlineRecommender("news.csv")

    while True:
        # Get user input
        print("\nMenu:")
        print("1. Search for a headline")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            keyword = input("Enter a keyword: ")
            recommendation = recommender.recommend(keyword)

            print("\nMost Relevant Headline:")
            print(f"Headline: {recommendation['Headline']}")
            print(f"Link: {recommendation['Link']}")
            print(f"Date: {recommendation['Date']}")
            print(f"Relevance Score: {recommendation['Similarity Score']:.4f}")
        elif choice == "2":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
