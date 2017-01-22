from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()
#secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

# class Inventory(Base):
#     __tablename__ = 'inventory'
#     id = Column(Integer, primary_key=True)
#     product_id = Column(Integer, ForeignKey('product.id'))
#     quantity = Column(Integer)
#     last_filled = Column(DateTime, default=func.now())
#     product = relationship("Product", back_populates="inventory")


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    address = Column(String(255))
    email = Column(String(255), unique=True)
    shoppingCart = relationship("ShoppingCart", uselist=False, back_populates="customer")
    photo = Column(String(255), unique=True)
    password_hash = Column(String(255))
    orders = relationship("Order", back_populates="customer")

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def set_photo(self, photo):
        self.photo = photo

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class ShoppingCart(Base):
    __tablename__ = 'shoppingCart'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", back_populates="shoppingCart")
    products = relationship("ShoppingCartAssociation", back_populates="shoppingCart")

class OrdersAssociation(Base):
    __tablename__ = 'OrdersAssociation'
    order_id = Column(Integer, ForeignKey('order.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    product_qty = Column(Integer)
    product = relationship("Product", back_populates="orders")
    order = relationship("Order", back_populates="products")

class ShoppingCartAssociation(Base):
    __tablename__ = 'shoppingCartAssociation'
    shopping_cart_id = Column(Integer, ForeignKey('shoppingCart.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    quantity = Column(Integer)
    product = relationship("Product", back_populates="shoppingCarts")
    shoppingCart = relationship("ShoppingCart", back_populates="products")

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    total = Column(Float)
    timestamp = Column(DateTime, default=func.now())
    confirmation = Column(String, unique=True)
    products = relationship("OrdersAssociation", back_populates="order")
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", back_populates="orders")

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    photo = Column(String)
    price = Column(Float)
    #inventory = relationship("Inventory", uselist=False, back_populates="product")
    orders = relationship("OrdersAssociation", back_populates="product")
    shoppingCarts = relationship("ShoppingCartAssociation", back_populates="product")


engine = create_engine('sqlite:///fizzBuzz.db')


Base.metadata.create_all(engine)
