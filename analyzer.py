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
            
            destination_param = input("  - Destination Address Parameter (e.g., 'to', 'tx.to'): ").strip()
            value_param = input("  - Value Parameter (e.g., 'value', 'tx.value'): ").strip()
            tx_type = input("  - Type (native_transfer/erc20_transfer/bridge_transfer): ").strip()
            
            new_rule = {
                "type": tx_type,
                "destination": destination_param,
                "value": value_param
            }
            
            save_rule(selector, new_rule)
            continue

        # Extract destination and value based on rule
        if rule["destination"].startswith("tx."):
            destination = tx.get(rule["destination"][3:], None)  # Extract field after 'tx.'
        else:
            destination = None

        if rule["value"].startswith("tx."):
            value = tx.get(rule["value"][3:], None)  # Extract field after 'tx.'
        else:
            value = None

        if destination is None or value is None:
            report.append(f"Error processing transaction: {tx['hash']}, invalid rule or missing data.")
            continue

        report.append(f"Processed transaction: {tx['hash']} -> {destination} ({value})")

    return "\n".join(report)

