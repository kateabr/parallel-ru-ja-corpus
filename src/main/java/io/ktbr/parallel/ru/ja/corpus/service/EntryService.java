package io.ktbr.parallel.ru.ja.corpus.service;

import io.ktbr.parallel.ru.ja.corpus.BaseXClient;
import io.ktbr.parallel.ru.ja.corpus.model.basex.Language;
import io.ktbr.parallel.ru.ja.corpus.model.basex.SearchMode;
import io.ktbr.parallel.ru.ja.corpus.model.basex.SearchResult;
import io.ktbr.parallel.ru.ja.corpus.model.xml.Attribute;
import io.ktbr.parallel.ru.ja.corpus.model.xml.Entry;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.StringReader;
import java.util.List;
import java.util.stream.Collectors;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Provider;
import javax.ws.rs.BadRequestException;
import javax.ws.rs.NotFoundException;
import javax.xml.bind.JAXB;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.jetbrains.annotations.NotNull;

@ApplicationScoped
public class EntryService {
    private static final String XQUERY_PREAMBLE = "XQUERY import module namespace m='http://parallel-ru-ja-corpus.com'; ";

    private static final String LOAD_ENTRY_QUERY = XQUERY_PREAMBLE + "m:load-entry(\"%s\", \"%s\")";

    private static final String FULL_TEXT_SEARCH_QUERY = XQUERY_PREAMBLE
            + "m:full-text-search(\"%s\", \"%s\", \"%s\", %b(), %d, %d)";

    private static final String TOKEN_SEARCH_QUERY = XQUERY_PREAMBLE
            + "m:token-search(\"%s\", \"%s\", \"%s\", \"%s\", %s, %s, %d, %d)";

    private static final String RESOURCE_NOT_FOUND_MSG = "Resource not found";


    private final Provider<BaseXClient> dbProvider;
    private final String dbName;

    EntryService(
            Provider<BaseXClient> dbProvider,
            @ConfigProperty(name = "basex.database.name") String dbName
    ) {
        this.dbProvider = dbProvider;
        this.dbName = dbName;
    }

    public Entry loadEntry(String id) {
        BaseXClient client = dbProvider.get();

        try {
            final String xml = client.execute(String.format(LOAD_ENTRY_QUERY, dbName, id));
            if (xml.isBlank()) {
                throw new NotFoundException(RESOURCE_NOT_FOUND_MSG);
            }

            try (var reader = new StringReader(xml)) {
                return JAXB.unmarshal(reader, Entry.class);
            }
        } catch (IOException e) {
            throw processBaseXException(e);
        }
    }

    public SearchResult tokenSearch(
            String query,
            Language language,
            SearchMode searchMode,
            List<Attribute> attributeList,
            List<String> extraAttributes,
            int offset,
            int limit
    ) {
        BaseXClient client = dbProvider.get();

        try (var out = new ByteArrayOutputStream()) {
            int xqOffset = offset + 1; // xquery enumerates sequences from 1
            String attrs = attrsToXqueryMap(attributeList);
            String extraAttrs = extraAttrsToXquerySeq(extraAttributes);

            client.execute(
                    String.format(TOKEN_SEARCH_QUERY,
                            dbName, language, query, searchMode, attrs, extraAttrs, xqOffset, limit),
                    out
            );
            try (var in = new ByteArrayInputStream(out.toByteArray())) {
                return JAXB.unmarshal(in, SearchResult.class);
            }
        } catch (IOException e) {
            throw processBaseXException(e);
        }
    }

    public ByteArrayOutputStream tokenSearchAll(
            String query,
            Language language,
            SearchMode searchMode,
            List<Attribute> attributeList,
            List<String> extraAttributes
    ) {
        BaseXClient client = dbProvider.get();

        try (var out = new ByteArrayOutputStream()) {
            String attrs = attrsToXqueryMap(attributeList);
            String extraAttrs = extraAttrsToXquerySeq(extraAttributes);

            client.execute(
                    String.format(TOKEN_SEARCH_QUERY,
                            dbName, language, query, searchMode, attrs, extraAttrs, 1, 0),
                    out
            );
            return out;
        } catch (IOException e) {
            throw processBaseXException(e);
        }
    }

    public SearchResult fullTextSearch(String query, Language language, boolean regex, int offset, int limit) {
        BaseXClient client = dbProvider.get();

        try (var out = new ByteArrayOutputStream()) {
            int xqOffset = offset + 1; // xquery enumerates sequences from 1
            client.execute(
                    String.format(FULL_TEXT_SEARCH_QUERY, dbName, language, query, regex, xqOffset, limit),
                    out
            );
            try (var in = new ByteArrayInputStream(out.toByteArray())) {
                return JAXB.unmarshal(in, SearchResult.class);
            }
        } catch (IOException e) {
            throw processBaseXException(e);
        }
    }

    public ByteArrayOutputStream fullTextSearchAll(String query, Language language, boolean regex) {
        BaseXClient client = dbProvider.get();

        try (var out = new ByteArrayOutputStream()) {
            client.execute(
                    String.format(FULL_TEXT_SEARCH_QUERY, dbName, language, query, regex, 1, 0),
                    out
            );
            return out;
        } catch (IOException e) {
            throw processBaseXException(e);
        }
    }

    private @NotNull String extraAttrsToXquerySeq(List<String> extraAttributes) {
        return "(" + String.join(", ", extraAttributes) + ")";
    }

    private @NotNull String attrsToXqueryMap(List<Attribute> attributeList) {
        return "map {"
                + attributeList.stream()
                .map(a -> a.getName() + ":" + a.getValue())
                .collect(Collectors.joining(","))
                + "}";
    }

    private RuntimeException processBaseXException(Exception e) {
        String message = e.getMessage();
        if (message == null) {
            return new RuntimeException(e);
        }

        final RuntimeException ex;
        if (message.contains("FODC0002")) {
            ex = new NotFoundException(RESOURCE_NOT_FOUND_MSG, e);
        } else if (message.contains("FORX0002")) {
            ex = new BadRequestException("Invalid regular exception");
        } else {
            ex = new RuntimeException(e);
        }
        return ex;
    }
}

