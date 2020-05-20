from pathlib import Path
from typing import List, Optional

import bs4
from bs4 import Tag
from dataclasses import dataclass

import src.main.python.corpus_xml as xml


@dataclass
class Attribute:
    name: str
    value: str

    def to_xml(self) -> xml.attribute:
        return xml.attribute(self.name, self.value)


@dataclass
class JapaneseToken:
    id: int
    text: str

    lexeme: Optional[str] = None
    reading: Optional[str] = None
    translation: Optional[str] = None

    attributes: Optional[List[Attribute]] = None
    extra_attributes: Optional[List[str]] = None

    # non-serializable
    reliability_score: Optional[float] = None
    unsorted_attributes: List = None

    def to_xml(self) -> xml.japaneseToken:
        return xml.japaneseToken(
            self.id,
            self.text,
            self.lexeme if self.lexeme is not None else None,
            self.reading if self.reading is not None else None,
            self.translation if self.translation is not None else None,
            xml.attributes([a.to_xml() for a in self.attributes]) if self.attributes is not None else None,
            xml.extraAttributes([xml.extraAttribute(exa) for exa in self.extra_attributes])
            if self.extra_attributes is not None else None
        )

    def has_attr(self, attr_name, attr_value=None):
        if attr_value is None:
            return attr_name in self.extra_attributes
        find_attr = [attr.value for attr in self.attributes if attr.name == attr_name]
        if find_attr:
            return attr_value in find_attr
        return False

    def get_attr_value(self, attr_name):
        search_res = [attr.value for attr in self.attributes if attr.name == attr_name]
        if search_res:
            return search_res[0]
        return None


@dataclass
class RussianToken:
    id: int
    text: str

    lexeme: Optional[str] = None

    attributes: Optional[List[Attribute]] = None
    extra_attributes: Optional[List[str]] = None

    # non-serializable
    reliability_score: Optional[float] = None

    def to_xml(self) -> xml.russianToken:
        return xml.russianToken(
            self.id,
            self.text,
            self.lexeme if self.lexeme is not None else None,
            xml.attributes([a.to_xml() for a in self.attributes]) if self.attributes is not None else None,
            xml.extraAttributes([xml.extraAttribute(exa) for exa in self.extra_attributes])
            if self.extra_attributes is not None else None
        )

    def has_attr(self, attr_name, attr_value=None):
        if attr_value is None:
            return attr_name in self.extra_attributes
        find_attr = [attr.value for attr in self.attributes if attr.name == attr_name]
        if find_attr:
            return find_attr[0] == attr_value
        return False

    def get_attr_value(self, attr_name):
        search_res = [attr.value for attr in self.attributes if attr.name == attr_name]
        if search_res:
            return search_res[0]
        return None


@dataclass
class SentencePair:
    id: int
    russian_source: str
    japanese_source: str
    russian: List[RussianToken]
    japanese: List[JapaneseToken]

    def to_xml(self) -> xml.sentencePair:
        return xml.sentencePair(
            self.id,
            xml.russianSentence(self.russian_source, xml.russianTokens([w.to_xml() for w in self.russian])),
            xml.japaneseSentence(self.japanese_source, xml.japaneseTokens([w.to_xml() for w in self.japanese]))
        )


@dataclass
class Title:
    russian: Optional[str]
    japanese: Optional[str]

    def to_xml(self) -> xml.entryTitle:
        return xml.entryTitle(self.russian, self.japanese)


@dataclass
class Entry:
    id: str
    sentence_pairs: List[SentencePair]
    title: Optional[Title] = None
    russian_link: Optional[str] = None
    japanese_link: Optional[str] = None

    def to_xml(self) -> xml.entry:
        return xml.entry(
            self.id if self.id is not None else None,
            xml.entryUrl(self.russian_link, self.japanese_link)
            if self.russian_link is not None or self.japanese_link is not None else None,
            self.title.to_xml() if self.title is not None else None,
            xml.sentencePairs([p.to_xml() for p in self.sentence_pairs])
        )

    @staticmethod
    def from_xml(file: Path):
        with open(file, 'r', encoding='utf-8') as f:
            xml = bs4.BeautifulSoup(f.read(), features="lxml")

            id = xml.entry.id.text
            sps_xml: Tag = xml.entry.sentencepairs
            sps = [SentencePair(sp.id, sp.russian.sentence.text, sp.japanese.sentence.text,
                                [RussianToken(
                                    int(t.id.text),
                                    t.find('text').text,
                                    None if t.lexeme is None else t.lexeme.text,
                                    None if t.find('attributes') is None or t.find('attributes').children is None else
                                    [Attribute(a.find('name').text, a.value.text)
                                     for a in t.find('attributes').children if isinstance(a, Tag)],
                                    None if t.find('extraAttributes') is None or t.find(
                                        'extraAttributes').children is None else
                                    [a.text for a in t.find('extraAttributes').children if isinstance(a, Tag)]
                                )
                                    for t in sp.russian.tokens if isinstance(t, Tag)],
                                [JapaneseToken(
                                    int(t.id.text),
                                    t.find('text').text,
                                    None if t.lexeme is None else t.lexeme.text,
                                    None if t.reading is None else t.reading.text,
                                    None if t.translation is None else t.translation.text,
                                    None if t.find('attributes') is None or t.find('attributes').children is None else
                                    [Attribute(a.find('name').text, a.value.text)
                                     for a in t.find('attributes').children if isinstance(a, Tag)],
                                    None if t.find('extraAttributes') is None or t.find(
                                        'extraAttributes').children is None else
                                    [a.text for a in t.find('extraAttributes').children if isinstance(a, Tag)]
                                )
                                    for t in sp.japanese.tokens if isinstance(t, Tag)]
                                )
                   for sp in sps_xml.children if isinstance(sp, Tag)]

            title = Title(xml.entry.title.russian.text, xml.entry.title.japanese.text)
            ru_link = xml.entry.url.russian.text
            ja_link = xml.entry.url.japanese.text

            return Entry(id, sps, title, ru_link, ja_link)
