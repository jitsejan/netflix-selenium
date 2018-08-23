FROM continuumio/miniconda3
# Copy the app
RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
# Netflix credentials
ARG netflix_user 
ARG netflix_pass
ENV NETFLIX_USER $netflix_user
ENV NETFLIX_PASS $netflix_pass
RUN chmod +x wait-for-it.sh