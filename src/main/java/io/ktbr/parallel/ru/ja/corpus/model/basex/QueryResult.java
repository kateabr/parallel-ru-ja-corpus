package io.ktbr.parallel.ru.ja.corpus.model.basex;

import io.ktbr.parallel.ru.ja.corpus.model.xml.EntryTitle;
import io.ktbr.parallel.ru.ja.corpus.model.xml.EntryUrl;
import io.ktbr.parallel.ru.ja.corpus.model.xml.SentencePair;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementWrapper;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;

@XmlRootElement(name = "result")
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {"entryId", "entryTitle", "entryUrl", "tokenIds", "sentencePair"})
public class QueryResult {
    @XmlElement(required = true)
    protected long entryId;
    @XmlElement
    protected EntryTitle entryTitle;
    @XmlElement
    protected EntryUrl entryUrl;
    @XmlElement(required = true, name = "id")
    @XmlElementWrapper(name = "tokenIds")
    protected List<Long> tokenIds;
    @XmlElement(required = true)
    protected SentencePair sentencePair;

    public List<Long> getTokenIds() {
        return tokenIds;
    }

    public void setTokenIds(List<Long> tokenIds) {
        this.tokenIds = tokenIds;
    }

    public EntryTitle getEntryTitle() {
        return entryTitle;
    }

    public void setEntryTitle(EntryTitle entryTitle) {
        this.entryTitle = entryTitle;
    }

    public EntryUrl getEntryUrl() {
        return entryUrl;
    }

    public void setEntryUrl(EntryUrl entryUrl) {
        this.entryUrl = entryUrl;
    }

    public long getEntryId() {
        return entryId;
    }

    public void setEntryId(long entryId) {
        this.entryId = entryId;
    }

    public SentencePair getSentencePair() {
        return sentencePair;
    }

    public void setSentencePair(SentencePair sentencePair) {
        this.sentencePair = sentencePair;
    }
}
