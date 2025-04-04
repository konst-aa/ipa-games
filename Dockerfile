FROM ghcr.io/astral-sh/uv:debian

RUN mkdir ipa-games
WORKDIR /root/ipa-games

RUN wget 'https://kaikki.org/dictionary/English/kaikki.org-dictionary-English.jsonl'

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

RUN uv venv
RUN bash -c 'source .venv/bin/activate && uv pip install -r pyproject.toml'


COPY english_api.py english_api.py
COPY run_dict.sh run_dict.sh

EXPOSE 6231
