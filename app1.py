from app import app, db  # Make sure you're correctly importing app and db

# Create an application context before calling db.create_all()
with app.app_context():
    db.create_all()

print("Database tables created successfully!")
