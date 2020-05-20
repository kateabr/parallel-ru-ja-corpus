import { axios } from "@/backend/axios";
import { Attribute, Entry, SearchResult, TokenType } from "@/backend/dto";

export const api = {
  fullTextSearchDownloadUrl(
    query: string,
    lang: string,
    regex: boolean
  ): string {
    const params = new URLSearchParams([
      ["query", query],
      ["lang", lang],
      ["regex", String(regex)]
    ]);
    return `/api/v1/entry/_search/full-text/download?${params.toString()}`;
  },
  async fullTextSearch(
    query: string,
    lang: string,
    regex: boolean,
    offset: number,
    limit: number
  ): Promise<SearchResult> {
    return axios
      .get<SearchResult>("/api/v1/entry/_search/full-text", {
        params: {
          query: query,
          lang: lang,
          regex: regex,
          offset: offset,
          limit: limit
        }
      })
      .then(value => value.data);
  },
  tokenSearchDownloadUrl(
    query: string,
    lang: string,
    tokenType: TokenType,
    attributes: Attribute[] | null,
    extraAttributes: string[] | null
  ): string {
    const params = new URLSearchParams([
      ["query", query],
      ["lang", lang],
      ["token_type", tokenType]
    ]);
    attributes
      ?.map(a => `${a.name}=${a.value}`)
      .forEach(a => params.append("attr", a));
    extraAttributes?.forEach(a => params.append("ext_attr", a));

    return `/api/v1/entry/_search/token/download?${params.toString()}`;
  },
  async tokenSearch(
    query: string,
    lang: string,
    tokenType: TokenType,
    attributes: Attribute[] | null,
    extraAttributes: string[] | null,
    offset: number,
    limit: number
  ): Promise<SearchResult> {
    /* eslint-disable @typescript-eslint/camelcase */
    return axios
      .get<SearchResult>("/api/v1/entry/_search/token", {
        params: {
          query: query,
          lang: lang,
          token_type: tokenType,
          attr: attributes?.map(a => `${a.name}=${a.value}`),
          ext_attr: extraAttributes,
          offset: offset,
          limit: limit
        }
      })
      .then(value => value.data);
    /* eslint-enable @typescript-eslint/camelcase */
  },
  async loadEntry(id: string): Promise<Entry> {
    /* eslint-disable @typescript-eslint/camelcase */
    return axios
      .get<Entry>(`/api/v1/entry/${id}`, {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json"
        }
      })
      .then(value => value.data);
    /* eslint-enable @typescript-eslint/camelcase */
  }
};
