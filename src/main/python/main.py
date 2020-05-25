from pathlib import Path
from typing import Optional

import jsonpickle
import maru
import pykakasi
from dataclasses import dataclass
from pyknp import KNP
from pymystem3 import Mystem

from src.main.python.aligned_text import AlignedText
from src.main.python.corpus_annotator import annotate_russian_text, annotate_japanese_text


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


@dataclass
class MetricsValuesPos:
    out_cnt: Optional[float]
    in_cnt: float
    total_cnt: float
    addition_size: int


@dataclass
class MetricsValues:
    verb: MetricsValuesPos
    noun: MetricsValuesPos
    lang: str

    def greater_1(self, target):
        return self.get_value_1() > target.get_value_1()

    def greater_2(self, target):
        return self.get_value_2() > target.get_value_2()

    def greater_3(self, target):
        if not (self.v_score_is_none() and target.v_score_is_none()):
            v_sc = self.verb.out_cnt / target.verb.out_cnt > self.verb.in_cnt / target.verb.in_cnt
        elif self.v_score_is_none() and not target.v_score_is_none() and target.verb.in_cnt > 0:
            v_sc = True
        else:
            v_sc = False

        if not (self.n_score_is_none() and target.n_score_is_none()):
            n_sc = self.noun.out_cnt / target.noun.out_cnt > self.noun.in_cnt / target.noun.in_cnt
        elif self.n_score_is_none() and not target.n_score_is_none() and target.noun.in_cnt > 0:
            n_sc = True
        else:
            n_sc = False

        return v_sc or n_sc

    def v_score_is_none(self):
        return (not self.verb.total_cnt > 0, not self.verb.addition_size > 0)

    def n_score_is_none(self):
        return (not self.noun.total_cnt > 0, not self.noun.addition_size > 0)

    def get_value_1(self):
        ns_tot_empty, ns_add_empty = self.n_score_is_none()
        vs_tot_empty, vs_add_empty = self.v_score_is_none()
        if ns_tot_empty:
            if ns_tot_empty:
                return 1000000.0

        if ns_tot_empty:
            if self.lang == 'ja':
                if self.noun.out_cnt == 0:
                    n_out = 7
                else:
                    n_out = self.noun.out_cnt * 1.5
            elif self.lang == 'ru':
                if self.noun.out_cnt == 0:
                    n_out = 2
                else:
                    n_out = self.noun.out_cnt * 1.5
        elif ns_add_empty:
            if self.lang == 'ja':
                n_out = 50
            elif self.lang == 'ru':
                n_out = 4
        else:
            n_out = self.noun.out_cnt

        if vs_tot_empty:
            if self.lang == 'ja':
                if self.verb.out_cnt == 0:
                    v_out = 7
                else:
                    v_out = self.verb.out_cnt * 1.5
            elif self.lang == 'ru':
                if self.verb.out_cnt == 0:
                    v_out = 2
                else:
                    v_out = self.verb.out_cnt * 1.5
        elif vs_add_empty:
            if self.lang == 'ja':
                v_out = 50
            elif self.lang == 'ru':
                v_out = 4
        else:
            v_out = self.verb.out_cnt

        return (n_out / self.noun.in_cnt) * (v_out / self.verb.in_cnt)

    def get_value_2(self):
        if self.n_score_is_none():
            if self.v_score_is_none():
                return 1000000.0
        if not self.n_score_is_none():
            if self.v_score_is_none():
                return (2 / self.verb.in_cnt) * (self.noun.total_cnt / self.noun.in_cnt)
        if not self.v_score_is_none():
            if self.n_score_is_none():
                return (2 / self.noun.in_cnt) * (self.verb.total_cnt / self.verb.in_cnt)
        return (self.noun.total_cnt / self.noun.in_cnt) * (self.verb.total_cnt / self.verb.in_cnt)


# def blank_metrics():
#     return MetricsValues(MetricsValuesPos(in_cnt=1.0, out_cnt=1000000.0, total_cnt=1, addition_size=1),
#                          MetricsValuesPos(in_cnt=1.0, out_cnt=1000000.0, total_cnt=1, addition_size=1))


def get_stats(ja_src, ru_src, rebalance=True, rebalance_several=False):
    def metrics(ja_base, ru_base, ja_bnd, ru_bnd, ja, ru, current_addition):
        res = []
        if current_addition == 'ru':
            for ps in ['VERB', 'NOUN']:
                candidates_old = list(set([item for item in list(set(sum(ru[ps][ru_base:ru_bnd-1], []))) if item != '']))
                candidates_new = list(set([item for item in list(set(sum(ru[ps][ru_bnd-1:ru_bnd], []))) if item != '' and
                                           not item in candidates_old]))
                in_cnt = len([item for item in candidates_old + candidates_new if item in sum(ja[ps][ja_base:ja_bnd], [])])
                out_cnt = len(list(set([item for item in candidates_old + candidates_new if item != '' and \
                                        item not in list(set(sum(ja[ps][ja_base:ja_bnd], [])))])))
                res.append(MetricsValuesPos(out_cnt=out_cnt, in_cnt=in_cnt + 0.1, total_cnt=len(candidates_old + candidates_new),
                                            addition_size=len(candidates_new)))
                print(f'RU:{ps} {in_cnt}/{out_cnt} | {[item for item in candidates_old if item in sum(ja[ps][ja_base:ja_bnd], [])]}'
                      f' + {[item for item in candidates_new if item in sum(ja[ps][ja_base:ja_bnd], [])]}')
        elif current_addition == 'ja':
            for ps in pos:
                candidates_old = list(set([item for item in list(set(sum(ja[ps][ja_base:ja_bnd-1], []))) if item != '']))
                candidates_new = list(set([item for item in list(set(sum(ja[ps][ja_bnd-1:ja_bnd], []))) if item != '' and
                                           not item in candidates_old]))
                in_cnt = len([item for item in sum(ru[ps][ru_base:ru_bnd], []) if item in candidates_old + candidates_new])
                out_cnt = len(list(set([item for item in candidates_old + candidates_new if item != '' and\
                                        item not in list(set(sum(ru[ps][ru_base:ru_bnd], [])))])))
                res.append(MetricsValuesPos(out_cnt=out_cnt, in_cnt=in_cnt + 0.1, total_cnt=len(candidates_old + candidates_new),
                                            addition_size=len(candidates_new)))
                print(f'JA:{ps} {in_cnt}/{out_cnt} | {[item for item in candidates_old if item in sum(ru[ps][ru_base:ru_bnd], [])]}'
                      f' + {[item for item in candidates_new if item in sum(ru[ps][ru_base:ru_bnd], [])]}')

        return MetricsValues(verb=res[0], noun=res[1], lang=current_addition)


        #     out_cnt = len(list(set(sum(ja['VERB'][ja_base:ja_bnd], [])))) - in_cnt
        #     addition_size = len([it for it in ja['VERB'][ja_bnd - 1:ja_bnd] if it != '' and
        #                          not it in sum(ja['VERB'][ja_base:ja_bnd - 1], [])])
        # verb_metrics = MetricsValuesPos(out_cnt=out_cnt, in_cnt=in_cnt + 0.1, total_cnt=len(ru_candidates),
        #                                 addition_size=addition_size)
        # print(f'VERB/in: {in_cnt} :: out: {out_cnt} |'
        #       f'{[item for item in ru_candidates if item in sum(ja["VERB"][ja_base:ja_bnd], [])]}')
        #
        # ru_candidates = [item for item in list(set(sum(ru['NOUN'][ru_base:ru_bnd], []))) if item != '']
        # in_cnt = len([item for item in ru_candidates if item in sum(ja['NOUN'][ja_base:ja_bnd], [])])
        # if current_addition == 'ru':
        #     out_cnt = len(ru_candidates) - in_cnt
        #     addition_size = len([it for it in ru['NOUN'][ru_bnd - 1:ru_bnd] if it != '' and
        #                          not it in sum(ru['NOUN'][ru_base:ru_bnd - 1], [])])
        # elif current_addition == 'ja':
        #     out_cnt = len(list(set(sum(ja['NOUN'][ja_base:ja_bnd], [])))) - in_cnt
        #     addition_size = len([it for it in ja['NOUN'][ja_bnd - 1:ja_bnd] if it != '' and
        #                          not it in sum(ja['NOUN'][ja_base:ja_bnd - 1], [])])
        # noun_metrics = MetricsValuesPos(out_cnt=out_cnt, in_cnt=in_cnt + 0.1, total_cnt=len(ru_candidates),
        #                                 addition_size=addition_size)
        # print(f'NOUN/in: {in_cnt} :: out: {out_cnt} |'
        #       f'{[item for item in ru_candidates if item in sum(ja["NOUN"][ja_base:ja_bnd], [])]}')
        #
        # return MetricsValues(verb=verb_metrics, noun=noun_metrics)

    sent_diff_mean = 2.6962334103151706
    pos = ['VERB', 'NOUN']  # , 'ADJECTIVE']

    ru = {}
    ja = {}

    print(f'File: {i}')
    for ps in pos:
        with open(f"../texts/raw/with_ann/align_data/{i}_ru_{ps}.txt", 'r') as file:
            ru[ps] = [line.strip().split(',') for line in file.readlines()]
        with open(f"../texts/raw/with_ann/align_data/{i}_ja_{ps}.txt", 'r') as file:
            ja[ps] = [line.strip().split(',') for line in file.readlines()]

    #         ja ru  ja_sc    ru_sc
    score = [[-1, -1, []]]

    while True:
        score.append([score[-1][0] + 1, score[-1][1] + 1, []])
        ja_baseline = score[-1][0]
        ru_baseline = score[-1][1]
        score[-1][2] = [metrics(ja_baseline, ru_baseline, score[-1][0] + 1, score[-1][1] + 1, ja, ru, 'ja'),
                        metrics(ja_baseline, ru_baseline, score[-1][0] + 1, score[-1][1] + 1, ja, ru, 'ru')]
        print(f'RU:{score[-1][2][1].get_value_1()} | JA:{score[-1][2][0].get_value_1()}')
        # print(' ',' '.join(ru_src[ru_baseline:score[-1][1] + 1]), '\n',
        #       ' '.join(ja_src[ja_baseline:score[-1][0] + 1]))

        ru_break_first = False
        ru_break_last = False
        ja_break_first = False
        ja_break_last = False

        while not (ru_break_last or ja_break_last):
            # +1 ru
            new_metrics = metrics(ja_baseline, ru_baseline, score[-1][0] + 1, score[-1][1] + 2, ja, ru, 'ru')
            print(f'{score[-1][2][1].get_value_1()} vs {new_metrics.get_value_1()}')
            # print(' ',' '.join(ru_src[ru_baseline:score[-1][1] + 2]), '\n',
            #       ' '.join(ja_src[ja_baseline:score[-1][0] + 1]))
            #cmp = [score[-1][2][1].greater_1(new_metrics), score[-1][2][1].greater_2(new_metrics), score[-1][2][1].greater_3(new_metrics)]
            if score[-1][2][1].greater_1(new_metrics):
                score[-1][2][1] = new_metrics
                score[-1][2][0] = metrics(ja_baseline, ru_baseline, score[-1][0] + 1, score[-1][1] + 2, ja, ru, 'ja')
                score[-1][1] += 1
                ja_break_first = False
                ja_break_last = False
            else:
                if ru_break_first:
                    ru_break_last = True
                else:
                    ru_break_first = True

            # +1 ja
            new_metrics = metrics(ja_baseline, ru_baseline, score[-1][0] + 2, score[-1][1] + 1, ja, ru, 'ja')
            print(f'{score[-1][2][0].get_value_1()} vs {new_metrics.get_value_1()}')
            # print(' ',' '.join(ru_src[ru_baseline:score[-1][1] + 1]), '\n',
            #       ' '.join(ja_src[ja_baseline:score[-1][0] + 2]))
            # cmp = [score[-1][2][0].greater_1(new_metrics), score[-1][2][0].greater_2(new_metrics), score[-1][2][0].greater_3(new_metrics)]
            if score[-1][2][0].greater_1(new_metrics):
                score[-1][2][0] = new_metrics
                score[-1][2][1] = metrics(ja_baseline, ru_baseline, score[-1][0] + 2, score[-1][1] + 1, ja, ru, 'ru')
                score[-1][0] += 1
                ru_break_first = False
                ru_break_last = False
            else:
                if ja_break_first:
                    ja_break_last = True
                else:
                    ja_break_first = True
        print(' ', ' '.join(ru_src[ru_baseline:score[-1][1] + 1]), '\n',
              ' '.join(ja_src[ja_baseline:score[-1][0] + 1]))

        if score[-1][0] == len(ja_src) or score[-1][1] == len(ru_src):
            break

    if ' '.join(ru_src[ru_baseline:score[-1][1] + 1]) == ' '.join(ja_src[ja_baseline:score[-1][0] + 1]) == '':
        score = score[:-1]
    score[-1][0] = len(ja_src)-1
    score[-1][1] = len(ru_src)-1
    score[0][2] = score[1][2]
    res = []
    ja_baseline = 0
    ru_baseline = 0

    for id, _ in enumerate(score[:-1]):
        res.append([list(range(score[id][0] + 1, score[id + 1][0]+1)),
                    list(range(score[id][1] + 1, score[id + 1][1]+1)), score[id][2]])
        # ja_baseline = score[id][0]
        # ru_baseline = score[id][1]

    if rebalance:
        for index in range(1, len(res)):
            if len(res[index][0]) > 1 and res[index][1]:
                m_without_first_element = metrics(res[index][0][1], res[index][1][0],
                                                  res[index][0][-1] + 1, res[index][1][-1] + 1,
                                                  ja, ru, 'ja')
                while res[index][2][0].greater_1(m_without_first_element):
                    res[index - 1][0].append(res[index][0][0])
                    res[index][0] = res[index][0][1:]
                    res[index][2][0] = m_without_first_element
                    res[index - 1][2][0] = metrics(res[index - 1][0][0], res[index - 1][1][0],
                                                   res[index - 1][0][-1] + 1, res[index - 1][1][-1] + 1,
                                                   ja, ru, 'ja')
                    if len(res[index][0]) > 1 and rebalance_several:
                        m_without_first_element = metrics(res[index][0][1], res[index][1][0],
                                                          res[index][0][-1] + 1, res[index][1][-1] + 1,
                                                          ja, ru, 'ja')
            if len(res[index][1]) > 1 and res[index][0]:
                m_without_first_element = metrics(res[index][0][0], res[index][1][1],
                                                  res[index][0][-1] + 1, res[index][1][-1] + 1,
                                                  ja, ru, 'ja')
                while res[index][2][1].greater_1(m_without_first_element):
                    res[index - 1][1].append(res[index][1][0])
                    res[index][1] = res[index][1][1:]
                    res[index][2][1] = m_without_first_element
                    res[index - 1][2][1] = metrics(res[index - 1][0][0], res[index][1][0],
                                                   res[index - 1][0][-1] + 1, res[index - 1][1][-1] + 1,
                                                   ja, ru, 'ru')
                    if len(res[index][1]) > 1 and rebalance_several:
                        m_without_first_element = metrics(res[index][0][0], res[index][1][1],
                                                          res[index][0][-1] + 1, res[index][1][-1] + 1,
                                                          ja, ru, 'ru')

    return [it[0:2] for it in res]

    #     new_iteration = True
    #     ja_iteration = -1
    #     ja_id = score[-1][0]
    #     ja_baseline = score[-1][0]
    #     while ja_id < len(ja_src) and not (ja_id > score[-1][0] + 1):
    #         ja_iteration += 1
    #         ru_iteration = -1
    #         ru_baseline = score[-2][1] + 1
    #         if score[-1][1] == ru_baseline:
    #             ru_id = score[-1][1]
    #         else:
    #             ru_id = score[-1][1] - 1
    #         while ru_id < len(ru_src) and ru_id + ja_id <= score[-1][1] + score[-1][0] + 1:
    #             ru_iteration += 1
    #             # if ja_iteration > 0 and ru_iteration == 0 and not new_iteration:
    #             #     ja_id -= 1
    #
    #             pos_sc = metrics(ja_baseline, ru_baseline, ja_id + 1, ru_id + 1, ja, ru)
    #             # print(f"ru: v -- {pos_sc['VERB'][0]}  n -- {pos_sc['NOUN'][0]}")
    #             # print(f"ja: v -- {pos_sc['VERB'][1]}  n -- {pos_sc['NOUN'][1]}")
    #
    #             if cur == 'ru' and score[-1][2][1].greater(pos_sc):
    #                 score[-1][1] = ru_id
    #                 score[-1][2][0] = pos_sc
    #             if ja_iteration >= ru_iteration and score[-1][2][0].greater(pos_sc):
    #                 score[-1][0] = ja_id
    #                 score[-1][2][1] = pos_sc
    #             if ru_iteration >= ja_iteration:
    #                 ru_id += 1
    #             else:
    #                 ja_id += 1
    #         new_iteration = False
    #         ja_id += 1
    #     print(' '.join(ru_src[score[-2][1] + 1:score[-1][1] + 1]), '\n',
    #           ' '.join(ja_src[score[-2][0] + 1:score[-1][0] + 1]))
    #
    # score = [sc_pair for sc_pair in score[1:] if min(sc_pair[0], sc_pair[1]) <= min(len(ja_src), len(ru_src))]
    # score[-1][0] = len(ja_src)
    # score[-1][1] = len(ru_src)

    # for id, item in enumerate(res):
    #     if not item[0]:
    #         if item[1][0] > 1:
    #             if id > 0:
    #                 pos_sc = metrics(id - 1, ja_id, ru_id, ja, ru, pos)
    #                 pass
    #         elif item[1][1] > 1:
    #             if id > 0:
    #                 pos_sc = metrics(id - 1, res[id - 1][2][0][-1], ru_id, ja, ru, pos)

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
    # get_line_info([1,11,12,13,14,15,16,17,18,19,20,21])
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

    for i in [1, 3, 7, 13, 14, 22, 41, 43, 45, 46, 47][9:10]:  # [4:]:
        with open(f"../texts/raw/with_ann/{i}_ru.json", 'r') as file:
            ru_src = [it[0] for it in jsonpickle.decode(file.read())]
        with open(f"../texts/raw/with_ann/{i}_ja.json", 'r') as file:
            ja_src = [it[0] for it in jsonpickle.decode(file.read())]
        ids = get_stats(ja_src, ru_src, rebalance=True, rebalance_several=True)
        for id_pair in ids:
            print(' '.join([ja_src[ja_id] for ja_id in id_pair[0]]), '\n',
                  ' '.join([ru_src[ru_id] for ru_id in id_pair[1]]))
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
