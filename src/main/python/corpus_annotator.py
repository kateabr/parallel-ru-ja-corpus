import string
import unicodedata

from maru.analyzer import Analyzer
from pykakasi import kakasi
from pyknp import KNP, BList, Morpheme
from pymystem3 import Mystem

from src.main.python.corpus_annotation_mappers import *
from src.main.python.corpus_model import *
from src.main.python.japanese_translator import scrap_translation
from src.main.python.numbers_to_japanese import convert_to_japanese, kanjiConvert


def annotate_russian_text(mystem: Mystem, maru_analyzer: Analyzer, text: str) -> List[RussianToken]:
    if text == '': return list()

    mystem_info = mystem.analyze(text)

    # mystem wrapper returns '\n' as the last element
    # sometimes it'a separate token, sometimes it's appended
    # to last entry
    last_token = mystem_info[-1]['text'].strip()
    if last_token == "":
        mystem_info = mystem_info[0:-1]
    else:
        mystem_info[-1]['text'] = last_token

    maru_info = list(maru_analyzer.analyze(
        [it for it in [it['text'] for it in mystem_info if 'analysis' in it.keys()]])
    )

    idx = 0
    result: List[RussianToken] = []
    for pos, item in enumerate(mystem_info, 1):
        if 'analysis' in item.keys():
            info = maru_info[idx]
            maru_tags = [Attribute(str(name), value.name) for (name, value)
                         in info.tag._asdict().items() if value is not None]
            if item['analysis']:
                analysis = item['analysis'][0]
                lexeme = analysis['lex']

                mystem_tags = analysis['gr'].split(',')
                mystem_extra_tags = [tag for tag in
                                     map(lambda x: mystem_extra_tags_mapper.get(x, None), mystem_tags)
                                     if tag is not None]
                score = analysis['wt']
            else:
                lexeme = None
                mystem_extra_tags = None
                score = 0

            token = RussianToken(pos, info.word, lexeme, maru_tags, mystem_extra_tags, score)
            result.append(token)
            idx = idx + 1
        else:
            result.append(RussianToken(pos, item['text']))

    return result


def annotate_japanese_text(knp: KNP, kakasi_converter: kakasi, text: str) -> List[JapaneseToken]:
    def lexeme_with_reading(nf_str):
        split_str = nf_str.split('/')
        split_str.append(None)
        return split_str[0:2]

    blist: BList = knp.parse(text)

    result: List[JapaneseToken] = []
    item: Morpheme
    for pos, item in enumerate(blist.mrph_list(), 1):
        text_src = item.midasi

        text = item.midasi

        hinsi = juman_hinsi_mapper[item.hinsi]
        if hinsi[0] == "Special" or item.midasi in ['～', '・'] or item.midasi in string.punctuation:
            result.append(JapaneseToken(pos, text))
            continue

        try:
            if unicodedata.normalize('NFKC', item.midasi).isnumeric():
                text, reading = convert_to_japanese(unicodedata.normalize('NFKC', item.midasi))
                item = knp.parse(text).mrph_list()[0]
                item.midasi = unicodedata.normalize('NFKC', text_src)
                item.yomi = reading
        except:
            pass

        tags: List[Attribute] = []
        extra_tags: List[str] = []
        unsorted = []

        bunrui = juman_bunrui_mapper[item.bunrui]
        if bunrui:
            if bunrui[0] == 'Numeral' or unicodedata.normalize('NFKC', text_src).isnumeric():
                tags.append(Attribute('pos', 'Numeral'))
            else:
                tags.append(Attribute('type', bunrui[0]))
        if not [tag.value for tag in tags if tag.name == 'pos']:
            tags.append(Attribute('pos', hinsi[0]))
        extra_tags.extend(hinsi[1:])
        extra_tags.extend(bunrui[1:])

        extra_tags.extend(juman_katuyou1_mapper[item.katuyou1])
        extra_tags.extend(juman_katuyou2_mapper(item.katuyou2))
        extra_tags = list(set(extra_tags))

        row = [(i, item) for i, item in enumerate(extra_tags) if item.endswith('_row')]
        if row:
            tags.append(Attribute('row', extra_tags[row[0][0]].split('_')[0]))
            extra_tags.remove(row[0][1])

        if hinsi[0] == 'Adjective' or (
                hinsi[0] in ['Suffix', 'Prefix'] and bunrui and bunrui[0] == 'Adjectival'):
            type = [(i, item) for i, item in enumerate(extra_tags) if item.endswith('_adjective')]
            if type:
                if hinsi[0] == 'Adjective':
                    tags.append(Attribute('type', extra_tags[type[0][0]].split('_')[0]))
                else:
                    tags.append(Attribute('adj_type', extra_tags[type[0][0]].split('_')[0]))
                extra_tags.remove(type[0][1])

        if hinsi[0] == 'Verb' or (hinsi[0] == 'Suffix' and bunrui and bunrui[0] == 'Verbal'):
            stem_type = [(i, item) for i, item in enumerate(extra_tags) if item.endswith('_stem')]
            if stem_type:
                tags.append(Attribute('stem_type', extra_tags[stem_type[0][0]].split('_')[0]))
                extra_tags.remove(stem_type[0][1])

        if hinsi[0] in ['Verb', 'Judgemental', 'Adjective', 'Suffix']:
            form = [(i, item) for i, item in enumerate(extra_tags) if item.endswith('_form')]
            if form:
                tags.append(Attribute('form', extra_tags[form[0][0]].split('_')[0]))
                extra_tags.remove(form[0][1])
            form1 = [(i, item) for i, item in enumerate(extra_tags) if item.endswith('_form1')]
            if form1:
                tags.append(Attribute('form1', extra_tags[form1[0][0]].split('_')[0]))
                extra_tags.remove(form1[0][1])
            form2 = [(i, item) for i, item in enumerate(extra_tags) if item.endswith('_form2')]
            if form2:
                tags.append(Attribute('form2', extra_tags[form2[0][0]].split('_')[0]))
                extra_tags.remove(form2[0][1])
            type = [(i, item) for i, item in enumerate(extra_tags) if item.endswith('_type')]
            if type:
                tags.append(Attribute('type', extra_tags[type[0][0]].split('_')[0]))
                extra_tags.remove(type[0][1])

        lexeme_reading = ''

        lexeme = item.genkei
        reading = kakasi_converter.do(item.yomi)
        if len(item.repname.split('/')) > 1 and item.repname.split('/')[1][-1] != 'a':
            lexeme, lexeme_reading = lexeme_with_reading(item.repname)
        elif 'ひらがな' in item.fstring:
            lexeme_reading = item.genkei

        score = None

        if item.imis != 'NIL':
            split_sem_info = [it.split(':') for it in item.imis.split()]
            for sem_it in split_sem_info:
                if sem_it[0] not in juman_semantic_info_mapper.keys():
                    unsorted.append(':'.join(sem_it))
                elif juman_semantic_info_mapper[sem_it[0]] == 'writing_representation':
                    lexeme, lexeme_reading = lexeme_with_reading(sem_it[1])
                elif juman_semantic_info_mapper[sem_it[0]] == 'category':
                    tags.append(Attribute('category', [juman_category_mapper[c] for c in sem_it[1].split(';')]))
                elif juman_semantic_info_mapper[sem_it[0]] == 'domain':
                    tags.append(Attribute('domain', [juman_domain_mapper[d] for d in sem_it[1].split(';')]))
                elif juman_semantic_info_mapper[sem_it[0]] == 'Toponym':
                    for id, geo_it in enumerate(sem_it):
                        if not geo_it in juman_semantic_info_mapper.keys():
                            unsorted.append(geo_it)
                        elif juman_semantic_info_mapper[geo_it] == 'Abbr':
                            extra_tags.append('Abbr')
                            lexeme = sem_it[id + 1]
                            break
                elif juman_semantic_info_mapper[sem_it[0]] == 'transitivity':
                    if juman_semantic_info_mapper[sem_it[1]] == 'Transitive':
                        # sem_it[1] can also be equal to '同形',
                        # apparently meaning that transitive and intransitive forms are the same
                        # since knp provides no information on whether the verb in question
                        # is transitive or intransitive, the 'Transitivity' field is left out
                        tags.append(Attribute('transitivity', "Intransitive"))
                    elif juman_semantic_info_mapper[sem_it[1]] == "Intransitive":
                        tags.append(Attribute('transitivity', "Transitive"))
                        tags.append(Attribute('intransitive_form', sem_it[2].split('/')[0]))
                elif juman_semantic_info_mapper[sem_it[0]][0] == 'Derivation':
                    extra_tags.append('Derivative')
                    tags.append(Attribute('derivation_type', juman_semantic_info_mapper[sem_it[0]][1]))
                    tags.append(Attribute('derivation_source', sem_it[1].split('/')[0]))
                elif juman_semantic_info_mapper[sem_it[0]] == 'Potential':
                    extra_tags.append('Potential')
                    tags.append(Attribute('non_potential_form', sem_it[1].split('/')[0]))
                elif juman_semantic_info_mapper[sem_it[0]] == 'Causative':
                    extra_tags.append('Causative')
                    tags.append(Attribute('non_causative_form', sem_it[1].split('/')[0]))
                elif juman_semantic_info_mapper[sem_it[0]][0] == 'Attached_verb':
                    extra_tags.append('Attached_verb')
                    tags.append(Attribute('attachment_form', juman_semantic_info_mapper[sem_it[0]][1]))
                elif juman_semantic_info_mapper[sem_it[0]] == 'Short_form':
                    lexeme, lexeme_reading = lexeme_with_reading(sem_it[1])
                elif juman_semantic_info_mapper[sem_it[0]] == 'Human_name_or_family_name':
                    if not sem_it[0].startswith('Wikipedia'):
                        if juman_semantic_info_mapper[sem_it[1]] == "japanese":
                            extra_tags.append(juman_semantic_info_mapper[sem_it[2]])
                            score = float(sem_it[4])
                        else:
                            extra_tags.append(juman_semantic_info_mapper[sem_it[0]])
                            extra_tags.append(juman_semantic_info_mapper[sem_it[1]])
                            score = 0
                    else:
                        extra_tags.append(juman_semantic_info_mapper[sem_it[0]])
                elif juman_semantic_info_mapper[sem_it[0]][0] == 'Ender':
                    extra_tags.extend(juman_semantic_info_mapper[sem_it[0]])
                elif juman_semantic_info_mapper[sem_it[0]][0] == 'reading_type':
                    tags.append(Attribute('reading_type', juman_semantic_info_mapper[sem_it[0]][1]))
                else:
                    if isinstance(sem_it, List):
                        for it in sem_it:
                            if it in juman_semantic_info_mapper.keys():
                                extra_tags.append(juman_semantic_info_mapper[it])
                            else:
                                unsorted.append(it)
                    elif sem_it[0] != 'Wikipedia':
                        extra_tags.append(juman_semantic_info_mapper[sem_it])
        if 'unrecognized_symbols' in extra_tags:
            if not 'Digits' in extra_tags:
                lexeme = None
            if "Katakana" not in extra_tags and 'Digits' not in extra_tags and not text.isalpha():
                reading = None
        if [tag.value for tag in tags if tag.name == 'pos'][0] == 'Human_name':
            if 'Human_name_or_family_name' in extra_tags:
                extra_tags.remove('Human_name_or_family_name')

        if [tag.value for tag in tags if tag.name == 'pos'][0] == 'Suffix' and \
                [tag.value for tag in tags if tag.name == 'type'][0] == 'Verbal':
            if kakasi_converter.do(lexeme_reading) == 'nai':
                extra_tags.append('Negative')
            elif kakasi_converter.do(lexeme_reading) in ['seru', 'saseru']:
                extra_tags.append('Causative')
            elif kakasi_converter.do(lexeme_reading) == 'iru':
                extra_tags.append('Progressive')
            elif kakasi_converter.do(lexeme_reading) in ['reru', 'rareru']:
                extra_tags.append('Passive')

        if reading is not None:
            tags.append(Attribute('romaji_reading', reading))
            hiragana_reading = item.yomi
        else:
            hiragana_reading = None
        new_token = JapaneseToken(pos, text, lexeme, hiragana_reading, None, tags, extra_tags,
                                  score, unsorted)

        ref_value = new_token.lexeme
        if (new_token.has_attr('type', 'Na') or new_token.has_attr('type', 'NaNo')
            or new_token.has_attr('adj_type', 'Na') or new_token.has_attr('adj_type', 'NaNo')) and \
                item.genkei[-1] == 'だ':
            if item.yomi[:-1] == item.genkei[:-1]:
                lexeme_reading = item.genkei
            lexeme_reading = lexeme_reading[:-1]
            if ref_value[-1] == 'だ':
                ref_value = ref_value[:-1]

        if new_token.has_attr('pos', 'Numeral'):
            if unicodedata.normalize('NFKC', text_src).isnumeric():
                translation = None
                new_token.text = unicodedata.normalize('NFKC', text_src)
            else:
                translation = kanjiConvert(text)
            if new_token.has_attr('suspected_writing_representation'):
                new_token.extra_attributes.remove('suspected_writing_representation')
            reading_type = None
        else:
            translation, reading_type = scrap_translation(new_token, kakasi_converter.do(lexeme_reading), ref_value)
        if translation is not None:
            new_token.translation = translation
            if reading_type is not None:
                new_token.attributes.append(Attribute('reading_type', reading_type))
        result.append(new_token)

        # if unsorted:
        #    print(new_token)
        print(f'{pos}/{len(blist.mrph_list()) + 1}', new_token)

    return result


def annotate_text(
        mystem: Mystem,
        maru_analyzer: Analyzer,
        knp: KNP,
        kakasi_converter: kakasi,

        entry_id: str,

        russian_text: List[str],
        japanese_text: List[str],

        russian_title: Optional[str] = None,
        japanese_title: Optional[str] = None,

        russian_url: Optional[str] = None,
        japanese_url: Optional[str] = None
) -> Entry:
    if mystem is None or maru_analyzer is None or knp is None or kakasi_converter is None:
        raise ValueError("External utilities are not initialized")
    if len(russian_text) != len(japanese_text):
        raise ValueError("text length doesn't match")
    if len(russian_text) == 0:
        raise ValueError("No sentences provided")

    russian = [(sentence, annotate_russian_text(mystem, maru_analyzer, sentence)) for sentence in russian_text]
    japanese = [(sentence, annotate_japanese_text(knp, kakasi_converter, sentence)) for sentence in japanese_text]
    sentence_pairs = [SentencePair(i, ru_src, ja_src, ru, ja)
                      for (i, ((ru_src, ru), (ja_src, ja))) in enumerate(zip(russian, japanese), 1)]

    return Entry(
        entry_id,
        sentence_pairs,
        Title(russian_title, japanese_title),
        russian_url,
        japanese_url
    )
