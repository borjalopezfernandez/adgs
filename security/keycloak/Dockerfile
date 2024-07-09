ARG VERSION=25.0.1

FROM quay.io/keycloak/keycloak:${VERSION} as build
ENV KC_FEATURES=admin-fine-grained-authz,recovery-codes,scripts,persistent-user-sessions,hostname:v2,organization
ENV METRICS_ENABLED=true
ENV HEALTH_ENABLED=true
ENV KC_DB=postgres
ARG VERSION
WORKDIR /opt/keycloak

RUN /opt/keycloak/bin/kc.sh build --features="$KC_FEATURES" --metrics-enabled="$METRICS_ENABLED" --health-enabled="$HEALTH_ENABLED"

FROM quay.io/keycloak/keycloak:${VERSION}
COPY --from=build /opt/keycloak/ /opt/keycloak/

USER root

RUN sed -i 's/1000/2020/' /etc/passwd

USER keycloak

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
