# Use an official Python runtime based on Debian 10 "buster" as a parent image.
# Info: as of March 2021 python:3.8.1-slim-buster doesn't work because it skips istalling nodejs and npm from nodesource (See: https://github.com/nodejs/help/issues/554)
FROM python:3.8.1
ENV PYTHONUNBUFFERED=1


# For node
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --allow-releaseinfo-change --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    postgis \
    gdal-bin \
    python-gdal \
    python3-gdal \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    gettext \
    python-psycopg2 \
    nodejs \
    wkhtmltopdf \
    # Weasyprint requirements \
    libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Add group:user that will be used in the container.
RUN groupadd --gid 2000 planet
RUN useradd --uid 2000 --gid planet --create-home planet

# Use /src folder as a directory where the source code is stored.
RUN mkdir /src
WORKDIR /src

# Set this directory to be owned by the "planet" user.
RUN chown planet:planet /src

# JS dependencies
COPY package.json /src/
RUN npm install

# Python dependencies
COPY requirements/ requirements/
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r /src/requirements.txt

# Copy the source code of the project into the container.
COPY --chown=planet:planet . /src

# Use user "planet" to run the build commands and the server itself.
USER planet
