# https://yandex.ru/dev/mystem/doc/grammemes-values-docpage/
mystem_extra_tags_mapper = {
    'parenth': 'Parenth',
    'geo': 'Toponym',
    # 'awkw': 'ignored',
    'persn': 'PersN',
    # 'dist': 'ignored',
    # 'mf': 'ignored',
    # 'obsc': 'ignored',
    'patrn': 'PatrN',
    'praed': 'Praed',
    'inform': 'Informal',
    # 'rare': 'ignored',
    'abbr': 'Abbr',
    'obsol': 'Obsolete',
    'famn': 'FamN',
}

# https://hayashibe.jp/tr/juman/dictionary/ctype
juman_hinsi_mapper = {
    '動詞': ['Verb'],
    '名詞': ['Noun'],
    '形容詞': ['Adjective'],
    '判定詞': ['Judgemental'],
    '助動詞': ['Verb', 'Auxiliary_type'],
    '接尾辞': ['Suffix'],
    '形容詞性名詞接尾辞': ['Suffix', 'Nominal', 'Adjectival'],
    '形容詞性述語接尾辞': ['Suffix', 'Predicative', 'Adjectival'],
    '動詞性接尾辞': ['Suffix', 'Verbal'],
    '特殊': ['Special'],
    '助詞': ['Particle'],
    '接頭辞': ['Prefix'],
    '指示詞': ['Demonstrative'],
    '副詞': ['Adverb'],
    '接続詞': ['Conjunction'],
    '連体詞': ['Adjective', 'Adnominal'],
    '感動詞': ['Interjection'],
}

# https://hayashibe.jp/tr/juman/dictionary/pos
juman_bunrui_mapper = {
    # nouns
    '普通名詞': ['Common'],
    'サ変名詞': ['Suru'],
    '固有名詞': ['Proper'],
    '地名': ['Toponym'],
    '人名': ['Human_name'],
    '組織名': ['Organization_name'],
    '数詞': ['Numeral'],
    '形式名詞': ['Expletive'],
    '副詞的名詞': ['Adverbial'],
    '時相名詞': ['Temporal'],
    # demonstratives
    '名詞形態指示詞': ['Nominal'],
    '連体詞形態指示詞': ['Adnominal', 'Adjectival'],
    '副詞形態指示詞': ['Adverbial'],
    # verbs -
    # adjectives -
    # judgementals -
    # auxiliary verbs -
    # adverbs -
    # particles
    '格助詞': ['Case_marking'],
    '副助詞': ['Adverbial'],
    '接続助詞': ['Conjunctive'],
    '終助詞': ['Sentence_ending'],
    # prefices
    '名詞接頭辞': ['Nominal'],
    '動詞接頭辞': ['Verbal'],
    'イ形容詞接頭辞': ['I_adjective'],
    'ナ形容詞接頭辞': ['Na_adjective'],
    # suffices
    '名詞性述語接尾辞': ['Nominal', 'Predicative'],
    '名詞性名詞接尾辞': ['Nominal'],
    '名詞性名詞助数辞': ['Nominal', 'Counting'],
    '名詞性特殊接尾辞': ['Nominal', 'Special'],
    '形容詞性述語接尾辞': ['Adjectival', 'Predicative'],
    '形容詞性名詞接尾辞': ['Adjectival', 'Nominal'],
    '動詞性接尾辞': ['Verbal'],
    # special -
    # unsupported
    # 'カタカナ': ['Katakana'],
    # 'アルファベット': ['Alpha'],
    # '数字': ['Digits'],
    # 'その他': ['Unknown_symbols'],
    # empty
    '*': []
}

# https://hayashibe.jp/tr/juman/dictionary/ctype
juman_katuyou1_mapper = {
    # verbs
    '母音動詞': ['Vowel_stem'],
    '子音動詞カ行': ['Consonant_stem', 'Ka_row'],
    '子音動詞カ行促音便形': ['Consonant_stem', 'Ka_row', 'Nasalization_change'],
    '子音動詞ガ行': ['Consonant_stem', 'Ga_row'],
    '子音動詞サ行': ['Consonant_stem', 'Sa_row'],
    '子音動詞タ行': ['Consonant_stem', 'Ta_row'],
    '子音動詞ナ行': ['Consonant_stem', 'Na_row'],
    '子音動詞バ行': ['Consonant_stem', 'Ba_row'],
    '子音動詞マ行': ['Consonant_stem', 'Ma_row'],
    '子音動詞ラ行': ['Consonant_stem', 'Ra_row'],
    '子音動詞ラ行イ形': ['Consonant_stem', 'Ra_row', 'I_form'],
    '子音動詞ワ行': ['Consonant_stem', 'Wa_row'],
    '子音動詞ワ行文語音便形': ['Consonant_stem', 'Wa_row', 'Written_form', 'Euphonic_change'],
    'カ変動詞': ['Irregular'],
    'カ変動詞来': ['Irregular', 'Kanji'],
    'サ変動詞': ['Suru_type'],
    'ザ変動詞': ['Zuru_type'],
    '動詞性接尾辞ます型': ['Masu'],
    # adjectives
    'イ形容詞アウオ段': ['I_adjective', 'AUO_row'],
    'イ形容詞イ段': ['I_adjective', 'I_row'],
    'イ形容詞イ段特殊': ['I_adjective', 'I_row', 'Special'],
    'ナ形容詞': ['Na_adjective'],
    'ナ形容詞特殊': ['Na_adjective', 'Special'],
    'ナノ形容詞': ['NaNo_adjective'],
    'タル形容詞': ['Taru_adjective'],
    # judgementals -
    # auxiliary verbs - (duplicates omitted)
    '判定詞': ['Judgemental'],
    '無活用型': ['Non_conjugating'],
    '助動詞ぬ型': ['Nu', 'Negation'],
    '助動詞だろう型': ['Darou'],
    '助動詞そうだ型': ['Souda'],
    '助動詞く型': ['Ku'],
    # suffices (duplicates omitted)
    '動詞性接尾辞うる型': ['Uru'],
    # empty
    '*': []
}

# http://nlp.ist.i.kyoto-u.ac.jp/index.php?plugin=attach&refer=KNP&openfile=knp_feature.pdf
juman_category_mapper = {
    '組織・団体': 'Organisations and associations',
    '動物': 'Animals',
    '植物': 'Plants',
    '動物-部位': 'Animals-Parts',
    '植物-部位': 'Plants-Parts',
    '人工物-食べ物': 'Crafted-Food',
    '人工物-衣類': 'Crafted-Clothes',
    '人工物-乗り物': 'Crafted-Vehicles',
    '人工物-金銭': 'Crafted-Money',
    '人工物-その他': 'Crafted-Other',
    '自然物': 'Nature',
    '場所-施設': 'Places-Facilities',
    '場所-施設部位': 'Places-Facilities-Parts',
    '場所-自然': 'Places-Nature',
    '場所-機能': 'Places-Functional',
    '場所-その他': 'Places-Other',
    '抽象物': 'Abstract',
    '現象-自然': 'Phenomena-Nature',
    '現象-生命': 'Phenomena-Life',
    '動作': 'Actions',
    '出来事': 'Incidents',
    '様子': 'States',
    '気持ち': 'Feelings',
    '制度・規則': 'Systems and rules',
    '知的生産物': 'Intellectual products',
    '力': 'Power',
    '抽象-機能': 'Abstract-Functional',
    '抽象-その他': 'Abstract-Other',
    '形・模様': 'Shapes and figures',
    '色': 'Colors',
    '数量': 'Quantity',
    '時間': 'Time',
    '人': 'People'
}

juman_domain_mapper = {
    '文化・芸術': 'Culture and fine arts',
    'レクリエーション': 'Recreation',
    'スポーツ': 'Sports',
    '健康・医学': 'Health and medicine',
    '家庭・暮らし': 'Home and family life',
    '料理・食事': 'Food and cooking',
    '交通': 'Transportation',
    '教育・学習': 'Education and learning',
    '科学・技術': 'Science and art',
    'ビジネス': 'Business',
    'メディア': 'Media',
    '政治': 'Politics',
    '無し': 'Unspecified',
}

# http://nlp.ist.i.kyoto-u.ac.jp/index.php?plugin=attach&refer=KNP&openfile=knp_feature.pdf
juman_semantic_info_mapper = {
    'カテゴリ': 'category',
    'ドメイン': 'domain',
    'Wikipedia姓': 'FamN',
    '姓': 'FamN',
    'Wikipedia名': 'PersN',
    '名': 'PersN',
    '人名': 'Human_name_or_family_name',
    'Wikipedia人名': 'Human_name_or_family_name',
    '日本': 'japanese',
    '外国': 'foreign',
    '略称': 'Abbr',
    '旧称': 'Former_name',
    '地名': 'Toponym',
    '読み不明': 'unknown_reading',
    '自動獲得': 'acquired_automatically',
    '自他動詞': 'transitivity',
    '自': 'Intransitive',
    '他': 'Transitive',
    '同形': 'Both',
    '可能動詞': 'Potential',
    '住所末尾': ['Ender', 'Address'],  # for addresses
    '地名末尾': ['Ender', 'Toponym'],  # for toponyms; coming in the end
    '地名末尾外': ['Ender', 'Toponym', 'Post'],  # for toponyms; coming after the end
    '組織名末尾': ['Ender', 'Organisation'],  # for organization names
    '人名末尾': ['Ender', 'Human_name'],  # for human names
    '人名末尾外': ['Ender', 'Human_name', 'Post'],  # for human names; after
    '国': 'Country',
    '未知語': 'unrecognized_symbols',
    'カタカナ': 'Katakana',
    'ひらがな': 'Hiragana',
    'ローマ字': 'Latin_letters',
    '数字': 'Digits',
    '漢字': 'Kanji',
    '擬音語擬態語': 'Onomatopoeia',
    'その他': 'Unknown_symbols',
    '準内容語': 'Associated_content_word',
    '内容語': 'Content_word',
    '補文ト': 'To_supplement',
    '付属動詞候補（基本）': ['Attached_verb', 'Basic'],
    '付属動詞候補（タ系）': ['Attached_verb', 'Ta_system'],
    '使役動詞': 'Causative',
    '省略': 'Short_form',
    '連語': 'Compound_word',
    '連語由来': 'Historical_compound_word',
    '弱時相名詞': 'Weak_temporal_noun',  # ??
    '用言弱修飾': 'Weak_declinable_modifier',  # ??
    '数量修飾': 'Quantity_modifier',
    '修飾（ニ格）': 'Ni_case_modifier',
    '修飾（デ格）': 'De_case_modifier',
    '修飾（ト格）': 'To_case_modifier',
    # '換言': 'Paraphrase', # not needed since there is translation
    '動詞派生': ['Derivation', 'Verbal'],
    '形容詞派生': ['Derivation', 'Adjectival'],
    '名詞派生': ['Derivation', 'Nominal'],
    '相対名詞': 'Relativity_noun',
    '相対名詞修飾': 'Relativity_modifier',
    '否定': 'Negation',
    '漢字読み': 'reading_type',
    '音': 'On',
    '訓': 'Kun'
}


# https://hayashibe.jp/tr/juman/dictionary/cform
def juman_katuyou2_mapper(katuyou2):
    res = []
    if katuyou2.find('タ形') != -1:
        res.append('Ta_form1')
    if katuyou2.find('タ系') != -1:
        res.append('Ta_system')
    if katuyou2.find('推量') != -1:
        res.append('Assumptional_form2')
    if katuyou2.find('条件') != -1:
        res.append('Conditional_form2')
    if katuyou2.find('省略') != -1:
        res.append('Short_form')
    if katuyou2.find('連用') != -1:
        res.append('Conjunctive_form2')
    if katuyou2.find('テ形') != -1:
        res.append('Te_form1')
    if katuyou2.find('ダ列') != -1:
        res.append('Da_row')
    if katuyou2.find('基本') != -1:
        res.append('Basic_form1')
    if katuyou2.find('デアル列') != -1:
        res.append('Dearu_row')
    if katuyou2.find('デス列') != -1:
        res.append('Desu_row')
    if katuyou2.find('音便') != -1:
        res.append('Euphonic_change')
    if katuyou2.find('ヤ列') != -1:
        res.append('Ya_row')
    if katuyou2.find('文語') != -1:
        res.append('Written_form')
    if katuyou2.find('連体') != -1:
        res.extend(['Adnominal', 'Adjectival'])
    if katuyou2.find('語幹') != -1:
        res.append('Stem')
    if katuyou2.find('エ基本') != -1:
        res.append('E_basic_form1')
    if katuyou2.find('タリ形') != -1:
        res.append('Tari_form')
    if katuyou2.find('チャ形') != -1:
        res.append('Cha_form')
    if katuyou2.find('チャ形２') != -1:
        res.extend(['Cha_form', 'Consonant_reduplication'])
    if katuyou2.find('命令') != -1:
        res.append('Imperative_form2')
    if katuyou2.find('未然') != -1:
        res.append('Imperfective_form1')
    if katuyou2.find('ジャ形') != -1:
        res.append('Ja_form')
    if katuyou2.find('特殊') != -1:
        res.append('Special')
    if katuyou2.find('意志') != -1:
        res.append('Volitional_form2')

    return res

juman_representation_mapper = {
    '正規化代表表記': 'normal_writing_representation',
    '代表表記': 'writing_representation',
    '疑似代表表記': 'suspected_writing_representation'
}