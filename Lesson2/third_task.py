def read_sales_data(file_path):
    sales = []

    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            sales.append(
                {
                    "item": parts[0],
                    "price": float(parts[1]),
                    "status": parts[2],
                }
            )

    return sales


def filter_valid_sales(sales):
    return [
        sale
        for sale in sales
        if sale["status"] == "completed" and sale["price"] > 0
    ]


def calculate_total_revenue(sales, discount_rate):
    total_revenue = 0

    for sale in sales:
        discounted_price = sale["price"] * (1 - discount_rate)
        total_revenue += discounted_price

    return total_revenue


def write_report(total_revenue, valid_sales_count, report_file_path):
    report = (
        f"Total Revenue: ${total_revenue:.2f}\n"
        f"Valid Transactions: {valid_sales_count}"
    )

    with open(report_file_path, "w") as file:
        file.write(report)


def send_revenue_notification(total_revenue):
    if total_revenue > 10000:
        print("Sending email to CEO: Target reached!")
    else:
        print("Sending email to Manager: Target not reached.")


def main(file_path, discount_rate):
    sales = read_sales_data(file_path)
    valid_sales = filter_valid_sales(sales)
    total_revenue = calculate_total_revenue(valid_sales, discount_rate)
    write_report(total_revenue, len(valid_sales), "report.txt")
    send_revenue_notification(total_revenue)


if __name__ == "__main__":
    main("sales.csv", 0.1)
