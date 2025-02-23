import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from constraints import list_job, ignore_words, newest_words, failed_words, passed_words, interupt_words, status_words
import difflib
import logging

# Disable NLTK download logs
logging.getLogger('nltk').setLevel(logging.CRITICAL)

# ✅ Download NLP resources
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

# ✅ Function to clean and extract keywords from a question
def extract_keywords(question):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(question.lower())  # Tokenize and convert to lowercase
    
    # ✅ Remove special characters and filter stopwords
    keywords = [word for word in words if word.isalnum() and word not in stop_words]
    
    """
    Determines the intent of the user's query.
    """
    
    intent = []
    keywords_to_remove = []
    for word in keywords:
        if word in ignore_words:
            keywords_to_remove.append(word)
            continue
        if word in interupt_words:
            intent.append("interrupted")
            keywords_to_remove.append(word)
            continue
        if word in status_words:
            intent.append("passed, failed, interrupted")
            keywords_to_remove.append(word)
            continue
        if word in newest_words:
            intent.append("latest")
            keywords_to_remove.append(word)
            continue
        elif word in failed_words:
            intent.append("failed")
            keywords_to_remove.append(word)
            continue
        elif word in passed_words:
            intent.append("passed")
            keywords_to_remove.append(word)
            continue
        elif word in list_job:
            intent.append(word)
            keywords_to_remove.append(word)
            continue

    # Remove the keywords that were marked for removal
    for word in keywords_to_remove:
        keywords.remove(word)

    for word in keywords:
        # Find all elements in list_job that are similar to word
        matching_jobs = difflib.get_close_matches(word, list_job, n=5, cutoff=0.6)

        # Additionally, find all elements in list_job that contain the word as a substring or are contained within the word
        substring_matches = [job for job in list_job if word in job or job in word]

        # Combine both lists and remove duplicates
        all_matches = list(set(matching_jobs + substring_matches))
        intent.extend(all_matches)   
    
    if intent:
        return intent
    else:
        return "unknown_intent"