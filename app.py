import http.server
import socketserver
from flask import Flask, render_template
import requests
from tabulate import tabulate

# Fetch JSON data from the API
url = "https://s3.amazonaws.com/open-to-cors/assignment.json"
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse JSON data
    json_data = response.json()

    # Extract relevant information (Subcategory, Title, Price, Popularity) from each product
    products = json_data.get("products", {})

    # Convert product data into a list of dictionaries
    product_list = [{"ID": product_id, "Title": details["title"], "Price": details["price"], "Popularity": details["popularity"]}
                    for product_id, details in products.items()]

    # Sort products based on descending popularity
    sorted_products = sorted(product_list, key=lambda x: int(x["Popularity"]), reverse=True)

    # Prepare data for the HTML template
    headers = ["ID", "Title", "Price", "Popularity"]
    table_data = [[product["ID"], product["Title"], product["Price"], product["Popularity"]] for product in sorted_products]

    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Product Table</title>
    </head>
    <body>
        <h1>Product Table</h1>
        <table border="1">
            <thead>
                <tr>
                    {" ".join(f'<th>{header}</th>' for header in headers)}
                </tr>
            </thead>
            <tbody>
                {" ".join(f'<tr>{" ".join(f"<td>{cell}</td>" for cell in row)}</tr>' for row in table_data)}
            </tbody>
        </table>
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open("index.html", "w") as f:
        f.write(html_content)

    # Use Python's built-in HTTP server to serve the HTML file
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
