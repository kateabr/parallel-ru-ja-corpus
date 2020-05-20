// eslint-disable-next-line @typescript-eslint/no-var-requires
const path = require("path");

module.exports = {
  pages: {
    index: {
      entry: "src/main/typescript/index.ts",
      title: "Parallel Russian-Japanese Corpus"
    }
  },

  configureWebpack: {
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "src/main/typescript")
      }
    }
  },

  outputDir: "target/spa",
  lintOnSave: false,

  css: {
    sourceMap: true
  },

  devServer: {
    proxy: "http://localhost:8080"
  }
};
