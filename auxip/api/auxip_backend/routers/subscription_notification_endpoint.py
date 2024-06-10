import datetime

from fastapi import APIRouter

from .. schemas import subscriptions

router = APIRouter()

@router.post("/test/EP/Notification/ProductAvailability", tags=["Notifications"])
async def handle_subscription_notification_product(product_notification: subscriptions.SubscriptionNotification):
   """
   Create a Subscription with the following parameters:

   - **SubscriptionId**: The identifier of the Subscription being notified. Maps to Subscription.Id 
   - **ProductId**: The unique identifier of the product being notified. Maps to Product.Id
   - **ProductName**: The data file name of the product being notified. Maps to Product.Name
   - **NotificationDate**: Date and time at which the notification was generated. Time is in UTC in the format YYYY-MM-DDThh:mm:ss.sssZ
   """
   str_now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
   return [{"ACK": "True"}, {"ReceptionDate": str_now},{"ProductName": product_notification.ProductName}]