FROM openeuler/openeuler:22.03-lts

WORKDIR /opt/aivuln
COPY . /opt/aivuln

RUN dnf install -y python3 python3-pip && \
    python3 -m pip install --no-index --find-links wheelhouse -r requirements.txt && \
    chmod +x scripts/*.sh

ENV PYTHONPATH=/opt/aivuln/src
EXPOSE 18080
CMD ["./scripts/start_api.sh"]

