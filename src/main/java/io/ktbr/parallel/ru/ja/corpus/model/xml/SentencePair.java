package io.ktbr.parallel.ru.ja.corpus.model.xml;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "sentencePair", propOrder = {"id", "russian", "japanese"})
public class SentencePair {

    @XmlElement(required = true)
    @XmlSchemaType(name = "positiveInteger")
    protected long id;
    @XmlElement(required = true)
    protected RussianSentence russian;
    @XmlElement(required = true)
    protected JapaneseSentence japanese;

    public long getId() {
        return id;
    }

    public void setId(long value) {
        this.id = value;
    }

    public RussianSentence getRussian() {
        return russian;
    }

    public void setRussian(RussianSentence value) {
        this.russian = value;
    }

    public JapaneseSentence getJapanese() {
        return japanese;
    }

    public void setJapanese(JapaneseSentence value) {
        this.japanese = value;
    }

}
