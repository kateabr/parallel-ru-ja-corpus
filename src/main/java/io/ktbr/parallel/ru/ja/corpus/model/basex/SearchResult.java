package io.ktbr.parallel.ru.ja.corpus.model.basex;

import io.ktbr.parallel.ru.ja.corpus.model.xml.Attribute;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementWrapper;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {"totalCount", "request", "results"})
@XmlRootElement(name = "searchResult")
public class SearchResult {
    @XmlElement(required = true)
    protected long totalCount;
    @XmlElement(required = true)
    protected SearchRequest request;
    @XmlElement(required = true, name = "result")
    @XmlElementWrapper(name = "results")
    protected List<QueryResult> results;

    public SearchRequest getRequest() {
        return request;
    }

    public void setRequest(SearchRequest request) {
        this.request = request;
    }

    public long getTotalCount() {
        return totalCount;
    }

    public void setTotalCount(long totalCount) {
        this.totalCount = totalCount;
    }

    public List<QueryResult> getResults() {
        return results;
    }

    public void setResults(List<QueryResult> results) {
        this.results = results;
    }

    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
            "database",
            "language",
            "query",
            "regex",
            "searchMode",
            "attributes",
            "extraAttributes",
            "offset",
            "limit",
            "elapsedTime"
    })
    @XmlRootElement(name = "request")
    public static class SearchRequest {
        @XmlElement(required = true)
        protected String database;
        @XmlElement(required = true)
        protected Language language;
        @XmlElement(required = true)
        protected String query;
        @XmlElement
        protected String searchMode;
        @XmlElement
        protected String regex;
        @XmlElementWrapper(name = "attributes")
        @XmlElement(name = "attribute")
        protected List<Attribute> attributes;
        @XmlElementWrapper(name = "extraAttributes")
        @XmlElement(name = "extraAttribute")
        protected List<String> extraAttributes;
        @XmlElement(required = true)
        protected long offset;
        @XmlElement(required = true)
        protected long limit;
        @XmlElement(required = true)
        protected long elapsedTime;

        public long getElapsedTime() {
            return elapsedTime;
        }

        public void setElapsedTime(long elapsedTime) {
            this.elapsedTime = elapsedTime;
        }

        public String getRegex() {
            return regex;
        }

        public void setRegex(String regex) {
            this.regex = regex;
        }

        public String getDatabase() {
            return database;
        }

        public void setDatabase(String database) {
            this.database = database;
        }

        public Language getLanguage() {
            return language;
        }

        public void setLanguage(Language language) {
            this.language = language;
        }

        public String getQuery() {
            return query;
        }

        public void setQuery(String query) {
            this.query = query;
        }

        public String getSearchMode() {
            return searchMode;
        }

        public void setSearchMode(String searchMode) {
            this.searchMode = searchMode;
        }

        public List<Attribute> getAttributes() {
            return attributes;
        }

        public void setAttributes(List<Attribute> attributes) {
            this.attributes = attributes;
        }

        public List<String> getExtraAttributes() {
            return extraAttributes;
        }

        public void setExtraAttributes(List<String> extraAttributes) {
            this.extraAttributes = extraAttributes;
        }

        public long getOffset() {
            return offset;
        }

        public void setOffset(long offset) {
            this.offset = offset;
        }

        public long getLimit() {
            return limit;
        }

        public void setLimit(long limit) {
            this.limit = limit;
        }
    }
}
