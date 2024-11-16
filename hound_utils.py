import argparse

def cli_parser(arguments):
    def decorator(func):
        def wrapper(*args, **kwargs):
            parser = argparse.ArgumentParser(description="Ethereum Funds Tracing CLI")
            for arg, options in arguments.items():
                parser.add_argument(arg, **options)
            args = parser.parse_args()
            return func(args)
        return wrapper
    return decorator

@cli_parser({
    "--address": {"required": True, "help": "Ethereum address to trace"},
    "--start-block": {"type": int, "required": True, "help": "Starting block"},
    "--end-block": {"type": int, "required": True, "help": "Ending block"},
    "--token": {"help": "Token contract address (optional)"},
    "--chain": {"default": "ethereum", "help": "Chain alias (default: ethereum)"}
})
def main(args):
    print(f"Tracing address {args.address} on {args.chain} from block {args.start_block} to {args.end_block}")
