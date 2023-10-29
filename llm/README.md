# LLM App

## Details
The llm app defines the prompting mechanism for Bruno. Specifically, views.py defines the view for prompting Bruno, while utils.py defines the function for calling the model.

## LLM Function
The open source version of Ai4Collab-Bruno will prompt OpenAI's API directly. It should be noted that references to "Middlesight" may be seen. This is a seperate proxy to GPT with additional functionality of rate limits and error visibility. See ProxyGPT for a lightweight version of this proxy: https://github.com/Bklieger/ProxyGPT
