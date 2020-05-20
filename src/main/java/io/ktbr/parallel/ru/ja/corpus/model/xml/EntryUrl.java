package io.ktbr.parallel.ru.ja.corpus.model.xml;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "entryUrl", propOrder = {"russian", "japanese"})
public class EntryUrl {

    @XmlSchemaType(name = "anyURI")
    protected String russian;
    @XmlSchemaType(name = "anyURI")
    protected String japanese;

    public String getRussian() {
        return russian;
    }

    public void setRussian(String value) {
        this.russian = value;
    }

    public String getJapanese() {
        return japanese;
    }

    public void setJapanese(String value) {
        this.japanese = value;
    }

}
