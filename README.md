# Car Workshop FAQ

This project stores 20 realistic car workshop FAQs in JSON and
prints a random one. This data is the single source of truth for an AI assistant that will be built in later tasks.

## Project structure

car-workshop-faq/
│
├── data/
│   └── faqs.json          # Stores 20 car workshop FAQs
├── main.py                # Loads JSON and prints a random FAQ
├── README.md              # Project documentation
└── .gitignore             # Specifies files Git should ignore


## Requirements
- Python 3.9 or newer
- No external libraries needed

## How to run
1. Clone the repository:
   git clone https://github.com/<your-username>/car-workshop-faq.git
   cd car-workshop-faq
2. Run the script:
   python main.py
3. Run it again to see a different random question.

## Example output
[PRICES]
Q: How much does an oil change cost?
A: A standard oil and filter change costs between 45 and 80 USD ...

## Data format
Each entry has: `id`, `category`, `question`, `answer`.