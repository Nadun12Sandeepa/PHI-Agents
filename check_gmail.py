"""
Gmail Spam Checker - Quick Start Script
Automatically check your Gmail inbox for spam
"""

import os
from dotenv import load_dotenv
from email_integration import GmailIntegration, check_email_spam

# Load .env file
load_dotenv()

def check_gmail_inbox():
    """
    Check Gmail inbox for unread emails and analyze for spam
    """
    
    print("=" * 80)
    print("📧 GMAIL SPAM DETECTOR")
    print("=" * 80)
    
    # Get credentials from .env
    email_address = os.getenv('GMAIL_EMAIL')
    app_password = os.getenv('GMAIL_PASSWORD')
    
    if not email_address or not app_password:
        print("\n❌ ERROR: Missing credentials in .env file")
        print("\n📋 Setup Instructions:")
        print("1. Go to: https://myaccount.google.com/apppasswords")
        print("2. Select 'Mail' and 'Windows Computer'")
        print("3. Copy the 16-character password")
        print("\n4. Create .env file with:")
        print("   GMAIL_EMAIL=your@gmail.com")
        print("   GMAIL_PASSWORD=xxxx xxxx xxxx xxxx")
        print("\n5. Run this script again!")
        return
    
    # Connect to Gmail
    gmail = GmailIntegration(email_address, app_password)
    
    print(f"\n🔐 Connecting to {email_address}...")
    
    if not gmail.connect():
        print("❌ Failed to connect. Check your credentials.")
        return
    
    # Get unread emails
    print("\n📬 Fetching unread emails...")
    emails = gmail.get_unread_emails(10)  # Get up to 10 unread emails
    
    if not emails:
        print("✅ No unread emails found")
        gmail.close()
        return
    
    print(f"📊 Found {len(emails)} unread email(s)\n")
    
    # Analyze each email
    results = {
        'spam': [],
        'safe': [],
        'error': []
    }
    
    for i, email_data in enumerate(emails, 1):
        print(f"[{i}/{len(emails)}] Analyzing: {email_data['subject'][:60]}...")
        
        try:
            result = check_email_spam(
                email_data['from'],
                email_data['subject'],
                email_data['body']
            )
            
            if result['is_spam']:
                results['spam'].append(result)
                print(f"     🚨 SPAM DETECTED")
            else:
                results['safe'].append(result)
                print(f"     ✅ Safe to open")
                
        except Exception as e:
            print(f"     ⚠️  Error: {str(e)[:50]}")
            results['error'].append(email_data['subject'])
    
    # Close connection
    gmail.close()
    
    # Display summary
    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    
    print(f"\n✅ SAFE ({len(results['safe'])}):")
    if results['safe']:
        for r in results['safe']:
            print(f"   • {r['subject'][:70]}")
    else:
        print("   None")
    
    print(f"\n🚨 SPAM ({len(results['spam'])}):")
    if results['spam']:
        for r in results['spam']:
            print(f"   • {r['subject'][:70]}")
            print(f"     From: {r['sender'][:60]}")
    else:
        print("   None")
    
    if results['error']:
        print(f"\n⚠️  ERRORS ({len(results['error'])}):")
        for subject in results['error']:
            print(f"   • {subject[:70]}")
    
    print("\n" + "=" * 80)
    
    # Recommendation
    if results['spam']:
        print(f"\n⚠️  WARNING: {len(results['spam'])} spam email(s) detected!")
        print("   Move these to your spam folder to keep your inbox clean.")
    else:
        print("\n✅ Great! All unread emails appear to be legitimate.")


if __name__ == "__main__":
    check_gmail_inbox()
