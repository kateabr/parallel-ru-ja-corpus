import re
from typing import Optional

import requests as req
from bs4 import BeautifulSoup, Tag, NavigableString

from src.main.python.corpus_model import JapaneseToken


def scrap_translation(token: JapaneseToken, lexeme_reading: str, ref_value: str) -> (
        Optional[str], Optional[str]):
    def scrap_single_translation(dirty_translation, reading_id=0):
        clean = []

        if isinstance(dirty_translation, Tag) and (
                'class' in dirty_translation.attrs and dirty_translation.attrs['class'] and
                dirty_translation.attrs['class'][0] in ['ref', 'lref', 'grref']):
            return ''

        if reading_id:
            dirty_translation = dirty_translation[:reading_id]

        for item in dirty_translation:
            if isinstance(item, NavigableString):
                if str(item).strip() != '':
                    clean.append(str(item).strip())
            elif not ('class' in item.attrs and item.attrs['class'] and item.attrs['class'][0] in ['ref', 'lref',
                                                                                                   'grref']):
                if item.name == 'span':
                    clean.append(str(''.join([it for it in item.contents if isinstance(it, str)])).strip())
                else:
                    clean.append(str(item).strip())
        return ''.join(clean)

    def scrap_numbered_translations(dirty_translation):
        numbered = [str(id + 1) + ') ' + ''.join([scrap_single_translation(it) for it in item.parent.contents[1:]]) for
                    id, item in enumerate(dirty_translation.find_all('td', {'class': 'mmno'}))]
        if numbered:
            return '<br>'.join(numbered)
        return scrap_single_translation(dirty_translation)

    def translation_from_compounds(soup, reading):
        def remove_numeration_and_readings(translation_data, readings_available=True):
            bad_part = [i for i, it in enumerate(translation_data) if
                        isinstance(it, Tag) and 'class' in it.attrs and it['class'][0] in ['comment', 'gtatgrey']]
            if bad_part:
                translation_data.contents = translation_data.contents[:bad_part[0]]
            if readings_available:
                clean_translation = ' '.join([str(item).strip() for item in translation_data.contents if
                                              not (isinstance(item, Tag) and 'class' in item.attrs and item.attrs[
                                                  'class'][0] == 'grouptitlereading')])
            else:
                clean_translation = ' '.join([str(item).strip() for item in translation_data]).strip()
            clean_translation = re.sub(r'^(\d+)\)\s*', '', clean_translation)
            return clean_translation

        res = []
        tr_without_readings = []
        for group in soup.find_all('p', {'class': 'grouptitle'}):
            if group.find('span', {'class': 'grouptitlereading'}) is None:
                tr_without_readings.append(remove_numeration_and_readings(group, False))
            else:
                compound_readings = normalize_reading(group.find('span', {'class': 'grouptitlereading'}))
                if reading in compound_readings:
                    res.append(remove_numeration_and_readings(group))
        if not res:
            if len(tr_without_readings) > 1:
                return '<br>'.join([f'{id + 1}) {tr}' for id, tr in enumerate(tr_without_readings)])
            else:
                return '<br>'.join(tr_without_readings)
        if len(res) > 1:
            if tr_without_readings:
                res.extend(tr_without_readings)
            return '<br>'.join([f'{id + 1}) {tr}' for id, tr in enumerate(res)])
        else:
            return '<br>'.join(res)

    def normalize_reading(src_reading):
        if src_reading is None:
            return []
        reading = ''
        for id, symbol in enumerate(src_reading.text):
            if symbol == 'ō':
                reading += 'ou'
            elif symbol == 'ū':
                reading += 'uu'
            elif symbol == 'd' and src_reading.text[id + 1] == 'u':
                reading += 'z'
            elif symbol in ['-', '(', ')', ' ']:
                continue
            else:
                reading += symbol
        return re.findall(r'([a-z\'+]+)', reading)

    def homonymous_variants(dirty_translations):
        res = ['<i>перевод неоднозначен</i>']
        for dirty_translation in dirty_translations:
            word = dirty_translation.find('td').text
            translation = scrap_numbered_translations(dirty_translation.find_all('td')[2])
            if not re.search(r'^\d*\)', translation):
                delim = ' '
            else:
                delim = '<br>'
            res.append(
                f"{word}:{delim}{translation}")
        if len(res) == 1:
            return '<i>перевод затруднен: начальная форма отличается от приведенной в словаре</i>'
        return '<br><br>'.join(res)

    if token.has_attr('FamN'):
        return '<i>фамилия</i>', None
    if token.has_attr('PersN'):
        return '<i>имя</i>', None
    if token.has_attr('Human_name_or_family_name'):
        return '<i>имя или фамилия</i>', None

    if token.has_attr('pos', 'Particle') and token.get_attr_value('romaji_reading') != 'nado':
        return '<i>служебная частица</i>', None

    if token.has_attr('pos', 'Suffix') and token.has_attr('type', 'Verbal') and not lexeme_reading in ['iru', 'beki',
                                                                                                       'nai', 'kuru',
                                                                                                       'iku',
                                                                                                       'kudasaru',
                                                                                                       'kureru']:
        return '<i>глагольный суффикс</i>', None

    if token.has_attr('pos', 'Suffix') and token.has_attr('type', 'Nominal') and token.has_attr('Predicative'):
        return '<i>предикативный именной суффикс</i>', None

    if token.has_attr('pos', 'Judgemental'):
        if token.has_attr('form2', 'Conditional'):
            return '<i>предикатив условия</i>', None
        elif token.has_attr('form2', 'Assumptional'):
            return '<i>предикатив предположения</i>', None
        elif token.has_attr('form2', 'Conjunctive'):
            return '<i>предикатив перечисления</i>', None
        else:
            return '<i>предикатив</i>', None

    if token.has_attr('type', 'Expletive'):
        return '<i>эксплетив</i>', None

    if token.get_attr_value('romaji_reading') == 'dono' and token.has_attr('pos', 'Demonstrative'):
        return 'какой <i>из</i>, как', None

    if token.has_attr('unrecognized_symbols'):
        return '<i>перевод отсутствует</i>', None

    reading = None

    if token.has_attr('Abbr'):
        reading = 'On'

    resp = req.post("http://yarxi.ru/search.php",
                    data={'K': '', 'R': ref_value, 'M': '', 'S': '', 'D': '0', 'NS': '0', 'F': '0'})
    soup = BeautifulSoup(resp.text, 'html.parser')
    mode = resp.text[1]

    if mode == 'S':
        resp = req.post("http://yarxi.ru/tsearch.php",
                        data={'R': ref_value, 'M': '', 'Src': 'bytext'})
        soup = BeautifulSoup(resp.text, 'html.parser')
        mode = resp.text[1]

    if mode == 'S' and ref_value == token.lexeme or token.text in ['ソ連']:
        if token.text == token.lexeme:
            ref_value = lexeme_reading
        else:
            ref_value = token.text
        resp = req.post("http://yarxi.ru/tsearch.php",
                        data={'R': ref_value, 'M': '', 'Src': 'bytext'})
        soup = BeautifulSoup(resp.text, 'html.parser')
        mode = resp.text[1]

    if mode == 'S':
        return '<i>перевод отсутствует</i>', None

    if mode == 'T':
        tables = soup.find_all('table', class_='comp')
        matching_readings = [tb_pair[1] for tb_pair in
                             [(normalize_reading(table.find('td', {'class': 'ttrans'})), table) for table in tables]
                             if
                             token.get_attr_value('romaji_reading') in tb_pair[0] or lexeme_reading in tb_pair[0]]
        if not matching_readings:
            matching_readings = [tb_pair[1] for tb_pair in
                                 [(normalize_reading(table.find('td', {'class': 'ttrans'})), table) for table in
                                  tables]
                                 if ref_value ==
                                 tb_pair[1].find('td', {
                                     'class': 'tjtext'}).text]
        special_suff = {'iru': 0, 'beki': 0, 'kureru': 0, 'nai': 1, 'kuru': 1, 'iku': 1}
        if len(matching_readings) == 1:
            return scrap_numbered_translations(matching_readings[0].find_all('td')[2]), reading
        elif lexeme_reading in special_suff.keys():
            return scrap_numbered_translations(
                matching_readings[special_suff[lexeme_reading]].find_all('td')[2]), reading
        else:
            matching_lexemes = [rec for rec in matching_readings if
                                rec.find('td', {'class': 'tjtext'}).text == ref_value \
                                or rec.find('td', {'class': 'tjtext'}).text == token.text]
            if len(matching_lexemes) == 1:
                return scrap_numbered_translations(matching_lexemes[0].find_all('td')[2]), reading
            # elif matching_lexemes:
            #     return homonymous_variants(matching_lexemes), reading
            elif matching_readings:
                return homonymous_variants(matching_readings), reading
            else:
                return '<i>перевод отсутствует</i>', None

    elif mode == 'E':
        nick = f"<b>{'/'.join([n.text for n in soup.find('td', {'id': 'nick'}).find_all('span')])}</b><br><br>"
        if token.has_attr('pos', 'Suffix') or token.has_attr('pos', 'Prefix'):
            return nick + translation_from_compounds(soup, token.get_attr_value('romaji_reading')), None
        tables = soup.find_all('table', class_='kun')
        for table in tables:
            if token.has_attr('pos', 'Suffix') or token.has_attr('Ender'):
                return nick + translation_from_compounds(soup, token.get_attr_value('romaji_reading')), None
            kun_reading = normalize_reading(table.find('span', {'class': 'kunreading'}))
            on_reading = normalize_reading(table.find('span', {'class': 'kunreading_ch'}))
            if token.get_attr_value(
                    'romaji_reading') in kun_reading or lexeme_reading in kun_reading or lexeme_reading in kun_reading:
                return nick + scrap_numbered_translations(table.find('td', {'class': 'kuntrans'})), 'Kun'
            elif token.get_attr_value('romaji_reading') in on_reading:
                return nick + scrap_numbered_translations(table.find('td', {'class': 'kuntrans'})), 'On'
        return nick + translation_from_compounds(soup, token.get_attr_value('romaji_reading')), None
    if token.has_attr('pos', 'Suffix'):
        return '<i>суффикс</i>', None
    if token.has_attr('type', 'Toponym'):
        return '<i>топоним</i>', None
    if token.has_attr('pos', 'Suffix') and token.has_attr('type', 'Nominal'):
        return '<i>именной суффикс</i>', None
    return '<i>перевод отсутствует</i>', None
