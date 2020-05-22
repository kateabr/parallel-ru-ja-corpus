from pathlib import Path
from statistics import mean

import jsonpickle
import maru
import pykakasi
from pyknp import KNP
from pymystem3 import Mystem

from src.main.python.aligned_text import AlignedText
from src.main.python.corpus_annotator import annotate_russian_text, annotate_japanese_text
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


def get_line_info(indices):
    mystem = Mystem(generate_all=True, use_english_names=True, weight=True)
    maru_analyzer = maru.get_analyzer(tagger='rnn', lemmatizer='dummy')

    pos = ['VERB', 'NOUN', 'ADJECTIVE']
    pos2 = ['Verb', 'Noun', 'Adjective']

    for i in indices:
        with open(f'../texts/raw/with_ann/{i}_ru.json', 'r') as f:
            txt = f.read()
            entry = jsonpickle.decode(txt)

        for ps in pos:
            with open(f"../texts/raw/with_ann/align_data/{i}_ru_{ps}.txt", 'w+') as file:
                for line in entry:
                    ppp = [word.lexeme for word in line[1] if word.lexeme and word.get_attr_value('pos') == ps]
                    file.write(','.join(ppp) + '\n')

        with open(f'../texts/raw/with_ann/{i}_ja.json', 'r') as f:
            txt = f.read()
            entry = jsonpickle.decode(txt)

        for pos_idx, ps in enumerate(pos):
            with open(f"../texts/raw/with_ann/align_data/{i}_ja_{ps}.txt", 'w+') as file:
                for line in entry:
                    ppp = sum(
                        [annotate_russian_text(mystem, maru_analyzer, word.translation) for word in line[1] if
                         word.attributes and word.translation and word.get_attr_value('pos') == pos2[pos_idx]], [])
                    ppp = [w.lexeme.lower() for w in ppp if w.lexeme and w.get_attr_value('pos') == ps]
                    file.write(','.join(ppp) + '\n')


def get_stats(indices):
    def balance(ru_bound_left, ru_bound_right, score, final_sent_keys):
        if ru_bound_left < ru_bound_right:
            rng_ru = range(ru_bound_left, ru_bound_right)
        else:
            rng_ru = range(ru_bound_left, ru_bound_right, -1)

        for ru_id in rng_ru:
            min_noun_val = 1000000
            min_verb_val = 1000000
            for ja_id in score[ru_id].keys():
                if score[ru_id][ja_id]['NOUN'] * score[ru_id][ja_id]['VERB'] < min_noun_val * min_verb_val:
                    final_sent_keys[ru_id] = ja_id
                    min_noun_val = score[ru_id][ja_id]['NOUN']
                    min_verb_val = score[ru_id][ja_id]['VERB']

        return final_sent_keys

    sent_diff_mean = 2.6962334103151706
    pos = ['VERB', 'NOUN']#, 'ADJECTIVE']

    ru = {}
    ja = {}

    for i in indices[1:]:
        print(f'File: {i}')
        for ps in pos:
            with open(f"../texts/raw/with_ann/align_data/{i}_ru_{ps}.txt", 'r') as file:
                ru[ps] = [line.strip().split(',') for line in file.readlines()]
            with open(f"../texts/raw/with_ann/align_data/{i}_ja_{ps}.txt", 'r') as file:
                ja[ps] = [line.strip().split(',') for line in file.readlines()]

        with open(f"../texts/raw/with_ann/{i}_ru.json", 'r') as file:
            ru_src = [it[0] for it in jsonpickle.decode(file.read())]
        with open(f"../texts/raw/with_ann/{i}_ja.json", 'r') as file:
            ja_src = [it[0] for it in jsonpickle.decode(file.read())]

        score = dict({0: (1, 1000)})
        score[len(ja_src)-1] = (len(ru_src), 0)

        for ja_id in range(0, len(ja_src)):
            for ru_id in range(score[ja_id][0], len(ru_src) + 1):
                if ru_id > score[ja_id][0] + 1:
                    continue
                pos_sc = {}
                for ps in pos:
                    in_cnt = len([item for item in sum(ru[ps][ja_id:ru_id], []) if item in ja[ps][ja_id]])
                    out_cnt = len(sum(ru[ps][ja_id:ru_id], [])) - in_cnt
                    pos_sc[ps] = out_cnt / (in_cnt + 1)
                if score[ja_id][1] > pos_sc['VERB'] * (pos_sc['NOUN']):
                    score[ja_id] = (ru_id, pos_sc['VERB'] * pos_sc['NOUN'])
                else:
                    score[ja_id + 1] = (score[ja_id][0] + 1, 1000)
                    if ja_id == 0:
                        print(' '.join(ru_src[0:score[ja_id][0]]), '\n', ja_src[ja_id])
                    else:
                        print(' '.join(ru_src[score[ja_id - 1][0]:score[ja_id][0]]), '\n', ja_src[ja_id])




def ann_jap(ids, kakasi_converter, knp):
    for id in ids:
        with open(f'../texts/raw/{id}_ja.txt', 'r') as f:
            j_text = f.readlines()
        j_text_annotated = [annotate_japanese_text(knp, kakasi_converter, sentence) for sentence in j_text]
        j_text_annotated_w_sent = [(''.join([token.text for token in sent]), sent) for sent in j_text_annotated]
        with open(f'../texts/raw/with_ann/{id}_ja.json', 'w') as f:
            f.write(jsonpickle.encode(j_text_annotated_w_sent))


def ann_ru(ids, mystem, maru_analyzer):
    for id in ids:
        with open(f'../texts/raw/{id}_ru.txt', 'r') as f:
            ru_txt = f.readlines()
        r_text_annotated = [annotate_russian_text(mystem, maru_analyzer, sentence) for sentence in ru_txt]
        r_text_annotated_w_sent = [(''.join([token.text for token in sent]), sent) for sent in r_text_annotated]
        with open(f'../texts/raw/with_ann/{id}_ru.json', 'w') as f:
            f.write(jsonpickle.encode(r_text_annotated_w_sent))


if __name__ == '__main__':
    #get_line_info([1,11,12,13,14,15,16,17,18,19,20,21])
    # align_texts()
    # annotate_texts()

    # knp = KNP()
    # kakasi = pykakasi.kakasi()
    # kakasi.setMode("H", "a")
    # kakasi.setMode("K", "a")
    # kakasi.setMode("r", "Hepburn")
    # converter = kakasi.getConverter()

    # mystem = Mystem(generate_all=True, use_english_names=True, weight=True)
    # maru_analyzer = maru.get_analyzer(tagger='rnn', lemmatizer='dummy')

    # ann_ru([1, 3, 7, 13, 14, 22, 41, 43, 45, 46, 47], mystem, maru_analyzer)

    get_stats([1, 3, 7, 13, 14, 22, 41, 43, 45, 46, 47])


    # mean diff in sentence length: 2.6962334103151706


    # ids = [i for i in range(1, 49)]
    # ids.remove(2)
    # ids.remove(10)
    #
    # len_ratio = []
    #
    # for i in ids:
    #     entry = Entry.from_xml(f'../texts/annotated/{i}.xml')
    #     for sp in entry.sentence_pairs:
    #         len_ratio.append((len(sp.russian_source), len(sp.japanese_source)))
    #     print(f'{i}/{len(ids)-1}')
    #
    # print(mean([item[0] / item[1] for item in len_ratio]))
    # pass
