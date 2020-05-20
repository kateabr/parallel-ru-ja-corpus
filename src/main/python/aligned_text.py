import json
from pathlib import Path
from typing import List, Optional

from dataclasses import dataclass, asdict
from maru.analyzer import Analyzer
from pykakasi import kakasi
from pyknp import KNP
from pymystem3 import Mystem

from src.main.python.corpus_annotator import annotate_text, annotate_russian_text
from src.main.python.corpus_model import Entry


@dataclass
class AlignedText:
    @dataclass
    class Title:
        russian: Optional[str] = None
        japanese: Optional[str] = None

    @dataclass
    class Url:
        russian: Optional[str] = None
        japanese: Optional[str] = None

    @dataclass
    class SentencePair:
        russian: str
        japanese: str

    id: str
    title: Optional[Title]
    url: Optional[Url]
    sentences: List[SentencePair]

    @staticmethod
    def from_json(filename: Path, encoding: str = 'utf-8'):
        with open(filename, 'r', encoding=encoding) as f:
            obj: dict = json.loads(f.read())

            title = obj.get('title')
            url = obj.get('url')
            return AlignedText(
                obj['id'],
                AlignedText.Title(title.get('russian'), title.get('japanese')) if title is not None else None,
                AlignedText.Url(url.get('russian'), url.get('japanese')) if url is not None else None,
                [AlignedText.SentencePair(p['russian'], p['japanese']) for p in obj['sentences']]
            )

    def to_json(self, filename: Path, encoding: str = 'utf-8') -> None:
        with open(filename, 'w', encoding=encoding) as f:
            json.dump(asdict(self), f, ensure_ascii=False)

    def to_annotated(
            self,
            mystem: Mystem,
            maru_analyzer: Analyzer,
            knp: KNP,
            kakasi_converter: kakasi
    ) -> Entry:
        return annotate_text(
            mystem, maru_analyzer, knp, kakasi_converter,
            str(self.id),
            [s.russian for s in self.sentences],
            [s.japanese for s in self.sentences],
            self.title.russian,
            self.title.japanese,
            self.url.russian,
            self.url.japanese
        )


def align(file_id, ru_lines: List[str], ja_lines: List[str], mystem: Mystem, maru_analyzer: Analyzer) -> AlignedText:
    # ru_lines_annotated_with_pivots = []
    pos = ['VERB', 'NOUN', 'ADJECTIVE']
    pos2 = ['Verb', 'Noun', 'Adjective']

    for ps in pos:
        for id, line in enumerate(ru_lines):
            with open(f"stats/{file_id}_ru_{ps}.txt", 'w') as file:
                ppp = [word.lexeme for word in line if word.lexeme and word.get_attr_value('pos') == ps]
                file.write(','.join(ppp) + '\n')

    for i, ps in enumerate(pos):
        for id, line in enumerate(ja_lines):
            with open(f"stats/{id}_ja_{ps}.txt", 'w') as file:
                ppp = sum([annotate_russian_text(mystem, maru_analyzer, word.translation) for word in line if
                           word.attributes and word.translation and word.get_attr_value('pos') == pos2[i]], [])
                ppp = [w.lexeme.lower() for w in ppp if w.lexeme and w.get_attr_value('pos') == ps]
                file.write(','.join(ppp) + '\n')
    # for id, line in enumerate(ru_lines):
    #     verbs = [word.lexeme for word in line if word.lexeme and word.get_attr_value('pos') == 'VERB']
    # nouns = [word.lexeme for word in line if word.lexeme and word.get_attr_value('pos') == 'NOUN']
    # adjectives = [word.lexeme for word in line if word.lexeme and word.get_attr_value('pos') == 'ADJECTIVE']
    # ru_lines_annotated_with_pivots.append({'id': id, 'line': line, 'digits': digits,
    #                                        'verbs': verbs, 'nouns': nouns, 'ja_lines': {}})

    # ja_lines_annotated_with_pivots = []
    # with open("ja_adjectives.txt", 'w') as file:
    #     for id, line in enumerate(ja_lines):
    #         verbs = sum([annotate_russian_text(mystem, maru_analyzer, word.translation) for word in line if
    #                  word.attributes and word.translation and word.get_attr_value('pos') == 'Adjective'], [])
    #         verbs = [w.lexeme.lower() for w in verbs if w.lexeme and w.get_attr_value('pos') == 'ADJECTIVE']
    #         file.write(','.join(verbs) + '\n')
    # nouns = sum([annotate_russian_text(mystem, maru_analyzer, word.translation) for word in line if
    #              word.attributes and word.translation and word.get_attr_value('pos') == 'Noun'], [])
    # nouns = [w.lexeme.lower() for w in nouns if w.lexeme and w.get_attr_value('pos') == 'NOUN']
    # digits = [word.text for word in line if word.attributes and word.text.isnumeric()]
    # ja_lines_annotated_with_pivots.append({'id': id, 'line': line, 'digits': digits,
    #                                        'verbs': verbs, 'nouns': nouns, 'ru_lines': {}})

    # offset = ceil(len(ru_lines_annotated_with_pivots) / len(ja_lines_annotated_with_pivots)) + 1
    #
    # sent_scores_ru = {}
    #
    # ru_id = 0
    # for line in ru_lines_annotated_with_pivots:
    #     upper_offset = min(len(ja_lines_annotated_with_pivots), line['id'] + offset)
    #     for id in range(line['id'], upper_offset):
    #         for digit in line['digits']:
    #             if digit in ja_lines_annotated_with_pivots[id]['digits']:
    #                 line['ja_lines'][id] = 1
    #                 # ja_lines_annotated_with_pivots[id]['ru_lines'][line['id']] = 1
    #
    # pivots_digits = [(line['id'], list(line['ja_lines'].keys())) for line in ru_lines_annotated_with_pivots if
    #                  line['ja_lines']]
    #
    # if len(pivots_digits) > 1:
    #     for id, _ in enumerate(pivots_digits[:-1]):
    #         if len(pivots_digits[id][1]) == 1 and pivots_digits[id][0] == pivots_digits[id][1][0]:
    #             if len(pivots_digits[id + 1][1]) == 1 and pivots_digits[id + 1][0] == pivots_digits[id + 1][1][0]:
    #                 for iid in range(pivots_digits[id][0], pivots_digits[id + 1][0] + 1):
    #                     ru_lines_annotated_with_pivots[id]['ja_lines'][iid] = 1
    #                     ja_lines_annotated_with_pivots[id]['ru_lines'][iid] = 1
    #
    # unmatched_lines = [line['id'] for line in ru_lines_annotated_with_pivots if not line['ja_lines']]

    print(1)
    # for pivot_id, pivot_val in enumerate(pivot_indices_ru[:-1]):
    #     cur_offset = ru_id + offset
    #     if cur_offset >= pivot_indices_ru[pivot_id + 1]:
    #         cur_offset = pivot_indices_ru[pivot_id + 1]
    #     for cur_sentence in range(pivot_val, pivot_indices_ru[pivot_id + 1]):
    #         for i in range(cur_sentence, cur_sentence + cur_offset):
    #             verb_score = len(w for w in ru_lines_annotated_with_pivots[ru_id]['verbs'] if w in ja_lines_annotated_with_pivots[ja_id]['verbs'])
    #             noun_score = len(
    #                 w for w in ru_lines_annotated_with_pivots[ru_id]['nouns'] if w in ja_lines_annotated_with_pivots[ja_id]['nouns'])
    #             sent_scores_ru[ru_id][i] = {'v': verb_score, 'n': noun_score}
    #             if i > ru_id:
    #                 for ii in range(ru_id, i + 1):
    #                     sent_scores_ru[ru_id][i]['v'] = mean(sent_scores_ru[ru_id][i]['v'],
    #                                                          sent_scores_ru[ru_id][ii]['v'])
    #                     sent_scores_ru[ru_id][i]['n'] = mean(sent_scores_ru[ru_id][i]['v'],
    #                                                          sent_scores_ru[ru_id][ii]['v'])
    #         ru_id += 1
    return None
