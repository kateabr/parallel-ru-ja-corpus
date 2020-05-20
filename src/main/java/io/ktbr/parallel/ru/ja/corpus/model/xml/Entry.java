package io.ktbr.parallel.ru.ja.corpus.model.xml;

import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementWrapper;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {"id", "url", "title", "sentencePairs"})
@XmlRootElement(name = "entry")
public class Entry {

    @XmlElement(required = true)
    protected String id;
    protected EntryUrl url;
    protected EntryTitle title;
    @XmlElement(required = true, name = "sentencePair")
    @XmlElementWrapper(name = "sentencePairs")
    protected List<SentencePair> sentencePairs;

    public String getId() {
        return id;
    }

    public void setId(String value) {
        this.id = value;
    }

    public EntryUrl getUrl() {
        return url;
    }

    public void setUrl(EntryUrl value) {
        this.url = value;
    }

    public EntryTitle getTitle() {
        return title;
    }

    public void setTitle(EntryTitle value) {
        this.title = value;
    }

    public List<SentencePair> getSentencePairs() {
        return sentencePairs;
    }

    public void setSentencePairs(List<SentencePair> value) {
        this.sentencePairs = value;
    }

}
