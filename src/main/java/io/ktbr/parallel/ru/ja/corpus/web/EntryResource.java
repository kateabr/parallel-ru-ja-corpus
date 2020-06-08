package io.ktbr.parallel.ru.ja.corpus.web;

import io.ktbr.parallel.ru.ja.corpus.model.basex.Language;
import io.ktbr.parallel.ru.ja.corpus.model.basex.SearchMode;
import io.ktbr.parallel.ru.ja.corpus.model.basex.SearchResult;
import io.ktbr.parallel.ru.ja.corpus.model.xml.Attribute;
import io.ktbr.parallel.ru.ja.corpus.model.xml.Entry;
import io.ktbr.parallel.ru.ja.corpus.model.xml.SentencePair;
import io.ktbr.parallel.ru.ja.corpus.service.EntryService;
import org.jboss.resteasy.annotations.jaxrs.PathParam;
import org.jboss.resteasy.annotations.jaxrs.QueryParam;

import javax.validation.constraints.*;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.StreamingOutput;
import java.io.ByteArrayOutputStream;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.stream.Collectors;

@Path("/api/v1/entry")
public class EntryResource {
    private final EntryService entryService;

    public EntryResource(EntryService entryService) {
        this.entryService = entryService;
    }

    @GET
    @Path("/{id}")
    @Produces({MediaType.APPLICATION_XML, MediaType.APPLICATION_JSON})
    public Entry loadEntry(@PathParam String id) {
        return entryService.loadEntry(id);
    }

    @GET
    @Path("/{id}/sentence/{sentenceId}")
    @Produces({MediaType.APPLICATION_XML, MediaType.APPLICATION_JSON})
    public SentencePair loadSentence(@PathParam String id, @PathParam long sentenceId) {
        return new SentencePair();
    }

    @GET
    @Path("/_search/token")
    @Produces({MediaType.APPLICATION_XML, MediaType.APPLICATION_JSON})
    public SearchResult tokenSearch(
            @QueryParam("query") String query,
            @QueryParam("lang") @NotNull Language language,
            @QueryParam("token_type") @NotNull SearchMode searchMode,
            @QueryParam("attr") List<@Pattern(regexp = "\\b.+=.+\\b") String> attributes,
            @QueryParam("ext_attr") List<String> extraAttributes,
            @QueryParam("offset") @NotNull @PositiveOrZero int offset,
            @QueryParam("limit") @NotNull @Positive @Max(50) int limit
    ) {
        if (query == null) query = "";

        List<Attribute> attributeList = convertToAttributes(attributes);
        return entryService.tokenSearch(
                query,
                language,
                searchMode,
                attributeList,
                extraAttributes,
                offset,
                limit
        );
    }

    @GET
    @Path("/_search/token/download")
    @Produces(MediaType.APPLICATION_XML)
    public Response tokenSearchDownload(
            @QueryParam("query") String query,
            @QueryParam("lang") @NotNull Language language,
            @QueryParam("token_type") @NotNull SearchMode searchMode,
            @QueryParam("attr") List<@Pattern(regexp = "\\b.+=.+\\b") String> attributes,
            @QueryParam("ext_attr") List<String> extraAttributes
    ) {
        if (query == null) query = "";

        List<Attribute> attributeList = convertToAttributes(attributes);
        ByteArrayOutputStream out = entryService.tokenSearchAll(query, language, searchMode, attributeList, extraAttributes);

        String filename = resultFilename();
        return searchResultResponse(out, filename);
    }

    @GET
    @Path("/_search/full-text")
    @Produces({MediaType.APPLICATION_XML, MediaType.APPLICATION_JSON})
    public SearchResult fullTextSearch(
            @QueryParam("query") @NotNull @NotBlank String query,
            @QueryParam("regex") @NotNull Boolean regex,
            @QueryParam("lang") @NotNull Language language,
            @QueryParam("offset") @NotNull @PositiveOrZero int offset,
            @QueryParam("limit") @NotNull @Positive @Max(50) int limit
    ) {
        return entryService.fullTextSearch(query, language, regex, offset, limit);
    }

    @GET
    @Path("/_search/full-text/download")
    @Produces(MediaType.APPLICATION_XML)
    public Response fullTextSearchDownload(
            @QueryParam("query") @NotNull @NotBlank String query,
            @QueryParam("regex") @NotNull Boolean regex,
            @QueryParam("lang") @NotNull Language language
    ) {
        ByteArrayOutputStream out = entryService.fullTextSearchAll(query, language, regex);

        String filename = resultFilename();
        return searchResultResponse(out, filename);
    }

    private Response searchResultResponse(ByteArrayOutputStream out, String filename) {
        return Response.ok((StreamingOutput) out::writeTo)
                .header("Content-Transfer-Encoding", "binary")
                .header("Content-Disposition", String.format(" attachment; filename=%s.xml", filename))
                .build();
    }

    private @NotNull String resultFilename() {
        return "search-results-" + LocalDateTime.now(ZoneOffset.UTC)
                .withNano(0)
                .format(DateTimeFormatter.ofPattern("H-mm-ss-d/M/yyyy"));
    }

    private @NotNull List<@NotNull Attribute> convertToAttributes(
            @QueryParam("attr") List<@Pattern(regexp = "\\b.+=.+\\b") String> attributes
    ) {
        return attributes.stream()
                .map(s -> {
                    String[] split = s.split("=");
                    Attribute attribute = new Attribute();
                    attribute.setName(split[0]);
                    attribute.setValue(split[1]);
                    return attribute;
                })
                .collect(Collectors.toList());
    }
}

