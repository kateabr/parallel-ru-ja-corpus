package io.ktbr.parallel.ru.ja.corpus.web;

import javax.ws.rs.core.Application;
import org.eclipse.microprofile.openapi.annotations.OpenAPIDefinition;
import org.eclipse.microprofile.openapi.annotations.info.Contact;
import org.eclipse.microprofile.openapi.annotations.info.Info;
import org.eclipse.microprofile.openapi.annotations.info.License;

@OpenAPIDefinition(
        info = @Info(
                title = "Parallel Russian-Japanese Corpus API",
                version = "1.0.0",
                contact = @Contact(
                        name = "Ekaterina Biryukova",
                        url = "https://github.com/kateabr"
                ),
                license = @License(
                        name = "Apache 2.0",
                        url = "http://www.apache.org/licenses/LICENSE-2.0.html"
                )
        )
)
public class OpenApiMetadata extends Application {
}
