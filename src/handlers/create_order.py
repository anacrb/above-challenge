import os
import json
import boto3
import uuid
from datetime import datetime, timezone
from models import ShoeModel, OrderModel

s3 = boto3.client('s3')
bucket_name = os.environ['INVOICES_BUCKET_NAME']

def handler(event, context):
    try:
        body = json.loads(event['body'])

        print("validation")

        # --- Input Validation ---
        required_fields = ['items', 'shipping', 'username']
        if not all(field in body for field in required_fields):
            return {'statusCode': 400, 'body': 'Missing required fields.'}

        order_items = body['items']
        username = body['username']
        shipping = body['shipping']

        # --- validate shipping ---
        if "address" not in shipping or "zip" not in shipping:
            return {'statusCode': 400, 'body': 'Shipping address not found.'}

        # --- Validate items list ---
        if not isinstance(order_items, list) or not order_items:
            return {'statusCode': 400, 'body': json.dumps('Items must be a non-empty list.')}

        print("validating shipping address")

        validated_shoes = []
        total_price = 0.0
        for item in order_items:

            if 'shoeId' not in item or 'size' not in item:
               return {'statusCode': 400, 'body': json.dumps(f"Invalid item found in order: {item}")}

            shoe_id = item['shoeId']
            selected_size = item['size']
            # --- Business Logic: Validate Size ---
            print("query shoes")
            try:
                shoe = ShoeModel.get(shoe_id)
                print(shoe)
            except ShoeModel.DoesNotExist:
                return {'statusCode': 404, 'body': json.dumps(f"Shoe with ID '{shoe_id}' not found.")}

            if selected_size not in shoe.sizes:
                return {'statusCode': 400, 'body': f'Size {selected_size} not available.'}

            validated_shoes.append(
                {
                    'id': shoe.id,
                    'brand': shoe.brand,
                    'name': shoe.name,
                    'size': selected_size,
                    'price': shoe.price
                }
            )
            total_price += float(shoe.price)

        print("save order")

        # --- Create the Order ---
        new_order = OrderModel(
            orderId=str(uuid.uuid4()),
            username=username,
            items=validated_shoes,
            shipping=shipping,
            totalPrice=total_price,
            createdAt=datetime.now(timezone.utc),
        )
        print(new_order)
        new_order.save()


        # --- Generate and Upload Invoice ---
        invoice = generate_invoice(new_order, validated_shoes, shipping)
        print(invoice)
        invoice_key = f"invoices/{username}/{new_order.orderId}.json"

        print("Invoice key:", invoice_key)

        s3.put_object(
            Bucket=bucket_name,
            Key=invoice_key,
            Body=json.dumps(invoice, indent=2, default=str).encode('UTF-8'),
            ContentType='application/json'
        )
        print("Invoice key:", invoice_key)

        return {
            'statusCode': 201,
            'body': json.dumps({'orderId': new_order.orderId, 'message': 'Order created successfully!'})
        }

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}

def generate_invoice(order, validated_shoes, shipping):

    now = datetime.now(timezone.utc)
    return {
        "invoiceId": f"INV-{now.strftime('%Y%m%d')}-{order.orderId[:8]}",
        "username": order.username,
        "orderId": order.orderId,
        "shoes": validated_shoes,
        "shipping": shipping,
        "total": order.totalPrice,
        "issuedAt": now.isoformat() + "Z"
    }