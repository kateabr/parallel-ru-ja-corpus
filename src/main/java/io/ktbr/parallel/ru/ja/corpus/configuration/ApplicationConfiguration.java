package io.ktbr.parallel.ru.ja.corpus.configuration;

import io.ktbr.parallel.ru.ja.corpus.BaseXClient;
import java.io.IOException;
import javax.enterprise.context.ApplicationScoped;
import javax.enterprise.inject.Default;
import javax.enterprise.inject.Produces;
import org.eclipse.microprofile.config.inject.ConfigProperty;

@ApplicationScoped
class ApplicationConfiguration {
    private final String baseXHost;
    private final int baseXPort;
    private final String baseXUsername;
    private final String baseXPassword;

    ApplicationConfiguration(
        @ConfigProperty(name = "basex.host") String baseXHost,
        @ConfigProperty(name = "basex.port") Integer baseXPort,
        @ConfigProperty(name = "basex.username") String baseXUsername,
        @ConfigProperty(name = "basex.password") String baseXPassword
    ) {
        this.baseXHost = baseXHost;
        this.baseXPort = baseXPort;
        this.baseXUsername = baseXUsername;
        this.baseXPassword = baseXPassword;
    }

    @Produces
    @Default
    BaseXClient baseXClient() throws IOException {
        return new BaseXClient(
            baseXHost,
            baseXPort,
            baseXUsername,
            baseXPassword
        );
    }

}
