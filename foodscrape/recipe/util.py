import os
import pickle
import re
from pathlib import Path
from typing import List, Tuple

import pandas as pd
import spacy

from foodscrape.config import Config
from foodscrape.logger import get_logger

from .trie import Trie

logger = get_logger(__name__)


class Processor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

        self.model_filename = Path(
            os.path.join(Config.APP_DIR, "data/ingredient_model.pkl")
        )
        self.model_data_dir = Path(os.path.join(Config.APP_DIR, "data"))
        path = Path(self.model_filename)
        if path.is_file():
            self.ingredient_model = self._load_model()
        else:
            self.ingredient_model = self._create_model()
            self._save_model(self.ingredient_model)

    def _create_model(self):
        logger.info("Creating Model")
        ingredients = list(self._process_data())
        trie = Trie()

        for ingredient in ingredients:
            processed_food = self._process_ingredient(ingredient)
            processed_food = self._plural_to_singular(processed_food)
            trie.insert(processed_food)

        return trie

    def _save_model(self, trie: Trie):
        logger.info("Saving Model to %s", self.model_filename)
        file = open(self.model_filename, "wb")
        pickle.dump(trie, file)
        file.close()

    def _load_model(self):
        logger.info("Loading model from %s", self.model_filename)
        file = open(self.model_filename, "rb")
        model = pickle.load(file)
        file.close()
        return model

    def _process_data(self) -> pd.Series:
        food_df: pd.DataFrame = pd.read_pickle(
            self.model_data_dir / "ingr_map.pkl"
        )
        food_df = food_df.rename(columns={"replaced": "name"})
        food_df = food_df.drop(
            columns=[
                "raw_ingr",
                "raw_words",
                "processed",
                "len_proc",
                "count",
                "id",
            ]
        )

        food_df = self._get_count(food_df, "name")
        food_df = self._filter_by_count(food_df, 2)
        food_df = self._filter_by_length(food_df, 3)

        df = pd.concat(
            [
                food_df["name"],
                pd.read_csv(self.model_data_dir / "ingredients.csv")["name"],
            ]
        )

        return df.drop_duplicates()

    def _get_count(
        self, df: pd.DataFrame, col: str, drop_duplicates: bool = True
    ) -> pd.DataFrame:
        df["count"] = df.groupby(col)[col].transform("size")  # type: ignore
        if drop_duplicates:
            return df.drop_duplicates()
        return df

    def _filter_by_count(
        self, df: pd.DataFrame, min_count: int
    ) -> pd.DataFrame:
        mask = df["count"] >= min_count
        return df.loc[mask]

    def _filter_by_length(
        self, df: pd.DataFrame, min_length: int
    ) -> pd.DataFrame:
        mask = df["name"].str.len() >= min_length
        return df.loc[mask]

    def _process_ingredient(self, ingredient: str) -> str:
        processed_ingredient = ingredient.lower()
        processed_ingredient = re.sub(
            r"[^-a-zA-Z0-9 ]", "", processed_ingredient
        ).replace("-", " ")

        return processed_ingredient

    def _plural_to_singular(self, text) -> str:
        processed_text = []
        text = self.nlp(text)
        lemma_tags = {"NNS", "NNPS"}

        for token in text:
            lemma = token.text

            if token.tag_ in lemma_tags:
                lemma = token.lemma_
            processed_text.append(lemma)

        return " ".join(processed_text)

    def _proccess_sentence(self, text: str) -> str:
        text = text.replace("(", " ")
        text = text.replace(")", " ")
        text = " ".join(text.split())
        words = text.split(" ")

        processed_text = []
        for word in words:
            processed_word = self._process_ingredient(word)
            processed_word = self._plural_to_singular(processed_word)

            processed_text.append(processed_word)

        return " ".join(processed_text)

    def find_ingredients(self, sentence: str) -> List[Tuple[str, str]]:
        sentence = self._proccess_sentence(sentence)
        words = sentence.split(" ")
        ingredients_found = []

        for i, word in enumerate(words):
            word_to_check = word
            foods_found = self.ingredient_model.search(word_to_check)
            j = i + 1

            if word_to_check in foods_found:
                ingredients_found.append((word, word_to_check))

            while len(foods_found) > 0 and j < len(words):
                word_to_check = word_to_check + " " + words[j]
                j += 1

                if word_to_check in foods_found:
                    ingredients_found.append((word, word_to_check))

        return ingredients_found


IngredientModel = Processor()
