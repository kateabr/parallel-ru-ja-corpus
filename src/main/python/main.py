from pathlib import Path

import maru
import pykakasi
from pyknp import KNP
from pymystem3 import Mystem

from src.main.python.aligned_text import AlignedText
from src.main.python.corpus_model import Entry


def annotate_texts():
    texts = [AlignedText.from_json(f) for f in
             Path("../texts/aligned").glob("*.json")]

    mystem = Mystem(generate_all=True, use_english_names=True, weight=True)
    maru_analyzer = maru.get_analyzer(tagger='rnn', lemmatizer='dummy')

    knp = KNP()
    kakasi = pykakasi.kakasi()
    kakasi.setMode("H", "a")
    kakasi.setMode("K", "a")
    kakasi.setMode("r", "Hepburn")
    converter = kakasi.getConverter()

    for text in texts[:1]:
        print(f"Processing {text.id}")
        entry = text.to_annotated(mystem, maru_analyzer, knp, kakasi)

        with open(f"../texts/annotated/{text.id}.xml", 'w') as f:
            xml = entry.to_xml()
            xml.export(f, 0)

        print(f"Saved {text.id}!")


def align_texts():
    # for i in range(4,8):
    #     with open(f'../texts/raw/ru/{i}.txt') as f:
    #         ru_text = f.readlines()
    #     with open(f'../texts/translated/ja/{i}.txt') as f:
    #         ja_text = f.readlines()
    #
    #     mystem = Mystem(generate_all=True, use_english_names=True, weight=True)
    #     maru_analyzer = maru.get_analyzer(tagger='rnn', lemmatizer='dummy')
    #
    #     align(i, ru_text, ja_text, mystem, maru_analyzer)

    entry = Entry.from_xml(Path("../texts/translated/1.xml"))

    # knp = KNP()
    # kakasi = pykakasi.kakasi()
    # kakasi.setMode("H", "a")
    # kakasi.setMode("K", "a")
    # kakasi.setMode("r", "Hepburn")
    # converter = kakasi.getConverter()

    # ru_lines_annotated = [annotate_russian_text(mystem, maru_analyzer, line) for line in ru_text[2:]]
    # ja_lines_annotated = [annotate_japanese_text(knp, converter, line) for line in ja_text[2:]]

    # with open('../texts/raw/ru/1_annotated.txt', 'w', encoding='utf-8') as f:
    #     json = jsonpickle.encode(ru_lines_annotated)
    #     f.write(json)

    # with open('../texts/raw/ru/1_annotated.txt', 'r', encoding='utf-8') as f:
    #     ru_text = jsonpickle.decode(f.read())
    #
    # with open('../texts/raw/ja/1_annotated.txt', 'r', encoding='utf-8') as f:
    #     ja_text = jsonpickle.decode(f.read())


if __name__ == '__main__':
    # align_texts()
    annotate_texts()
