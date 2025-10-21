import sendgrid
from sendgrid.helpers.mail import Mail
from .config import SENDGRID_API_KEY
import os
import random

def get_sendgrid_client():
    if not SENDGRID_API_KEY or SENDGRID_API_KEY == "your_sendgrid_api_key_here":
        print("WARNING: SendGrid API key not configured. Email sending will be disabled.")
        return None
    return sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

def send_email_sync(to_email: str, subject: str, content: str):
    sg = get_sendgrid_client()
    if not sg:
        print(f"Email sending disabled. Would have sent email to {to_email} with subject: {subject}")
        return None
        
    from_email = "sathishdhuda25@gmail.com"
    
    print(f"Sending email to {to_email} with subject: {subject}")
    
    mail = Mail(from_email=from_email, to_emails=to_email, subject=subject, html_content=content)
    
    try:
        response = sg.send(mail)
        print(f"Email sent successfully to {to_email}. Status code: {response.status_code}")
        return response
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return None

def send_verification_email(to_email: str, verification_token: str):
    """
    Send email verification email to user
    """
    # Get the base URL from environment or use localhost for development
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    verification_link = f"{base_url}/auth/verify-email?token={verification_token}"
    
    subject = "Verify your FairRide account"
    content = f"""
    <html>
    <body>
        <h2>Welcome to FairRide!</h2>
        <p>Thank you for signing up. Please verify your email address by clicking the link below:</p>
        <p><a href="{verification_link}">Verify Email Address</a></p>
        <p>If you didn't create an account with us, you can safely ignore this email.</p>
        <p>Best regards,<br>The FairRide Team</p>
    </body>
    </html>
    """
    
    return send_email_sync(to_email, subject, content)

def send_welcome_email(to_email: str, name: str):
    """
    Send welcome email after successful verification
    """
    subject = "Welcome to FairRide!"
    content = f"""
    <html>
    <body>
        <h2>Welcome to FairRide, {name}!</h2>
        <p>Your email has been successfully verified. You can now log in to your account and start using FairRide.</p>
        <p><a href="http://localhost:8000/docs">Visit our API Documentation</a></p>
        <p>Best regards,<br>The FairRide Team</p>
    </body>
    </html>
    """
    
    return send_email_sync(to_email, subject, content)

def send_otp_email(to_email: str, otp: str):
    """
    Send OTP email to user for login verification
    """
    subject = "FairRide Login Verification Code"
    content = f"""
    <html>
    <body>
        <h2>FairRide Login Verification</h2>
        <p>Your verification code for logging into FairRide is:</p>
        <h1 style="font-size: 32px; color: #1a73e8;">{otp}</h1>
        <p>This code will expire in 30 minutes.</p>
        <p>If you didn't request this code, you can safely ignore this email.</p>
        <p>Best regards,<br>The FairRide Team</p>
    </body>
    </html>
    """
    
    print(f"Generated OTP: {otp} for email: {to_email}")
    return send_email_sync(to_email, subject, content)