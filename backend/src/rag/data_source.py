TOPICS = ["market_trends", 
          "interest_rate", 
          "eligibility", 
          "financial_choice", 
          "refinancing"]

DATA_URL = {
    "interest_rate" : [
      "https://www.cnet.com/personal-finance/mortgage-rate-predictions-holiday-week-brings-higher-rates/",
      "https://finance.yahoo.com/news/15-countries-highest-mortgage-rates-210146206.html"
    ],
    "market_trends" : ["https://www.linkedin.com/pulse/2024-mortgage-market-review-key-insights-trends-shaped-year-kexwe/",
                      "https://themortgagereports.com/116167/2024-housing-market-recap",
                      "https://www.bankrate.com/real-estate/housing-trends/",
                      # "https://www.freddiemac.com/research/forecast/20241126-us-economy-remains-resilient-with-strong-q3-growth#spotlight",
                      "/home/quochungtran/Desktop/ML_project/LLM_project/data/pdf/cfpb_2023-mortgage-market-activity-and-trends_2024-12.pdf"
                    ],
    "eligibility" : [
        "https://www.lendingtree.com/home/mortgage/minimum-mortgage-requirements/",
        "https://www.americanexpress.com/en-us/credit-cards/credit-intel/how-to-qualify-for-a-home-loan/",
        "https://www.hdfc.com/blog/home-finance/understanding-home-loan-eligibility#:~:text=1.,Your%20overall%20personal%20profile%20viz.",
    ],
    "financial_choice": [
      "https://agrimhfc.com/home-loan-balance-transfer-or-top-up-loan/",
      "https://agrimhfc.com/home-loan-under-construction-property-benefits/",
      "https://agrimhfc.com/home-loan-or-renting-which-is-the-right-financial-choice-for-you/"
    ],
    "refinancing": [
        "https://www.athena.com.au/learn/requirements-for-home-loan-refinancing",
        "https://www.investopedia.com/mortgage/refinance/when-and-when-not-to-refinance-mortgage/#:~:text=Since%20refinancing%20can%20cost%20between,when%20it's%20better%20to%20wait."
    ]
}
