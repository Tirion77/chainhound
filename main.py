# Load the environment variables
from dotenv import load_dotenv
load_dotenv()

from time import time
import os

from hound_utils import cli_parser

import argparse
from fetcher import fetch_transactions
from analyzer import analyze_transactions
from learning import initialize_db



@cli_parser({
    "--address": {"required": True, "help": "Ethereum address to trace"},
    "--start-block": {"type": int, "required": True, "help": "Starting block"},
    "--end-block": {"type": int, "required": True, "help": "Ending block"},
    "--token": {"help": "Token contract address (optional)"},
    "--chain": {"default": "ethereum", "help": "Chain alias (default: ethereum)"}
})
def main(args):
    
    initialize_db()
    
    # Fetch transactions

    transactions = fetch_transactions(
        address=args.address,
        start_block=args.start_block,
        end_block=args.end_block,
        chain=args.chain,
        api_key=os.getenv('ETHERSCAN_KEY')
,
    )
    # Analyze and trace funds
    report = analyze_transactions(transactions, args.address, args.token)
    
    # Save report
    timestamp = int(time.time())
    report_file = f"reports/{args.address}-{timestamp}.txt"
    with open(report_file, "w") as f:
        f.write(report)
    
    print(f"Report generated: {report_file}")

if __name__ == "__main__":
    main()
