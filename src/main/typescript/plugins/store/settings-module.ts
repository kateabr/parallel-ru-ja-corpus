import { Actions, Getters, Module, Mutations } from "vuex-smart-module";
import { vuetify } from "@/plugins/vuetify";

export type Theme = "Dark" | "Light";
export type LocaleCode = "en" | "ja" | "ru";

class SettingsState {
  theme: Theme = "Light";
  locale: LocaleCode = navigator.language.startsWith("ru")
    ? "ru"
    : navigator.language.startsWith("ja")
    ? "ja"
    : "en";
  itemsPerPage: number = 10;
}

class SettingsGetters extends Getters<SettingsState> {
  get isDarkTheme(): boolean {
    return this.state.theme === "Dark";
  }

  get theme(): Theme {
    return this.state.theme;
  }

  get locale(): LocaleCode {
    return this.state.locale;
  }

  get itemsPerPage(): number {
    return this.state.itemsPerPage;
  }
}

class SettingsMutations extends Mutations<SettingsState> {
  setTheme(theme: Theme): void {
    this.state.theme = theme;
    vuetify.framework.theme.dark = this.state.theme === "Dark";
  }

  setLocale(locale: LocaleCode): void {
    this.state.locale = locale;
    vuetify.framework.lang.current = locale;
  }

  setItemsPerPage(itemsPerPage: number) {
    this.state.itemsPerPage = itemsPerPage;
  }
}

class SettingsActions extends Actions<
  SettingsState,
  SettingsGetters,
  SettingsMutations,
  SettingsActions
> {
  setTheme(theme: Theme) {
    this.mutations.setTheme(theme);
  }

  setLocale(locale: LocaleCode): void {
    this.mutations.setLocale(locale);
  }

  setItemsPerPage(itemsPerPage: number) {
    this.mutations.setItemsPerPage(itemsPerPage);
  }
}

export const settingsModule = new Module({
  state: SettingsState,
  getters: SettingsGetters,
  mutations: SettingsMutations,
  actions: SettingsActions
});
