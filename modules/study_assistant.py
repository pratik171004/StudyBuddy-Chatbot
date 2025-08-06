import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class StudyAssistant:
    def __init__(self, intents_path='data/intents.json'):
        self.intents = self.load_intents(intents_path)
        self.vectorizer, self.patterns, self.tags = self.prepare_data()

        # Load pre-trained generative model (DialoGPT)
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

    def load_intents(self, path):
        with open(path, 'r') as file:
            return json.load(file)["intents"]

    def prepare_data(self):
        patterns = []
        tags = []
        for intent in self.intents:
            for pattern in intent['patterns']:
                patterns.append(pattern)
                tags.append(intent['tag'])

        vectorizer = TfidfVectorizer()
        vectorizer.fit(patterns)

        return vectorizer, patterns, tags

    def get_response(self, user_input, threshold=0.7):
        input_vec = self.vectorizer.transform([user_input])
        pattern_vecs = self.vectorizer.transform(self.patterns)

        similarities = cosine_similarity(input_vec, pattern_vecs).flatten()
        best_match_index = similarities.argmax()
        confidence = similarities[best_match_index]

        if confidence < threshold:
            return self.generate_response(user_input)

        matched_tag = self.tags[best_match_index]
        for intent in self.intents:
            if intent['tag'] == matched_tag:
                return random.choice(intent['responses'])

    def generate_response(self, user_input):
        input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors='pt')
        output_ids = self.model.generate(input_ids, max_length=100, pad_token_id=self.tokenizer.eos_token_id)
        response = self.tokenizer.decode(output_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        return response 