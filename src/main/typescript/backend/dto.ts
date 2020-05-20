export type Language = "RUSSIAN" | "JAPANESE";
export type TokenType = "WORD" | "LEXEME";

//*************************
// XML Entry

export interface Entry {
  id: string;
  url: Url;
  title: Title;
  sentencePairs: SentencePair[];
}

export interface Url {
  russian: string;
  japanese: string;
}

export interface Title {
  russian: string;
  japanese: string;
}

export interface SentencePair {
  id: number;
  russian: RussianSentence;
  japanese: JapaneseSentence;
}

export interface RussianSentence {
  sentence: string;
  tokens: RussianToken[];
}

export interface RussianToken {
  id: number;
  text: string;
  lexeme: string | null;
  attributes: Attribute[] | null;
  extraAttributes: string[] | null;
}

export interface JapaneseSentence {
  sentence: string;
  tokens: JapaneseToken[];
}

export interface JapaneseToken {
  id: number;
  text: string;
  lexeme: string | null;
  reading: string | null;
  translation: string | null;
  attributes: Attribute[] | null;
  extraAttributes: string[] | null;
}

export interface Attribute {
  name: string;
  value: string;
}

//*************************
// Search Result

export interface SearchResult {
  totalCount: number;
  request: Request;
  results: Result[];
}

export interface Request {
  database: string;
  language: Language;
  query: string;
  regex: string | null;
  searchMode: TokenType | null;
  attributes: Attribute[] | null;
  extraAttributes: string[] | null;
  offset: number;
  limit: number;
  elapsedTime: number;
}

export interface Result {
  entryId: number;
  entryTitle: Title;
  entryUrl: Url;
  tokenIds: number[] | null;
  sentencePair: SentencePair;
}
