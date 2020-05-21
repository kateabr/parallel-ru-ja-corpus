from pathlib import Path

import maru
import pykakasi
from pyknp import KNP
from pymystem3 import Mystem

from src.main.python.aligned_text import AlignedText
from src.main.python.corpus_annotator import annotate_russian_text
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

    for text in texts[36:]:
        print(f"Processing {text.id}")
        entry = text.to_annotated(mystem, maru_analyzer, knp, kakasi)

        with open(f"../texts/annotated/{text.id}.xml", 'w') as f:
            xml = entry.to_xml()
            xml.export(f, 0)

        print(f"Saved {text.id}!")


def get_align_info(indices):
    mystem = Mystem(generate_all=True, use_english_names=True, weight=True)
    maru_analyzer = maru.get_analyzer(tagger='rnn', lemmatizer='dummy')

    pos = ['VERB', 'NOUN', 'ADJECTIVE']
    pos2 = ['Verb', 'Noun', 'Adjective']

    for i in indices:
        entry = Entry.from_xml(Path(f'../texts/annotated/{i}.xml'))

        for ps in pos:
            with open(f"../texts/annotated/align_data/{i}_ru_{ps}.txt", 'w+') as file:
                for line in entry.sentence_pairs:
                    ppp = [word.lexeme for word in line.russian if word.lexeme and word.get_attr_value('pos') == ps]
                    file.write(','.join(ppp) + '\n')

        for pos_idx, ps in enumerate(pos):
            with open(f"../texts/annotated/align_data/{i}_ja_{ps}.txt", 'w+') as file:
                for line in entry.sentence_pairs:
                    ppp = sum(
                        [annotate_russian_text(mystem, maru_analyzer, word.translation) for word in line.japanese if
                         word.attributes and word.translation and word.get_attr_value('pos') == pos2[pos_idx]], [])
                    ppp = [w.lexeme.lower() for w in ppp if w.lexeme and w.get_attr_value('pos') == ps]
                    file.write(','.join(ppp) + '\n')

        # with open(f"../texts/annotated/align_data/{i}_ja_ru.txt", 'w+') as file:
        #     for line in entry.sentence_pairs:
        #         file.write('〇\n' + line.japanese_source + '\n●\n')
        #         file.write(line.russian_source + '\n◎\n\n')


if __name__ == '__main__':
    # get_align_info([1,11,12,13,14,15,16,17,18,19,20,21])
    # align_texts()
    # annotate_texts()
    pass
