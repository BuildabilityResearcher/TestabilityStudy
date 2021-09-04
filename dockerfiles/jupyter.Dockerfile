FROM jupyter/minimal-notebook

RUN pip install --upgrade pip

COPY notebooks/requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /home/notebooks/

CMD ["jupyter-notebook", "--notebook-dir=/home/jovyan/work/", "--ip='0.0.0.0'", "--port=8888","--NotebookApp.token=''","--allow-root"]

# BUILD docker build -f dockerfiles/jupyter.Dockerfile -t jupyter-bugs:v2 .
# RUN docker run -d --rm --name jupyter-bugs-v2 -p 8888:8888 -v $PWD:/home/jovyan/work/ -w /home/jovyan/work/ jupyter-bugs:v2