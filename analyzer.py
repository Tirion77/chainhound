from learning import get_rule, save_rule

def analyze_transactions(transactions, address, token):
    report = []
    for tx in transactions:
        selector = tx.get("input", "")[:10]  # Extract function selector
        rule = get_rule(selector)
        
        if not rule:
            print(f"Unknown transaction detected:")
            print(f"  - Hash: {tx['hash']}")
            print(f"  - Input Data: {tx['input']}")
            print()
            
            destination_param = input("  - Destination Address Parameter (e.g., to, tx.to): ").strip()
            value_param = input("  - Value Parameter (e.g., amount, tx.value): ").strip()
            tx_type = input("  - Type (native_transfer/erc20_transfer/bridge_transfer): ").strip()
            
            new_rule = {
                "type": tx_type,
                "destination": destination_param,
                "value": value_param
            }
            
            save_rule(selector, new_rule)
            continue

        # Apply rule to process transaction
        destination = eval(rule["destination"], {}, {"tx": tx})
        value = eval(rule["value"], {}, {"tx": tx})
        report.append(f"Processed transaction: {tx['hash']} -> {destination} ({value})")

    return "\n".join(report)
