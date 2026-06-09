import os

class Config:
    # Configuration PostgreSQL locale
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/devops_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '28f218fd66fbffb35db4dff88b9628d1a88fa17856f22c9fe811b01bed614ea0304e3bef8cbcddf39084898378af8cd5b2e406e82d6269c067ef95e1ec0bf038'

class DockerConfig(Config):
    # Configuration pour Docker Compose
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/devops_db'