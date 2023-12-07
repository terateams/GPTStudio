
       ______  _______   _________   ______    _                  __   _          
     .' ___  ||_   __ \ |  _   _  |.' ____ \  / |_               |  ] (_)         
    / .'   \_|  | |__) ||_/ | | \_|| (___ \_|`| |-'__   _    .--.| |  __   .--.   
    | |   ____  |  ___/     | |     _.____`.  | | [  | | | / /'`\' | [  |/ .'`\ \ 
    \ `.___]  |_| |_       _| |_   | \____) | | |, | \_/ |,| \__/  |  | || \__. | 
     `._____.'|_____|     |_____|   \______.' \__/ '.__.'_/ '.__.;__][___]'.__.'  
                                                                                  
            
# GPTStudio

GPTStudio is a library of tools based on GPT (Generative Pre-trained Transformer).
It is designed to provide developers and data scientists with powerful and easy-to-use GPT capabilities.
It combines knowledge base management, GPT capabilities, and a collection of AI-based tools to make it 
a powerful and easy-to-use tool for anyone involved in AI and big data.
making it ideal for any project involving AI and big models.
    
## Key Features
    
### Knowledge base retrieval:
    
Provides an efficient search tool to help users quickly find relevant information in the knowledge base.
    
### GPT Proficiency Test

- **Model Capability Testing**: Allows users to test the performance and capability of GPT models with the assistance of the knowledge base.
- **Real-time Feedback**: Provides real-time feedback to help users understand the response and accuracy of the model.
    
### AI Tools Collection

- **A wide range of AI tools**: including but not limited to text generation, language understanding, data analysis and many other AI-related tools.
- **Large Model Support**: Supports integration with other large AI models to extend the capability and scope of the application.

## Quick Start

### docker-compose

> Use the .env environment variable file or configure docker-compose.yml

```yaml
version: "3"
services:
  gptstudio:
    container_name: "gptstudio"
    image: talkincode/gptstudio:latest
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
    environment:
        - GPT_SERVICE_ADDRESS=${GPT_SERVICE_ADDRESS}
        - GPT_SERVICE_TOKEN=${GPT_SERVICE_TOKEN}
        - OPENAI_API_TYPE=${OPENAI_API_TYPE}
        - OPENAI_API_KEY=${OPENAI_API_KEY}
        - AZURE_OPENAI_API_VERSION=${AZURE_OPENAI_API_VERSION}
        - AZURE_OPENAI_API_BASE=${AZURE_OPENAI_API_BASE}
        - AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
        - MSAL_TENANTID=${MSAL_TENANTID}
        - MSAL_APPID=${MSAL_APPID}
        - DATA_DIR=/data
    volumes:
      - gptstudio-volume:/data
    ports:
      - "8898:80"
    command: ["streamlit","run", "/GPTStudio.py"]
    networks:
      gptstudio_network:

networks:
  gptstudio_network:

volumes:
  gptstudio-volume:
```

## Contribute

We welcome contributions of any kind, including but not limited to issues, pull requests, documentation, examples, etc.
