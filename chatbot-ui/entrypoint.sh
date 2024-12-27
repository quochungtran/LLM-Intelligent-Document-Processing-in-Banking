#!/bin/bash

mkdir -p /root/.streamlit
cp config.toml /root/.streamlit

streamlit run chat_interface.py --server.port 8051
