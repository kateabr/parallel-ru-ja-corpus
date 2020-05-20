package io.ktbr.parallel.ru.ja.corpus.web;

import io.ktbr.parallel.ru.ja.corpus.BaseXClient;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Provider;
import org.eclipse.microprofile.health.HealthCheck;
import org.eclipse.microprofile.health.HealthCheckResponse;
import org.eclipse.microprofile.health.Readiness;

@Readiness
@ApplicationScoped
public class DatabaseHealthCheck implements HealthCheck {

    private final Provider<BaseXClient> dbProvider;

    public DatabaseHealthCheck(Provider<BaseXClient> dbProvider) {
        this.dbProvider = dbProvider;
    }

    @Override
    public HealthCheckResponse call() {
        var builder = HealthCheckResponse.named("BaseX connection health check");

        HealthCheckResponse health = builder.down().build();
        try {
            var baseXClient = dbProvider.get();
            String response = baseXClient.execute("INFO");

            Map<String, String> info = Stream.of(
                response
                    .substring(0, response.indexOf("Global options"))
                    .substring("General Information:".length())
                    .trim()
                    .split("\n"))
                .collect(Collectors.toMap(
                    s -> s.split(":")[0],
                    s -> s.split(":")[1])
                );

            var up = builder.up();
            for (var key : info.keySet()) {
                up.withData(key, info.get(key));
            }

            health = up.build();
        } catch (Exception ignored) {
        }

        return health;
    }
}
