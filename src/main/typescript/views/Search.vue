<template>
  <div>
    <v-card outlined class="pa-3">
      <v-row>
        <v-col>
          <v-tabs v-model="searchMode">
            <v-tab key="0">Полнотекстовой поиск</v-tab>
            <v-tab key="1">Поиск по словоформам</v-tab>
          </v-tabs>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4">
          <v-radio-group
            v-model="searchLanguage"
            label="Язык поиска"
            row
            @change="resetInput()"
          >
            <v-radio label="Русский" value="RUSSIAN" />
            <v-radio label="Японский" value="JAPANESE" />
          </v-radio-group>
        </v-col>
        <v-col v-if="searchMode === 0" cols="4"><v-switch v-model="regex" label="Regex" /></v-col>
        <v-col v-if="searchMode === 1" cols="4">
          <v-radio-group v-model="searchTokenType" row>
            <v-radio label="Поиск по слову" value="WORD" />
            <v-radio label="Поиск по лексеме" value="LEXEME" />
          </v-radio-group>
        </v-col>
        <v-col align-self="center">
          <v-menu
                  transition="slide-y-transition"
                  bottom
                  offset-y
          >
            <template v-slot:activator="{ on }">
              <v-btn v-on="on">
                Результатов на странице: {{itemsPerPage}}
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                      v-for="item in itemsPerPageVariants"
                      :key="item"
                      @change="search(1)"
                      @click="itemsPerPage = item"
              >
                <v-list-item-title>{{ item }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-col>
      </v-row>
      <v-tabs-items v-model="searchMode">
        <v-tab-item key="0" :transition="true" :reverse-transition="false">
          <v-row>
            <v-col>
            <v-text-field
                    clearable
              v-model="searchQuery"
              label="Слово или фраза"
              @click:clear="searchQuery = ''"
              @keydown.enter="search(1)"
            />
            </v-col>
          </v-row>
        </v-tab-item>
        <v-tab-item key="1" :transition="true" :reverse-transition="false">
          <v-row>
            <v-col>
          <v-text-field
                  clearable
            v-model="searchQuery"
            label="Слово или лексема"
            @click:clear="searchQuery = ''"
            @keydown.enter="search(1)"
          />
            </v-col>
          </v-row>
          <v-row
            v-for="item in attributeList"
            :key="attributeList.indexOf(item)"
          >
            <v-col>
              <v-text-field
                v-model="item.name"
                dense
                outlined
                readonly
              ></v-text-field>
            </v-col>
            <v-col>
              <v-text-field
                v-model="item.value"
                outlined
                dense
                readonly
              ></v-text-field
            ></v-col>
            <v-col cols="1">
              <v-btn
                depressed
                color="red lighten-1"
                class="mx-2"
                small
                fab
                @click="attributeList.splice(attributeList.indexOf(item), 1)"
              >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row v-if="searchLanguage === 'JAPANESE'">
            <v-col>
              <v-autocomplete
                v-model="attributePlaceholderName"
                :items="attributeListNamesJa"
                dense
                outlined
                label="Основной параметр"
              ></v-autocomplete>
            </v-col>
            <v-col>
              <v-autocomplete
                v-model="attributePlaceholderValue"
                :items="attributeListMapJa.get(attributePlaceholderName)"
                outlined
                dense
                label="Значение параметра"
              ></v-autocomplete
            ></v-col>
            <v-col cols="1">
              <v-btn
                :disabled="
                  !(
                    attributePlaceholderValue.length !== 0 &&
                    attributePlaceholderName.length !== 0
                  )
                "
                depressed
                color="green lighten-1"
                class="mx-2"
                small
                fab
                @click="addAttribute()"
              >
                <v-icon>mdi-check</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row v-if="searchLanguage === 'RUSSIAN'">
            <v-col>
              <v-autocomplete
                v-model="attributePlaceholderName"
                :items="attributeListNamesRu"
                dense
                outlined
                label="Основной параметр"
              ></v-autocomplete>
            </v-col>
            <v-col>
              <v-autocomplete
                v-model="attributePlaceholderValue"
                :items="attributeListMapRu.get(attributePlaceholderName)"
                outlined
                dense
                label="Значение параметра"
              ></v-autocomplete
            ></v-col>
            <v-col cols="1">
              <v-btn
                :disabled="
                  !(
                    attributePlaceholderValue.length !== 0 &&
                    attributePlaceholderName.length !== 0
                  )
                "
                depressed
                color="green lighten-1"
                class="mx-2"
                small
                fab
                @click="addAttribute()"
              >
                <v-icon>mdi-check</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row v-if="searchLanguage === 'JAPANESE'">
            <v-col>
              <v-autocomplete
                v-model="extraAttributeList"
                :items="extraAttributeNamesJa"
                outlined
                dense
                clearable
                small-chips
                deletable-chips
                label="Дополнительные параметры"
                multiple
              ></v-autocomplete>
            </v-col>
          </v-row>
            <v-row v-if="searchLanguage === 'RUSSIAN'">
              <v-col>
                <v-autocomplete
                        v-model="extraAttributeList"
                        :items="extraAttributeNamesRu"
                        outlined
                        dense
                        clearable
                        small-chips
                        deletable-chips
                        label="Дополнительные параметры"
                        multiple
                ></v-autocomplete>
              </v-col>
            </v-row>
        </v-tab-item>
      </v-tabs-items>
      <v-row>
        <v-col cols="4"></v-col>
        <v-col cols="4">
          <v-btn
            block
            color="primary"
            :loading="loading"
            :disabled="
              searchQuery.trim() === '' &&
              attributeList.length === 0 &&
              extraAttributeList.length === 0
            "
            @click="search(1)"
          >
            <v-icon left class="mdi mdi-magnify"></v-icon>
            Поиск
          </v-btn>
        </v-col>
        <v-col cols="4"></v-col>
      </v-row>
    </v-card>

    <div v-if="searchResult !== null">
        <v-row class="pl-3 pr-3 pt-2 pb-2">
          <v-col cols="9">
      <div class="pt-1">Время поиска: {{ String(queryTime() / 1000.0) }} с</div>
            <div class="pt-1">Найдено результатов: {{ searchResult.totalCount }}</div>
          </v-col>
          <v-col cols="3" align-self="center">
      <v-btn
              block
        color="primary"
        :disabled="loading || results.length < 1"
        @click="downloadResults"
      >
        <v-icon left>mdi-download</v-icon>
        Скачать результаты
      </v-btn>
          </v-col>
        </v-row>
      <sentence-pair-card
        v-for="result in results"
        :key="result.entryId + ',' + result.sentencePair.id"
        :result="result"
        :search-language="searchResult.request.language"
      />
    </div>

    <div class="ma-5">
    <v-pagination
      :value="page"
      :length="numberOfPages()"
      :total-visible="7"
      :disabled="loading"
      @input="changePage"
    />
    </div>

    <v-snackbar v-model="error">
      {{ errorMessage }}
      <v-btn color="red" text @click="error = false">
        Скрыть
      </v-btn>
    </v-snackbar>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Component, Watch } from "vue-property-decorator";
import {
  Attribute,
  Language,
  Result,
  SearchResult,
  TokenType
} from "@/backend/dto";
import { api } from "@/backend";
import { Dictionary } from "vue-router/types/router";
import SentencePairCard from "@/components/SentencePairCard.vue";
import { settingsModule } from "@/plugins/store/settings-module";

@Component({
  components: { SentencePairCard }
})
export default class extends Vue {
  private readonly settingsStore = settingsModule.context(this.$store);

  private searchResult: SearchResult | null = null;
  private results: Result[] = [];

  private page = 1;
  private itemsPerPage = this.settingsStore.getters.itemsPerPage;
  private itemsPerPageVariants = [10, 20, 50]

  private searchQuery: string = "";
  private regex: boolean = false;
  private attributeList: Attribute[] = [];
  private attributeListNamesJa: string[] = ["pos", "type", 'stem_type', 'row', 'form', 'adj_type', 'transitivity',
    'attachment_form', 'form', 'form1', 'form2', 'derivation_type', 'reading_type'];
  private attributeListMapJa: Map<string, string[]> = new Map<string, string[]>(
    [
      ['pos', ['Verb', 'Noun', 'Adjective', 'Judgemental', 'Suffix', 'Particle', 'Prefix', 'Demonstrative', 'Adverb',
      'Conjunction', 'Interjection', 'Numeral']],
      ['type', ['Common', 'Suru', 'Proper', 'Toponym', 'Human_name', 'Organization_name', 'Expletive', 'Adverbial',
      'Temporal', 'Nominal', 'Adnominal', 'Adjectival', 'Adverbial', 'Case_marking', 'Conjunctive', 'Sentence_ending',
      'Verbal', 'Auxiliary', 'I', 'Na', 'NaNo', 'Taru', 'Zuru']],
      ['stem_type', ['Consonant', 'Vowel']],
      ['row', ['Ka', 'Ga', 'Sa', 'Ta', 'Na', 'Ba', 'Ma', 'Ra', 'Wa', 'Da', 'AUO', 'I']],
      ['form', ['Written', 'I']],
      ['adj_type', ['I', 'Na']],
      ['transitivity', ['Intransitive', 'Transitive', 'Both']],
      ['attachment_form', ['Basic', 'Ta_system']],
      ['form', ['Short', 'Written', 'I', 'Tari', 'Cha', 'Ja']],
      ['form1', ['Ta', 'Te', 'Basic', 'Imperfective']],
      ['form2', ['Assumptional', 'Conditional', 'Conjunctive', 'Imperative', 'Volitional'],],
      ['derivation_type', ['Verbal', 'Adjectival', 'Nominal']],
      ['reading_type', ['Kun', 'On']]
    ]
  );
  private attributeListNamesRu: string[] = ['animacy', 'aspect', 'case', 'degree', 'gender', 'mood',
    'number', 'person', 'pos', 'tense', 'variant', 'verbform', 'voice'];
  private attributeListMapRu: Map<string, string[]> = new Map<string, string[]>(
    [['animacy', ['ANIMATE', 'INANIMATE']],
      ['aspect', ['PERFECT', 'IMPERFECT']],
      ['case', ['NOMINATIVE', 'GENITIVE', 'DATIVE', 'ACCUSATIVE', 'LOCATIVE', 'INSTRUCTIVE']],
      ['degree', ['POSITIVE', 'COMPARATIVE']],
      ['gender', ['MASCULINE', 'FEMININE', 'NEUTER']],
      ['mood', ['INDICATIVE', 'IMPERATIVE']],
      ['number', ['SINGULAR', 'PLURAL']],
      ['person', ['FIRST', 'SECOND', 'THIRD']],
      ['pos', ['NOUN', 'ADJECTIVE', 'PRONOUN', 'NUMERICAL', 'VERB', 'ADVERB', 'DETERMINANT',
      'CONJUNCTION', 'ADPOSITION', 'PARTICLE', 'INTERJECTION', 'INTRODUCTION', 'UNKNOWN']],
      ['tense', ['PAST', 'PRESENT', 'FUTURE']],
      ['variant', ['FULL', 'SHORT']],
      ['verbform', ['INFINITIVE', 'FINITE', 'CONVERB']],
      ['voice', ['ACTIVE', 'MIDDLE', 'PASSIVE']]]
  );
  private extraAttributeList: string[] = [];
  private extraAttributeNamesJa: string[] = [
    'FamN',
    'PersN',
    'Human_name_or_family_name',
    'Abbr',
    'Content_word',
    'Hiragana',
    'Kanji',
    'Katakana',
    'Digits',
    'unknown_reading',
    'Progressive',
    'unrecognized_symbols',
    'Associated_content_word',
    'Counting',
    'To_supplement',
    'Ender',
    'Toponym',
    'Address',
    'Post',
    'Organisation',
    'Human_name',
    'Predicative',
    'Special',
    'Counting',
    'Nominal',
    'Nasalization_change',
    'Euphonic_change',
    'Irregular',
    'Ta_system',
    'Uru',
    'japanese',
    'foreign',
    'Former_name',
    'Potential',
    'Onomatopoeia',
    'Causative',
    'Masu',
    'Nu',
    'Negation',
    'Darou',
    'Souda',
    'Ku',
    'Compound_word',
    'Consonant_reduplication',
    'Stem',
    'Historical_compound_word',
    'Weak_temporal_noun',
    'Weak_declinable_modifier',
    'Quantity_modifier',
    'Ni_case_modifier',
    'De_case_modifier',
    'To_case_modifier',
    'Derivative',
    'Relativity_noun',
    'Relativity_modifier'
  ];
  private extraAttributeNamesRu: string[] = ['Parenth',
  'Toponym',
  'PersN',
  'PatrN',
  'Praed',
  'Informal',
  'Abbr',
  'Obsolete',
  'FamN'];

  private searchMode: SearchMode = SearchMode.FULL_TEXT;
  private searchLanguage: Language = "RUSSIAN";
  private searchTokenType: TokenType = "WORD";

  private attributePlaceholderName = "";
  private attributePlaceholderValue = "";

  private loading = false;
  private error = false;
  private errorMessage = "";

  async search(page: number) {
    this.page = page;

    this.updateUrlQuery();

    try {
      this.requestStarted();

      switch (this.searchMode) {
        case SearchMode.FULL_TEXT:
          this.searchResult = await api.fullTextSearch(
            this.searchQuery,
            this.searchLanguage,
            this.regex,
            this.offset(),
            this.itemsPerPage
          );
          break;
        case SearchMode.WORD_FORM:
          this.searchResult = await api.tokenSearch(
            this.searchQuery,
            this.searchLanguage,
            this.searchTokenType,
            this.attributeList,
            this.extraAttributeList,
            this.offset(),
            this.itemsPerPage
          );
          break;
      }
    } catch (e) {
      this.requestErrored(e);
    } finally {
      this.requestEnded();
    }
  }

  async downloadResults() {
    try {
      this.requestStarted();

      let url: string;
      switch (this.searchMode) {
        case SearchMode.FULL_TEXT:
          url = api.fullTextSearchDownloadUrl(
            this.searchQuery,
            this.searchLanguage,
            this.regex
          );
          break;
        case SearchMode.WORD_FORM:
          url = api.tokenSearchDownloadUrl(
            this.searchQuery,
            this.searchLanguage,
            this.searchTokenType,
            this.attributeList,
            this.extraAttributeList
          );
          break;
      }
      window.open(url, "_blank");
    } catch (e) {
      this.requestErrored(e);
    } finally {
      this.requestEnded();
    }
  }

  addAttribute() {
    this.attributeList.push({
      name: this.attributePlaceholderName,
      value: this.attributePlaceholderValue
    });
    this.attributePlaceholderName = "";
    this.attributePlaceholderValue = "";
  }

  resetInput() {
    this.attributeList.splice(0, this.attributeList.length);
    this.extraAttributeList.splice(0, this.extraAttributeList.length);
    this.searchQuery = '';
  }

  updateUrlQuery() {
    this.$router
      .push({
        name: "search",
        query: this.paramsToQuery()
      })
      .catch(reason => {
        // vue-router will throw NavigationDuplicated if the route is the same, do nothing
        if (reason.name === "NavigationDuplicated") {
          /* ignored */
        } else {
          console.log("Unexpected error during route navigation: " + reason);
        }
      });
  }

  @Watch("searchResult")
  queryTime(): number {
    if (this.searchResult === null) {
      return 0;
    }
    return this.searchResult.request.elapsedTime;
  }

  @Watch("searchResult")
  onSearchResultUpdate() {
    if (this.searchResult === null) return;
    this.results = this.searchResult.results;
  }

  changePage(page: number) {
    this.search(page);
  }

  numberOfPages(): number {
    if (this.searchResult === null) return 0;
    return Math.ceil(this.searchResult.totalCount / this.itemsPerPage);
  }

  offset(): number {
    return (this.page - 1) * this.itemsPerPage;
  }

  requestStarted() {
    this.loading = true;
  }

  requestEnded() {
    this.loading = false;
  }

  requestErrored(e: Error) {
    const code: number | null = e.response.status ?? null;
    if (code == null) {
      this.errorMessage = "Неизвестная ошибка";
    } else {
      if (code >= 400 && code < 500) {
        this.errorMessage =
          "Ошибка запроса, обновите адресную строку и повторите запрос";
      } else if (code >= 500) {
        this.errorMessage = "Сервер не смог обработать запрос";
      } else {
        this.errorMessage = "Неизвестная ошибка";
      }
    }

    this.error = true;
  }

  paramsToQuery(): Dictionary<string | (string | null)[] | null | undefined> {
    const query: Dictionary<string | (string | null)[] | null | undefined> = {};

    query.searchQuery = this.searchQuery;
    query.searchLanguage = this.searchLanguage;
    query.searchMode = this.searchMode.toString();
    query.searchTokenType = this.searchTokenType;
    query.regex = this.regex.toString();
    query.attributeList = JSON.stringify(this.attributeList);
    query.extraAttributeList = JSON.stringify(this.extraAttributeList);
    query.offset = this.offset().toString();
    query.limit = this.itemsPerPage.toString();

    return query;
  }

  created() {
    // map every known query parameter to UI

    const query = this.$route.query;
    this.searchQuery = (query.searchQuery as string) || this.searchQuery;
    this.searchLanguage =
      (query.searchLanguage as Language) || this.searchLanguage;
    this.searchMode =
      (Number(query.searchMode) as SearchMode) || this.searchMode;
    this.searchTokenType =
      (query.searchTokenType as TokenType) || this.searchTokenType;

    this.regex = Boolean(query.regex === "true") || this.regex;

    if (query.attributeList) {
      try {
        this.attributeList = JSON.parse(query.attributeList as string);
        // eslint-disable-next-line no-empty
      } catch (ignored) {}
    }
    if (query.extraAttributeList) {
      try {
        this.extraAttributeList = JSON.parse(
          query.extraAttributeList as string
        );
        // eslint-disable-next-line no-empty
      } catch (ignored) {}
    }

    this.itemsPerPage = Number(query.limit as string) || this.itemsPerPage;
    if (query.offset) {
      const offset = Number(query.offset as string) || 1;
      this.page = Math.floor(offset / this.itemsPerPage) + 1 || this.page;
    }
  }

  mounted() {
    const query = this.$route.query;
    if (query.searchQuery == null) return;
    this.search(this.page);
  }
}

enum SearchMode {
  FULL_TEXT = 0,
  WORD_FORM = 1
}
</script>
