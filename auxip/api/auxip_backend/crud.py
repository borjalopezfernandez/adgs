import json
# DB CRUD function
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from uuid import UUID

from . models import subscriptions as models
from . schemas import subscriptions as schemas
from . import schemas
from .logger import logger


def get_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subscription).offset(skip).limit(limit).all()

# -----------------------------------------------------------------------------

def create_subscription(db: Session, subscription: schemas.subscriptions.SubscriptionCreate):
    logger.debug("create_subscription: Id                      => {}".format(subscription.Id))
    logger.debug("create_subscription: Id                      => {}".format(subscription.Id))
    logger.debug("create_subscription: Status                  => {}".format(subscription.Status))
    logger.debug("create_subscription: NotificationEndpoint    => {}".format(subscription.NotificationEndpoint))
    logger.debug("create_subscription: NotificationEpUsername  => {}".format(subscription.NotificationEpUsername))
    logger.debug("create_subscription: NotificationEpPassword  => {}".format(subscription.NotificationEpPassword))
    logger.debug("create_subscription: LastNotificationDate    => {}".format(subscription.LastNotificationDate))

    db_subscription = models.Subscription(
        Id                          = subscription.Id,
        Status                      = subscription.Status,
        FilterParam                 = subscription.FilterParam,
        NotificationEndpoint        = subscription.NotificationEndpoint,
        NotificationEpUsername      = subscription.NotificationEpUsername,
        NotificationEpPassword      = subscription.NotificationEpPassword,
        SubmissionDate              = subscription.SubmissionDate,
        LastNotificationDate        = subscription.LastNotificationDate,
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

# -----------------------------------------------------------------------------

def get_subscription(db: Session, subscription_id: schemas.subscriptions.SubscriptionId):
    logger.debug("get_subscription: Id (input)              => {}".format(subscription_id.Id))
    result = db.query(models.Subscription).filter(models.Subscription.Id == subscription_id.Id).first()
    logger.debug(f"get_subscription: Id                      => {result.Id}")
    logger.debug(f"get_subscription: Status                  => {result.Status}")
    logger.debug(f"get_subscription: NotificationEndpoint    => {result.NotificationEndpoint}")
    logger.debug(f"get_subscription: NotificationEpUsername  => {result.NotificationEpUsername}")
    logger.debug(result)
    return result

# -----------------------------------------------------------------------------

def get_subscription_list_id(db: Session):
    logger.debug("get_subscription_list_id")
    return db.query(models.Subscription.Id).all()
    
# -----------------------------------------------------------------------------

def update_subscription_status(db: Session, subscription_status: schemas.subscriptions.SubscriptionStatus):
    logger.debug("update_subscription: Id                     => {}".format(subscription_status.Id))
    logger.debug("update_subscription: Status                 => {}".format(subscription_status.Status))
    db_subscription = db.query(models.Subscription).filter(models.Subscription.Id == subscription_status.Id).update({models.Subscription.Status: subscription_status.Status})
    db.commit()
    db.flush()
    return db_subscription

# -----------------------------------------------------------------------------

def create_subscription_notification_product(db: Session, notification: schemas.subscriptions.SubscriptionNotificationDB):
    logger.debug("create_subscription_notification_product: NotificationSuccess     => {}".format(notification.NotificationSuccess))
    logger.debug("create_subscription_notification_product: NotificationInfo        => {}".format(notification.NotificationInfo))
    logger.debug("create_subscription_notification_product: SubscriptionId          => {}".format(notification.SubscriptionId))
    logger.debug("create_subscription_notification_product: ProductId               => {}".format(notification.ProductId))
    logger.debug("create_subscription_notification_product: ProductName             => {}".format(notification.ProductName))
    logger.debug("create_subscription_notification_product: NotificationDate        => {}".format(notification.NotificationDate))

    db_subscription_notification = models.SubscriptionNotification(
        NotificationDate        = notification.NotificationDate,
        NotificationSuccess     = notification.NotificationSuccess,
        NotificationInfo        = notification.NotificationInfo,
        SubscriptionId          = notification.SubscriptionId,
        ProductId               = notification.ProductId,
        ProductName             = notification.ProductName,
    )
    
    db.add(db_subscription_notification)
    db.commit()
    db.flush()
    return db_subscription_notification

# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------

def create_product(db: Session, product: schemas.subscriptions.ProductCreate):
    logger.debug("create_product: {}".format(product.Name))
    db_product = sub.Product(
        Name=product.Name,
        ContentType=product.ContentType,
        ContentLength=product.ContentLength,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# -----------------------------------------------------------------------------
