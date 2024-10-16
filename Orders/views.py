import json
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from Orders.models import Product, Order
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from customer.models import Customer
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer_id = request.user.id
            product_id = data['product_id']
            quantity = data['quantity']

            if not customer_id or not product_id or quantity is None:
                logger.error(f"Missing required fields: customer_id={customer_id}, product_id={product_id}, quantity={quantity}")
                return JsonResponse({'status': 'Missing required fields'}, status=400)


            product = get_object_or_404(Product,id=product_id)
            customer = get_object_or_404(Customer,id=customer_id)

            if product.stock >= quantity:
                order = Order.objects.create(customer=customer, product=product, quantity=quantity)
                if order_processing(customer,product, quantity):
                    product.stock -= quantity
                    product.save()
                    order.status = 'Paid'
                    order.save()
                    send_email(order.id,customer.email,quantity,product.name,quantity*product.price,customer.balance)
                    return JsonResponse({'status': 'Order Completed Successfully...'})
                else:
                    logger.warning("Insufficient balance for customer_id=%s, required_balance=%s", customer_id,
                                   quantity * product.price)
                    return JsonResponse({'status': 'Insufficient balance...'})
            else:
                logger.warning("Stock unavailable for product_id=%s, requested_quantity=%s, available_stock=%s",
                               product_id, quantity, product.stock)
                return JsonResponse({'status': f'Stock unavailable ...,there is only {product.stock} available.'})
        except json.JSONDecodeError:
            logger.error("Invalid JSON format")
            return JsonResponse({'status': 'Invalid JSON format'}, status=400)

        except Exception as e:
            logger.exception("Unexpected error occurred: %s", e)
            return JsonResponse({'status': 'An unexpected error occurred.'}, status=500)
    logger.warning("Invalid request method: %s", request.method)
    return JsonResponse({'status': 'Invalid request method'}, status=400)


def order_processing(customer,product,quantity):
    total_price = quantity*product.price
    if customer.balance >= total_price:
        customer.balance -= quantity*product.price
        customer.save()
        return True
    return False


def send_email(order_id,email,quantity,product,total_price,balance):
    email_user = 'modebeboo.20002@gmail.com'
    email_password = 'xmijylmvvjsdncba'
    email_send = f'{email}'

    subject = 'Order confirmation'

    html_message = render_to_string('order_confirmation_email.html', {
        'customer_name': email.split('@')[0],  # Assuming customer name is the email prefix
        'order_id': order_id,
        'product_name': product,
        'quantity': quantity,
        'total_price': total_price,
        'remaining_balance': balance,
    })
    plain_message = strip_tags(html_message)

    msg = MIMEMultipart()
    msg['From'] = "Ordering System"
    msg['To'] = email_send
    msg['Subject'] = subject
    msg.attach(MIMEText(html_message,'html'))

    #body = f"Order#: {order_id} \nQuantity: {quantity}\nProduct: {product}\nTotal price: {total_price}.\nRemaining balance is {balance} "
    #msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, email_send, text)
        server.quit()
        logger.info("Email sent successfully to %s", email_send)
    except Exception as e:
        logger.error("Failed to send email: %s", e)
    # return JsonResponse({"message": "Password reset email sent."})



def get_all_customers(request):
    customers = list(Customer.objects.values('id', 'username', 'email', 'balance'))
    return JsonResponse({'customers': customers})

def get_all_products(request):
    products = list(Product.objects.values('id', 'name', 'price','stock'))
    return JsonResponse({'customer': products})


# git add .
# git commit -m "Initial commit"
# git push -u origin master
