package io.ktbr.parallel.ru.ja.corpus.model.xml;

import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementWrapper;
import javax.xml.bind.annotation.XmlType;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "russianSentence", propOrder = {"sentence", "tokens"})
public class RussianSentence {

    @XmlElement(required = true)
    protected String sentence;
    @XmlElement(required = true, name = "token")
    @XmlElementWrapper(name = "tokens")
    protected List<RussianToken> tokens;

    public String getSentence() {
        return sentence;
    }

    public void setSentence(String value) {
        this.sentence = value;
    }

    public List<RussianToken> getTokens() {
        return tokens;
    }

    public void setTokens(List<RussianToken> value) {
        this.tokens = value;
    }

}
