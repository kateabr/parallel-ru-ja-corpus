package io.ktbr.parallel.ru.ja.corpus.model.xml;

import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementWrapper;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "japaneseToken", propOrder = {
        "id",
        "text",
        "lexeme",
        "reading",
        "translation",
        "attributes",
        "extraAttributes"
})
public class JapaneseToken {

    @XmlElement(required = true)
    @XmlSchemaType(name = "positiveInteger")
    protected long id;
    @XmlElement(required = true)
    protected String text;
    protected String lexeme;
    protected String reading;
    protected String translation;
    @XmlElementWrapper(name = "attributes")
    @XmlElement(name = "attribute")
    protected List<Attribute> attributes;
    @XmlElementWrapper(name = "extraAttributes")
    @XmlElement(name = "extraAttribute")
    protected List<String> extraAttributes;

    public long getId() {
        return id;
    }

    public void setId(long value) {
        this.id = value;
    }

    public String getText() {
        return text;
    }

    public void setText(String value) {
        this.text = value;
    }

    public String getLexeme() {
        return lexeme;
    }

    public void setLexeme(String value) {
        this.lexeme = value;
    }

    public String getReading() {
        return reading;
    }

    public void setReading(String value) {
        this.reading = value;
    }

    public String getTranslation() {
        return translation;
    }

    public void setTranslation(String value) {
        this.translation = value;
    }

    public List<Attribute> getAttributes() {
        return attributes;
    }

    public void setAttributes(List<Attribute> value) {
        this.attributes = value;
    }

    public List<String> getExtraAttributes() {
        return extraAttributes;
    }

    public void setExtraAttributes(List<String> value) {
        this.extraAttributes = value;
    }

}
