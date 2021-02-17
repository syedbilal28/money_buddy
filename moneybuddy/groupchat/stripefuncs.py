import stripe
from .models import Profile

def CreateCustomer(user):
    customer=stripe.Customer.create(
            email=user.email,
            name=user.get_full_name(),
            metadata={
                'user_id':user.pk,
                'username':user.username
            },
            description="Created from django",
            )
    profile=Profile.objects.get(user=user)
    profile.stripe_customer_id=customer.id
    profile.save()
    return customer

def CreateAccount(user):
    profile=Profile.objects.get(user=user)
    try:
        account= stripe.Account.create(
                            type="custom",
                            country=profile.country,
                            email=user.email,
                            capabilities={
                                "card_payments":{"requested":True},
                                "transfers":{"requested":True}
                            }
                            
                        )
        profile.stripe_account_id=account.id
        profile.save()
    except:
        account=f"Our operations are not currently supported in {profile.country}"
    return account

def CreatePlan(product,thread_price):
    plan=stripe.Plan.create(
            product=product.id,
            nickname='Initial Plan',
            interval='month',
            currency='usd',
            amount=thread_price,
        )
    return plan
def CreatePaymentMethod(card,cvc,exp_month,exp_year):
    Payment_Method=stripe.PaymentMethod.create(
                type="card",
                card={
                    "number":card,
                    "cvc":cvc,
                    'exp_month':exp_month,
                    'exp_year':exp_year
                }
            )
    return Payment_Method