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


def get_stats(ja_src, ru_src):
    def metrics(ja_base, ru_base, ja_bnd, ru_bnd, ja, ru, pos):
        pos_sc = {}
        for ps in pos:
            ru_candidates = [item for item in list(set(sum(ru[ps][ru_base:ru_bnd], []))) if item != '']
            #ja_candidates = [item for item in list(set(sum(ja[ps][ja_base:ja_bnd], []))) if item != '']
            in_cnt_ja = len([item for item in ru_candidates if item in sum(ja[ps][ja_base:ja_bnd], [])])
            # print(ps, ' : ', [item for item in sum(ru[ps][ru_base:ru_bnd], []) if item in sum(ja[ps][ja_base:ja_bnd], [])])
            #in_cnt_ru = len([item for item in ja_candidates if item in sum(ru[ps][ru_base:ru_bnd], [])])
            if not ru_candidates or not [it for it in ru[ps][ru_bnd-1] if it != '']:
                out_cnt_ja = 10
            else:
                out_cnt_ja = len(ru_candidates) - in_cnt_ja
            print(f'{ps}/in: {in_cnt_ja} :: out: {out_cnt_ja} | {[item for item in ru_candidates if item in sum(ja[ps][ja_base:ja_bnd], [])]}')
            # if not ja_candidates:
            #     out_cnt_ru = 10
            # else:
            #     out_cnt_ru = len(ja_candidates) - in_cnt_ru
            pos_sc[ps] = out_cnt_ja / (in_cnt_ja + 0.1)#, out_cnt_ru / (in_cnt_ru + 0.1))
        return pos_sc

    sent_diff_mean = 2.6962334103151706
    pos = ['VERB', 'NOUN']#, 'ADJECTIVE']

    ru = {}
    ja = {}

    print(f'File: {i}')
    for ps in pos:
        with open(f"../texts/raw/with_ann/align_data/{i}_ru_{ps}.txt", 'r') as file:
            ru[ps] = [line.strip().split(',') for line in file.readlines()]
        with open(f"../texts/raw/with_ann/align_data/{i}_ja_{ps}.txt", 'r') as file:
            ja[ps] = [line.strip().split(',') for line in file.readlines()]
    #
    # with open(f"../texts/raw/with_ann/{i}_ru.json", 'r') as file:
    #     ru_src = [it[0] for it in jsonpickle.decode(file.read())]
    # with open(f"../texts/raw/with_ann/{i}_ja.json", 'r') as file:
    #     ja_src = [it[0] for it in jsonpickle.decode(file.read())]

    #         ja ru  ja_sc    ru_sc
    score = [[-1, -1,  [0.0,    0.0]],
             [0, 0,  [1000000.0, 1000000.0]]]

    for counter in range(0, min(len(ja_src), len(ru_src))):
        ja_iteration = -1
        ja_id = score[-1][0]
        ja_baseline = score[-1][0]
        while ja_id < len(ja_src) and not (ja_id > score[-1][0] + 1):
            ja_iteration += 1
            ru_iteration = -1
            ru_id = score[-1][1]
            ru_baseline = score[-1][1]
            while ru_id < len(ru_src) and ru_id + ja_id <= score[-1][1] + score[-1][0] + 1:
                ru_iteration += 1

                pos_sc = metrics(ja_baseline, ru_baseline, ja_id + 1, ru_id + 1, ja, ru, pos)
                # print(f"ru: v -- {pos_sc['VERB'][0]}  n -- {pos_sc['NOUN'][0]}")
                # print(f"ja: v -- {pos_sc['VERB'][1]}  n -- {pos_sc['NOUN'][1]}")

                if ru_iteration >= ja_iteration and score[-1][2][0] > pos_sc['VERB'] * pos_sc['NOUN']:
                    score[-1][1] = ru_id
                    score[-1][2][0] = pos_sc['VERB'] * pos_sc['NOUN']
                if ja_iteration >= ru_iteration and score[-1][2][1] > pos_sc['VERB'] * pos_sc['NOUN']:
                    score[-1][0] = ja_id
                    score[-1][2][1] = pos_sc['VERB'] * pos_sc['NOUN']
                ru_id += 1
            ja_id += 1
        print(' '.join(ru_src[score[-2][1] + 1:score[-1][1] + 1]), '\n', ' '.join(ja_src[score[-2][0] + 1:score[-1][0] + 1]))
        score.append([score[-1][0] + 1, score[-1][1] + 1, [1000000.0, 1000000.0]])



    score = [sc_pair for sc_pair in score[1:] if min(sc_pair[0], sc_pair[1]) <= min(len(ja_src), len(ru_src))]
    score[-1][1] = len(ru_src)
    res = []
    ja_baseline = 0
    ru_baseline = 0
    for id, _ in enumerate(score[:-1]):
        ja_id = score[id+1][0] - score[id][0]
        ru_id = score[id+1][1] - score[id][1]
        res.append((list(range(ja_baseline, score[id+1][0])), list(range(ru_baseline, score[id+1][1]))))
        ja_baseline += ja_id
        ru_baseline += ru_id

    # for id, item in enumerate(res):
    #     if not item[0]:
    #         if item[1][0] > 1:
    #             if id > 0:
    #                 pos_sc = metrics(id - 1, ja_id, ru_id, ja, ru, pos)
    #                 pass
    #         elif item[1][1] > 1:
    #             if id > 0:
    #                 pos_sc = metrics(id - 1, res[id - 1][2][0][-1], ru_id, ja, ru, pos)

    return res

    # for ja_id in range(0, len(ja_src)):
    #     for ru_id in range(score[ja_id][0], len(ru_src) + 1):
    #         if ru_id > score[ja_id][0] + 1:
    #             continue
    #         pos_sc = {}
    #         for ps in pos:
    #             in_cnt = len([item for item in sum(ru[ps][ja_id:ru_id], []) if item in ja[ps][ja_id]])
    #             out_cnt = len(sum(ru[ps][ja_id:ru_id], [])) - in_cnt
    #             pos_sc[ps] = out_cnt / (in_cnt + 1)
    #         if score[ja_id][1] > pos_sc['VERB'] * (pos_sc['NOUN']):
    #             score[ja_id] = (ru_id, pos_sc['VERB'] * pos_sc['NOUN'])
    #         else:
    #             score[ja_id + 1] = (score[ja_id][0] + 1, 1000)
    #             if ja_id == 0:
    #                 print(' '.join(ru_src[0:score[ja_id][0]]), '\n', ja_src[ja_id])
    #             else:
    #                 print(' '.join(ru_src[score[ja_id - 1][0]:score[ja_id][0]]), '\n', ja_src[ja_id])




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

    for i in [1, 3, 7, 13, 14, 22, 41, 43, 45, 46, 47][4:]:
        with open(f"../texts/raw/with_ann/{i}_ru.json", 'r') as file:
            ru_src = [it[0] for it in jsonpickle.decode(file.read())]
        with open(f"../texts/raw/with_ann/{i}_ja.json", 'r') as file:
            ja_src = [it[0] for it in jsonpickle.decode(file.read())]
        ids = get_stats(ja_src, ru_src)
        for id_pair in ids:
            print(' '.join([ja_src[ja_id] for ja_id in id_pair[0]]), '\n', ' '.join([ru_src[ru_id] for ru_id in id_pair[1]]))
        print(1)


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
