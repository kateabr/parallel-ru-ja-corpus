package io.ktbr.parallel.ru.ja.corpus.model.xml;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlType;


@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "entryTitle", propOrder = {"russian", "japanese"})
public class EntryTitle {

    protected String russian;
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
