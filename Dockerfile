FROM python:3.12

SHELL [ "/bin/bash", "-c" ]
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y dos2unix
RUN pip install --upgrade pip
WORKDIR /app

RUN useradd -rms /bin/bash fm && chmod 777 /opt /run

WORKDIR /fm

RUN mkdir /fm/static && mkdir /fm/media && chown -R fm:fm /fm && chmod 755 /fm

COPY --chown=fm:fm . .
RUN find . -type f -print0 | xargs -0 dos2unix  # Преобразование всех файлов

RUN pip install -r requirements.txt

USER fm
CMD ["gunicorn", "-b", "0.0.0.0:8001", "mlbb_faceit.wsgi:application"]
