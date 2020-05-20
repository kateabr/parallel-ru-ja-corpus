package io.ktbr.parallel.ru.ja.corpus.model.xml;

import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementWrapper;
import javax.xml.bind.annotation.XmlType;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "japaneseSentence", propOrder = {"sentence", "tokens"})
public class JapaneseSentence {

    @XmlElement(required = true)
    protected String sentence;
    @XmlElement(required = true, name = "token")
    @XmlElementWrapper(name = "tokens")
    protected List<JapaneseToken> tokens;

    public String getSentence() {
        return sentence;
    }

    public void setSentence(String value) {
        this.sentence = value;
    }

    public List<JapaneseToken> getTokens() {
        return tokens;
    }

    public void setTokens(List<JapaneseToken> value) {
        this.tokens = value;
    }

}
