
# OCI Generative AI Agent SDK Chat Template

This repository provides a customizable chat application template using Oracle's Generative AI Agent SDK. 
The sample is designed to be flexible, with features for adjusting system prompts, retry logic, and session metadata.

## Features
- Easy-to-modify system prompt for specific use cases.
- Built-in retry logic for error handling.

## Prerequisites
- Python 3.12 or later
- Oracle Cloud account with Generative AI service enabled
- `uv` for managing Python environments

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd oci-genai-agent-sdk-chat-template
   ```

2. Initialize the virtual environment:
   ```bash
   uv --init
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Set up environment variables in `.env`:
   ```env
   OCI_SERVICE_ENDPOINT=https://agent-runtime.generativeai.<region>.oci.oraclecloud.com
   OCI_AGENT_ENDPOINT_ID=ocid1.genaiagentendpoint.oc1.<region>.<unique_id>
   USER_ID=<optional_user_id>
   ```

## Usage
Run the chat application:
```bash
uv run src/oci_genai_chat.py
```

## Adjustable Properties
- **System Prompt**: Customize the behavior and context of the assistant.
- **Retry Logic**: Fine-tune retry attempts and timeouts.
