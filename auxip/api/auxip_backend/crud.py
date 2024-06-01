# DB CRUD function

from sqlalchemy.orm import Session
from uuid import UUID

from . import models, schemas


def create_database():
    SQLALCHEMY_DATABASE_URL = "postgresql://adgs:adg$#5432@127.0.0.1/adgs_db"
    engine                  = create_engine(SQLALCHEMY_DATABASE_URL)
    models.Base.metadata.create_all(bind=engine)
# logger.debug("Creating database => models.Base.metadata.create_all(bind=engine)")

def get_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subscription).offset(skip).limit(limit).all()

# -----------------------------------------------------------------------------

def create_subscription(db: Session, subscription: schemas.SubscriptionCreate):
    print("create_subscription: Id                      => {}".format(subscription.Id))
    print("create_subscription: Status                  => {}".format(subscription.Status))
    print("create_subscription: NotificationEndpoint    => {}".format(subscription.NotificationEndpoint))
    print("create_subscription: NotificationEpUsername  => {}".format(subscription.NotificationEpUsername))
    print("create_subscription: NotificationEpPassword  => {}".format(subscription.NotificationEpPassword))
    print("create_subscription: LastNotificationDate    => {}".format(subscription.LastNotificationDate))

    db_subscription = models.Subscription(
        Id=subscription.Id,
        Status=subscription.Status,
        FilterParam=subscription.FilterParam,
        NotificationEndpoint=subscription.NotificationEndpoint,
        NotificationEpUsername=subscription.NotificationEpUsername,
        NotificationEpPassword=subscription.NotificationEpPassword,
        SubmissionDate=subscription.SubmissionDate,
        LastNotificationDate=subscription.LastNotificationDate,
    )
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

# -----------------------------------------------------------------------------

def get_subscription(db: Session, subscription_id: schemas.SubscriptionId):
    print("get_subscription: Id (input)              => {}".format(subscription_id.Id))
    result = db.query(models.Subscription).filter(models.Subscription.Id == subscription_id.Id).first()
    print(f"get_subscription: Id                      => {result.Id}")
    print(f"get_subscription: Status                  => {result.Status}")
    print(f"get_subscription: NotificationEndpoint    => {result.NotificationEndpoint}")
    print(f"get_subscription: NotificationEpUsername  => {result.NotificationEpUsername}")
    return result

# -----------------------------------------------------------------------------

def update_subscription_status(db: Session, subscription_status: schemas.SubscriptionStatus):
    print("update_subscription: Id                     => {}".format(subscription_status.Id))
    print("update_subscription: Status                 => {}".format(subscription_status.Status))
    db_subscription = db.query(models.Subscription).filter(models.Subscription.Id == subscription_status.Id).update({models.Subscription.Status: subscription_status.Status})
    db.commit()
    db.flush()
    return db_subscription

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------


def create_product(db: Session, product: schemas.ProductCreate):
    print("create_product: {}".format(product.Name))
    db_product = models.Product(
        Name=product.Name,
        ContentType=product.ContentType,
        ContentLength=product.ContentLength,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# -----------------------------------------------------------------------------
