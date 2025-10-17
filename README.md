# Data curation aimed at monitoring global progress towards ending TB

## Overview
This project implements a reproducible end-to-end data curation pipeline to monitor global progress toward ending tuberculosis (TB). It integrates data from WHO, the World Bank, and UNDP.

## UNDP HDI API Key Setup
The UNDP Human Development Index (HDI) dataset requires an API key to access the HDRO Data API.

### Steps to obtain an API key:
1. Navigate to [HDR Data API Subscription](https://hdrdata.org).
2. Click **Subscribe for HDR Data API** and fill out the form.
3. Verify your email through the link sent by HDR.
4. After verification, you will receive your API key via email. Keep it secure.

### Using the API key:
1. Create a `.env` file in the root of this project.
2. Add your API key in the following format:
```HDRO_API_KEY=your_api_key_here```