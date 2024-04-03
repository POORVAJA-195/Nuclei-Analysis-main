import json

#list of products that have not null shodan queries 
def save_products_with_non_null_shodan_queries(filename_in, filename_out):
    try:
        with open(filename_in, 'r') as file:
            existing_details = json.load(file)
    except FileNotFoundError:
        print("Input file not found.")
        return

    vendors = existing_details.get("vendors", {})
    products_with_non_null_shodan = []

    for vendor, vendor_details in vendors.items():
        products = vendor_details.get("products", [])
        for product in products:
            shodan_queries = product.get("shodan_queries")
            if shodan_queries:
                product_details = f"Product - {product['product']}\nShodan Queries - {', '.join(shodan_queries)}\n\n"
                products_with_non_null_shodan.append(product_details)

    try:
        with open(filename_out, 'w') as file_out:
            file_out.writelines(products_with_non_null_shodan)
        print("Products with non-null Shodan queries saved to", filename_out)
    except IOError:
        print("Error saving to file.")

# Example usage:
save_products_with_non_null_shodan_queries("output_details_1(unique_shodan_queries).txt", "not_null_shodan_queries.txt")
