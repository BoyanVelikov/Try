# pip install ccxt
# Here's a simple example of a grid bot script for the BTC/USDT pair:

import ccxt
import time

# Set your API keys
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

# Initialize the exchange
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

symbol = 'BTC/USDT'
grid_range = (20000, 35000)
grid_size = 100
grid_spacing = (grid_range[1] - grid_range[0]) / grid_size

# Generate grid levels
buy_levels = [grid_range[0] + i * grid_spacing for i in range(grid_size)]
sell_levels = [level + grid_spacing for level in buy_levels]

# Set the order size for each level
buy_order_size = 100 / grid_spacing  # Adjust this as needed
sell_order_size = buy_order_size

# Place buy orders
for buy_level in buy_levels:
    try:
        buy_order = exchange.create_limit_buy_order(symbol, buy_order_size, buy_level)
        print(f"Placed buy order: {buy_order}")
    except Exception as e:
        print(f"Error placing buy order at {buy_level}: {e}")

# Place sell orders
for sell_level in sell_levels:
    try:
        sell_order = exchange.create_limit_sell_order(symbol, sell_order_size, sell_level)
        print(f"Placed sell order: {sell_order}")
    except Exception as e:
        print(f"Error placing sell order at {sell_level}: {e}")

# Monitor executed orders
while True:
    try:
        open_orders = exchange.fetch_open_orders(symbol)
        for order in open_orders:
            order_id = order['id']
            order_type = order['side']
            order_price = order['price']

            # Check if the order is executed
            if exchange.fetch_order_status(symbol, order_id) == 'closed':
                print(f"Order executed: {order_type} at {order_price}")

                # Place a new order in the opposite direction
                if order_type == 'buy':
                    new_sell_order = exchange.create_limit_sell_order(symbol, sell_order_size, order_price + grid_spacing)
                    print(f"Placed sell order: {new_sell_order}")
                elif order_type == 'sell':
                    new_buy_order = exchange.create_limit_buy_order(symbol, buy_order_size, order_price - grid_spacing)
                    print(f"Placed buy order: {new_buy_order}")

    except Exception as e:
        print(f"Error monitoring orders: {e}")

    time.sleep(60)  # Adjust the monitoring interval as needed