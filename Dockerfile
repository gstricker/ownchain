FROM continuumio/miniconda3

# create environment
COPY environment.yml .
RUN conda env create -f environment.yml

make run command use the ownchain environment
SHELL ["conda", "run", "-n", "ownchain", "/bin/bash", "-c"]

# run server instance
COPY ownchain/blockcoin.py .
ENTRYPOINT ["conda", "run", "-n", "ownchain", "python", "blockcoin.py", "serve"


