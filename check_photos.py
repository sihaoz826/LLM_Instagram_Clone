#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SZ: Photo Analysis Script

This script analyzes all photos in the Albumy database to identify:
1. Photos missing descriptions
2. Photos missing alt text
3. Photos with default/fallback alt text

Usage:
    python check_photos.py
"""

import os
import sys
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from albumy import create_app
from albumy.models import Photo, User
from albumy.extensions import db

def check_photos():
    """SZ: Analyze all photos in the database for missing descriptions and alt text"""
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Get all photos
        photos = Photo.query.all()
        
        print("=" * 80)
        print("SZ: PHOTO ANALYSIS REPORT")
        print("=" * 80)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Photos: {len(photos)}")
        print()
        
        # Initialize counters
        missing_description = []
        missing_alt_text = []
        default_alt_text = []
        complete_photos = []
        
        # Analyze each photo
        for photo in photos:
            photo_info = {
                'id': photo.id,
                'filename': photo.filename,
                'author': photo.author.username if photo.author else 'Unknown',
                'timestamp': photo.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'description': photo.description,
                'alt_text': photo.alt_text
            }
            
            # Check for missing description
            if not photo.description or photo.description.strip() == '':
                missing_description.append(photo_info)
            
            # Check for missing alt text
            if not photo.alt_text or photo.alt_text.strip() == '':
                missing_alt_text.append(photo_info)
            
            # Check for default/fallback alt text
            if (photo.alt_text and 
                (photo.alt_text == "empty-alt-text" or 
                 photo.alt_text == "Image description not available" or
                 photo.alt_text == "Photo uploaded by user")):
                default_alt_text.append(photo_info)
            
            # Check for complete photos (have both description and proper alt text)
            if (photo.description and photo.description.strip() != '' and
                photo.alt_text and photo.alt_text.strip() != '' and
                photo.alt_text not in ["empty-alt-text", "Image description not available", "Photo uploaded by user"]):
                complete_photos.append(photo_info)
        
        # Print results
        print("📊 ANALYSIS RESULTS:")
        print("-" * 40)
        print(f"✅ Complete photos (description + alt text): {len(complete_photos)}")
        print(f"❌ Missing descriptions: {len(missing_description)}")
        print(f"❌ Missing alt text: {len(missing_alt_text)}")
        print()
        
        # Show missing descriptions
        if missing_description:
            print("�� PHOTOS MISSING DESCRIPTIONS:")
            print("-" * 40)
            for photo in missing_description:
                print(f"ID: {photo['id']} | Author: {photo['author']} | File: {photo['filename']} | Date: {photo['timestamp']}")
            print()
        
        # Show missing alt text
        if missing_alt_text:
            print("🖼️  PHOTOS MISSING ALT TEXT:")
            print("-" * 40)
            for photo in missing_alt_text:
                print(f"ID: {photo['id']} | Author: {photo['author']} | File: {photo['filename']} | Date: {photo['timestamp']}")
            print()
        
        
        # Summary statistics
        print("�� SUMMARY STATISTICS:")
        print("-" * 40)
        if len(photos) > 0:
            desc_coverage = ((len(photos) - len(missing_description)) / len(photos)) * 100
            alt_coverage = ((len(photos) - len(missing_alt_text)) / len(photos)) * 100
            proper_alt_coverage = ((len(photos) - len(missing_alt_text) - len(default_alt_text)) / len(photos)) * 100
            
            print(f"Description Coverage: {desc_coverage:.1f}%")
            print(f"Alt Text Coverage: {alt_coverage:.1f}%")
            print(f"Proper Alt Text Coverage: {proper_alt_coverage:.1f}%")
            print(f"Complete Photos: {(len(complete_photos) / len(photos)) * 100:.1f}%")
        else:
            print("No photos found in database.")
        
        print()
        print("=" * 80)
        print("Analysis complete!")
        print("=" * 80)

def regenerate_missing_alt_text():
    """SZ: Optionally regenerate alt text for photos that have default/fallback alt text"""
    
    app = create_app()
    
    with app.app_context():
        # Find photos with default alt text
        default_alt_photos = Photo.query.filter(
            Photo.alt_text.in_(["empty-alt-text", "Image description not available", "Photo uploaded by user"])
        ).all()
        
        if not default_alt_photos:
            print("No photos found with default alt text.")
            return


if __name__ == "__main__":
    print("SZ: Albumy Photo Analysis Tool")
    print("=" * 50)
    
    # Run the analysis
    check_photos()
    