FROM continuumio/miniconda3

# make docker use bash instead of sh
SHELL ["/bin/bash", "--login", "-c"]

# copy all necessary files
COPY environment.yml .
COPY ownchain/blockcoin.py .
COPY entrypoint.sh /usr/local/bin/

# make entrypoint script executable
RUN chmod u+x /usr/local/bin/entrypoint.sh
# create environment
RUN conda env create -f environment.yml

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python", "blockcoin.py", "serve"]
