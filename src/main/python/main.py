from pathlib import Path
from statistics import mean
from typing import Optional

import jsonpickle
import maru
import pykakasi
from dataclasses import dataclass
from pyknp import KNP
from pymystem3 import Mystem

from src.main.python.aligned_text import AlignedText
from src.main.python.corpus_annotator import annotate_russian_text, annotate_japanese_text, Entry, Attribute


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

    pos = ['VERB', 'NOUN']  # , 'ADJECTIVE']
    pos2 = ['Verb', 'Noun']  # , 'Adjective']

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

    def copy(self, src):
        self.out_cnt = src.out_cnt
        self.in_cnt = src.in_cnt
        self.total_cnt = src.total_cnt
        self.addition_size = src.addition_size


@dataclass
class MetricsValues:
    verb: MetricsValuesPos
    noun: MetricsValuesPos
    lang: str

    def copy(self, src):
        self.verb.copy(src.verb)
        self.noun.copy(src.noun)
        self.lang = src.lang

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
        return not self.verb.total_cnt > 0, not self.verb.addition_size > 0

    def n_score_is_none(self):
        return not self.noun.total_cnt > 0, not self.noun.addition_size > 0

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


def get_stats(ja_src, ru_src, rebalance=True, rebalance_several=False):
    def metrics(ja_base: int, ru_base: int, ja_bnd: int, ru_bnd: int, ja: [str], ru: [str], current_addition: str):
        res = []
        if current_addition == 'ru':
            for ps in ['VERB', 'NOUN']:
                candidates_old = list(
                    set([item for item in list(set(sum(ru[ps][ru_base:ru_bnd - 1], []))) if item != '']))
                candidates_new = list(
                    set([item for item in list(set(sum(ru[ps][ru_bnd - 1:ru_bnd], []))) if item != '' and
                         not item in candidates_old]))
                in_cnt = len(
                    [item for item in candidates_old + candidates_new if item in sum(ja[ps][ja_base:ja_bnd], [])])
                out_cnt = len(list(set([item for item in candidates_old + candidates_new if item != '' and \
                                        item not in list(set(sum(ja[ps][ja_base:ja_bnd], [])))])))
                res.append(MetricsValuesPos(out_cnt=out_cnt, in_cnt=in_cnt + 0.1,
                                            total_cnt=len(candidates_old + candidates_new),
                                            addition_size=len(candidates_new)))
                print(
                    f'RU:{ps} {in_cnt}/{out_cnt} | {[item for item in candidates_old if item in sum(ja[ps][ja_base:ja_bnd], [])]}'
                    f' + {[item for item in candidates_new if item in sum(ja[ps][ja_base:ja_bnd], [])]}')
        elif current_addition == 'ja':
            for ps in pos:
                candidates_old = list(
                    set([item for item in list(set(sum(ja[ps][ja_base:ja_bnd - 1], []))) if item != '']))
                candidates_new = list(
                    set([item for item in list(set(sum(ja[ps][ja_bnd - 1:ja_bnd], []))) if item != '' and
                         not item in candidates_old]))
                in_cnt = len(
                    [item for item in sum(ru[ps][ru_base:ru_bnd], []) if item in candidates_old + candidates_new])
                out_cnt = len(list(set([item for item in candidates_old + candidates_new if item != '' and \
                                        item not in list(set(sum(ru[ps][ru_base:ru_bnd], [])))])))
                res.append(MetricsValuesPos(out_cnt=out_cnt, in_cnt=in_cnt + 0.1,
                                            total_cnt=len(candidates_old + candidates_new),
                                            addition_size=len(candidates_new)))
                print(
                    f'JA:{ps} {in_cnt}/{out_cnt} | {[item for item in candidates_old if item in sum(ru[ps][ru_base:ru_bnd], [])]}'
                    f' + {[item for item in candidates_new if item in sum(ru[ps][ru_base:ru_bnd], [])]}')

        return MetricsValues(verb=res[0], noun=res[1], lang=current_addition)

    def prev(id: int, mode: int):
        if mode == 1:
            return id - 1
        elif mode == -1:
            return id + 1
        else:
            return -1

    pos = ['VERB', 'NOUN']  # , 'ADJECTIVE']

    ru = {}
    ja = {}

    print(f'File: {i}')
    for ps in pos:
        with open(f"../texts/raw/with_ann/align_data/{i}_ru_{ps}.txt", 'r') as file:
            ru[ps] = [line.strip().split(',') for line in file.readlines()]
        with open(f"../texts/raw/with_ann/align_data/{i}_ja_{ps}.txt", 'r') as file:
            ja[ps] = [line.strip().split(',') for line in file.readlines()]

    #         ja  ru  ja_sc, ru_sc
    score = [[-1, -1, []]]

    while True:
        score.append([score[-1][0] + 1, score[-1][1] + 1, []])

        if score[-1][0] == len(ja_src) or score[-1][1] == len(ru_src):
            break

        ja_baseline = score[-1][0]
        ru_baseline = score[-1][1]
        score[-1][2] = [metrics(ja_baseline, ru_baseline, score[-1][0] + 1, score[-1][1] + 1, ja, ru, 'ja'),
                        metrics(ja_baseline, ru_baseline, score[-1][0] + 1, score[-1][1] + 1, ja, ru, 'ru')]
        print(f'RU:{score[-1][2][1].get_value_1()} | JA:{score[-1][2][0].get_value_1()}')
        # print(' ',' '.join(ru_src[ru_baseline:score[-1][1] + 1]), '\n',
        #       ' '.join(ja_src[ja_baseline:score[-1][0] + 1]))

        ru_break = False
        ja_break = False

        while True:
            # +1 ru
            new_metrics = metrics(ja_baseline, ru_baseline, score[-1][0] + 1, score[-1][1] + 2, ja, ru, 'ru')
            print(f'RU:{score[-1][2][1].get_value_1()} vs RU:{new_metrics.get_value_1()}')
            # print(' ',' '.join(ru_src[ru_baseline:score[-1][1] + 2]), '\n',
            #       ' '.join(ja_src[ja_baseline:score[-1][0] + 1]))
            # cmp = [score[-1][2][1].greater_1(new_metrics), score[-1][2][1].greater_2(new_metrics), score[-1][2][1].greater_3(new_metrics)]
            if score[-1][2][1].greater_1(new_metrics):
                score[-1][2][1].copy(new_metrics)
                score[-1][2][0].copy(
                    metrics(ja_baseline, ru_baseline, score[-1][0] + 1, score[-1][1] + 2, ja, ru, 'ja'))
                score[-1][1] += 1
                ja_break = False
            else:
                ru_break = True

            if ru_break and ja_break:
                break

            # +1 ja
            new_metrics = metrics(ja_baseline, ru_baseline, score[-1][0] + 2, score[-1][1] + 1, ja, ru, 'ja')
            print(f'JA:{score[-1][2][0].get_value_1()} vs JA:{new_metrics.get_value_1()}')
            # print(' ',' '.join(ru_src[ru_baseline:score[-1][1] + 1]), '\n',
            #       ' '.join(ja_src[ja_baseline:score[-1][0] + 2]))
            # cmp = [score[-1][2][0].greater_1(new_metrics), score[-1][2][0].greater_2(new_metrics), score[-1][2][0].greater_3(new_metrics)]
            if score[-1][2][0].greater_1(new_metrics):
                score[-1][2][0].copy(new_metrics)
                score[-1][2][1].copy(
                    metrics(ja_baseline, ru_baseline, score[-1][0] + 2, score[-1][1] + 1, ja, ru, 'ru'))
                score[-1][0] += 1
                ru_break = False
            else:
                ja_break = True

            if ru_break and ja_break:
                break

        print(' ', ' '.join(ru_src[ru_baseline:score[-1][1] + 1]), '\n',
              ' '.join(ja_src[ja_baseline:score[-1][0] + 1]))

    # if ' '.join(ru_src[ru_baseline:score[-1][1] + 1]) == ' '.join(ja_src[ja_baseline:score[-1][0] + 1]) == '':
    #     score = score[:-1]
    score[-1][0] = len(ja_src) - 1
    score[-1][1] = len(ru_src) - 1
    # score[0][2].copy(score[1][2])
    res = []
    ja_baseline = 0
    ru_baseline = 0

    for id, _ in enumerate(score[1:-1]):
        res.append([list(range(score[id][0] + 1, score[id + 1][0] + 1)),
                    list(range(score[id][1] + 1, score[id + 1][1] + 1)), score[id + 1][2]])
        # ja_baseline = score[id][0]
        # ru_baseline = score[id][1]

    loop_ids = [[1, len(res), 1], [len(res) - 2, -1, -1]]

    if rebalance:
        for loop_id in loop_ids:
            for index in range(loop_id[0], loop_id[1], loop_id[2]):
                while len(res[index][0]) > 1 and res[index][1]:
                    m_without_first_element = metrics(res[index][0][1],
                                                      res[index][1][0],
                                                      res[index][0][-1] + 1,
                                                      res[index][1][-1] + 1,
                                                      ja, ru, 'ja')
                    m_with_first_element = metrics(res[prev(index, loop_id[2])][0][0],
                                                   res[prev(index, loop_id[2])][1][0],
                                                   res[prev(index, loop_id[2])][0][-1] + 2,
                                                   res[prev(index, loop_id[2])][1][-1] + 1,
                                                   ja, ru, 'ja')
                    if mean([m_without_first_element.get_value_1(),
                             m_with_first_element.get_value_1()]) < \
                            mean([res[index][2][0].get_value_1(),
                                  res[prev(index, loop_id[2])][2][0].get_value_1()]):
                        res[prev(index, loop_id[2])][0].append(res[index][0][0])
                        res[index][0] = res[index][0][1:]
                        res[index][2][0].copy(m_without_first_element)
                        res[prev(index, loop_id[2])][2][0].copy(m_with_first_element)
                        res[index][2][1] = metrics(res[index][0][0],
                                                   res[index][1][0],
                                                   res[index][0][-1] + 1,
                                                   res[index][1][-1] + 1,
                                                   ja, ru, 'ru')
                        res[prev(index, loop_id[2])][2][1] = metrics(res[prev(index, loop_id[2])][0][0],
                                                                     res[prev(index, loop_id[2])][1][0],
                                                                     res[prev(index, loop_id[2])][0][-1] + 1,
                                                                     res[prev(index, loop_id[2])][1][-1] + 1,
                                                                     ja, ru, 'ru')
                    else:
                        break
                    if not rebalance_several:
                        break
                while len(res[index][1]) > 1 and res[index][0]:
                    m_without_first_element = metrics(res[index][0][0],
                                                      res[index][1][1],
                                                      res[index][0][-1] + 1,
                                                      res[index][1][-1] + 1,
                                                      ja, ru, 'ru')
                    m_with_first_element = metrics(res[prev(index, loop_id[2])][0][0],
                                                   res[prev(index, loop_id[2])][1][0],
                                                   res[prev(index, loop_id[2])][0][-1] + 1,
                                                   res[prev(index, loop_id[2])][1][-1] + 2,
                                                   ja, ru, 'ru')
                    if mean([m_without_first_element.get_value_1(),
                             m_with_first_element.get_value_1()]) < \
                            mean([res[index][2][1].get_value_1(),
                                  res[prev(index, loop_id[2])][2][1].get_value_1()]):
                        res[prev(index, loop_id[2])][1].append(res[index][1][0])
                        res[index][1] = res[index][1][1:]
                        res[index][2][1].copy(m_without_first_element)
                        res[prev(index, loop_id[2])][2][1].copy(m_with_first_element)
                        res[index][2][0] = metrics(res[index][0][0],
                                                   res[index][1][0],
                                                   res[index][0][-1] + 1,
                                                   res[index][1][-1] + 1,
                                                   ja, ru, 'ja')
                        res[prev(index, loop_id[2])][2][0] = metrics(res[prev(index, loop_id[2])][0][0],
                                                                     res[prev(index, loop_id[2])][1][0],
                                                                     res[prev(index, loop_id[2])][0][-1] + 1,
                                                                     res[prev(index, loop_id[2])][1][-1] + 1,
                                                                     ja, ru, 'ja')
                    else:
                        break
                    if not rebalance_several:
                        break
                print(' '.join([ja_src[ja_id] for ja_id in res[prev(index, loop_id[2])][0]]), '\n',
                      ' '.join([ru_src[ru_id] for ru_id in res[prev(index, loop_id[2])][1]]))

    return [it[0:2] for it in res]


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


# def add_xtra_attr(fname):
#     text_broken = Entry.from_xml(f'../texts/annotated/{fname}.xml')
#     text = Entry.from_xml(f'../texts/annotated_old/{fname}.xml')
#     for spair_id, spair in enumerate(text.sentence_pairs):
#         for token_id, token in enumerate(spair.japanese):
#             if token.extra_attributes and not text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes:
#                 text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes = token.extra_attributes
#             if text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes and 'reading_type' in text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes:
#                 if not [tok for tok in text_broken.sentence_pairs[spair_id].japanese[token_id].attributes if tok.name == 'reading_type']:
#                     if 'On' in text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes:
#                         text_broken.sentence_pairs[spair_id].japanese[token_id].attributes.append(Attribute('reading_type', 'On'))
#                         text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes.remove('On')
#                     else:
#                         text_broken.sentence_pairs[spair_id].japanese[token_id].attributes.append(Attribute('reading_type', 'Kun'))
#                         text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes.remove('Kun')
#                     text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes.remove('reading_type')
#             if text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes:
#                 if 'On' in text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes:
#                     text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes.remove('On')
#                 if 'Kun' in text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes:
#                     text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes.remove('Kun')
#                 if 'reading_type' in text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes:
#                     text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes.remove('reading_type')
#             if text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes and\
#                 'Judgemental' in text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes and\
#                 [tok for tok in text_broken.sentence_pairs[spair_id].japanese[token_id].attributes if tok.name == 'pos']:
#                 text_broken.sentence_pairs[spair_id].japanese[token_id].extra_attributes.remove('Judgemental')
#
#     for spair_id, spair in enumerate(text.sentence_pairs):
#         for token_id, token in enumerate(spair.russian):
#             if token.extra_attributes and not text_broken.sentence_pairs[spair_id].russian[token_id].extra_attributes:
#                 text_broken.sentence_pairs[spair_id].russian[token_id].extra_attributes = token.extra_attributes
#     return text_broken


if __name__ == '__main__':
    # get_line_info([1,11,12,13,14,15,16,17,18,19,20,21])
    # align_texts()
    # annotate_texts()

    knp = KNP()
    kakasi = pykakasi.kakasi()
    kakasi.setMode("H", "a")
    kakasi.setMode("K", "a")
    kakasi.setMode("r", "Hepburn")
    converter = kakasi.getConverter()

    # mystem = Mystem(generate_all=True, use_english_names=True, weight=True)
    # maru_analyzer = maru.get_analyzer(tagger='rnn', lemmatizer='dummy')

    # ann_ru([1, 3, 7, 13, 14, 22, 41, 43, 45, 46, 47], mystem, maru_analyzer)

    # for i in [1, 3, 7, 13, 14, 22, 41, 43, 45, 46, 47][0:1]:  # [4:]:
    #     with open(f"../texts/raw/with_ann/{i}_ru.json", 'r') as file:
    #         ru_src = [it[0] for it in jsonpickle.decode(file.read())]
    #     with open(f"../texts/raw/with_ann/{i}_ja.json", 'r') as file:
    #         ja_src = [it[0] for it in jsonpickle.decode(file.read())]
    #     ids = get_stats(ja_src, ru_src, rebalance=True, rebalance_several=True)
    #     for id_pair in ids:
    #         print(' '.join([ja_src[ja_id] for ja_id in id_pair[0]]), '\n',
    #               ' '.join([ru_src[ru_id] for ru_id in id_pair[1]]))
    # print(1)

    # ru_t = 0
    # ja_t = 0
    #
    # for f in Path("../texts/annotated").glob("*.xml"):
    #     for sp in Entry.from_xml(f).sentence_pairs:
    #         ru_t += len([t for t in sp.russian if t.attributes])
    #         ja_t += len([t for t in sp.japanese if t.lexeme])
    #
    # print(f'Ru tokens: {ru_t} | Ja tokens: {ja_t}')
    # for i in range(11, 49):
    #     broken_text = add_xtra_attr(i)
    #     with open(f'../texts/annotated/{i}.xml', 'w') as f:
    #         xml = broken_text.to_xml()
    #         xml.export(f, level=0)
    #     print(i)