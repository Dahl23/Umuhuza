# 📁 File Upload Architecture - Umuhuza Platform

## Overview

This document explains how file uploads (images for listings, documents for dealer applications) work in the Umuhuza platform.

---

## 🖼️ Image Storage System

### Storage Location

**All uploaded files are stored locally on the backend server:**

```
backend/
├── media/                          # Root media directory
│   ├── listings/                   # Listing images
│   │   ├── {listing_id}/          # Organized by listing ID
│   │   │   ├── {uuid}.jpg         # Optimized JPEG images
│   │   │   ├── {uuid}.jpg
│   │   │   └── ...
│   ├── dealer_documents/          # Dealer application documents
│   │   ├── {dealer_app_id}/
│   │   │   ├── business_license.pdf
│   │   │   ├── tax_certificate.pdf
│   │   │   └── ...
│   └── profile_photos/            # User profile photos (future)
│       └── {user_id}/
│           └── avatar.jpg
```

### Image Processing Pipeline

When an image is uploaded:

1. **Validation**
   - File type: Only JPEG, PNG, WebP allowed
   - File size: Maximum 5MB per image
   - Quantity: Maximum 10 images per listing

2. **Optimization**
   - Convert RGBA/P mode to RGB
   - Resize if width > 1920px (maintains aspect ratio)
   - Save as JPEG with 85% quality
   - Apply optimization

3. **Storage**
   - Generate unique filename: `{uuid}.jpg`
   - Save to: `media/listings/{listing_id}/{uuid}.jpg`
   - Store URL in database: `/media/listings/{listing_id}/{uuid}.jpg`

4. **Database Record**
   - Create `ListingImage` record
   - Set first image as primary
   - Assign display order

### Image URLs

**Development:**
```
http://localhost:8000/media/listings/123/abc123def456.jpg
```

**Production:**
```
https://api.umuhuza.bi/media/listings/123/abc123def456.jpg
```

---

## 🔧 Technical Implementation

### Django Settings (`settings.py`)

```python
# Media files (User uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

### URLs Configuration (`umuhuza_api/urls.py`)

For development, add to urls.py:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Image Upload Flow

**Backend Endpoint:** `POST /api/listings/{listing_id}/upload-image/`

```python
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO
import uuid

def upload_listing_image(request, listing_id):
    image_file = request.FILES['image']

    # Open and optimize
    img = Image.open(image_file)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Resize if needed
    if img.width > 1920:
        ratio = 1920 / img.width
        new_height = int(img.height * ratio)
        img = img.resize((1920, new_height), Image.Resampling.LANCZOS)

    # Save optimized
    output = BytesIO()
    img.save(output, format='JPEG', quality=85, optimize=True)
    output.seek(0)

    # Generate filename and save
    filename = f"listings/{listing_id}/{uuid.uuid4().hex}.jpg"
    path = default_storage.save(filename, ContentFile(output.read()))
    url = default_storage.url(path)

    # Create database record
    ListingImage.objects.create(
        listing_id=listing,
        image_url=url,
        is_primary=(existing_count == 0),
        display_order=existing_count
    )
```

### Frontend Upload (`ImageUpload.tsx`)

```typescript
// User selects files via drag-and-drop or file picker
const onDrop = (acceptedFiles: File[]) => {
  // Validate
  const validFiles = acceptedFiles.filter(file => {
    return file.type.startsWith('image/') && file.size <= 5 * 1024 * 1024;
  });

  // Store File objects
  setImages([...images, ...validFiles]);

  // Create local previews
  validFiles.forEach(file => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviews(prev => [...prev, e.target.result]);
    };
    reader.readAsDataURL(file);
  });
};

// On form submit
const onSubmit = (data) => {
  const formData = new FormData();
  formData.append('listing_title', data.title);
  // ... other fields

  // Append all images
  images.forEach(image => {
    formData.append('images', image);
  });

  // Send to backend
  await listingsApi.create(formData);
};
```

---

## 📦 Production Considerations

### Current Setup (Development)
- ✅ Files stored on local backend server
- ✅ Served by Django development server
- ⚠️ **Not suitable for production**

### Production Options

#### Option 1: Local Storage with Web Server (nginx)

**Setup nginx to serve media files:**

```nginx
server {
    location /media/ {
        alias /path/to/backend/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

**Pros:**
- Simple setup
- No additional costs
- Fast for local users

**Cons:**
- Limited scalability
- No CDN benefits
- Backup complexity

#### Option 2: Cloud Storage (Recommended for Production)

**AWS S3 / DigitalOcean Spaces / Cloudinary**

Install django-storages:
```bash
pip install django-storages boto3
```

Configure settings:
```python
# Use S3 for media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'umuhuza-media'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
```

**Pros:**
- Scalable
- CDN integration
- Automatic backups
- Global availability

**Cons:**
- Monthly costs ($5-50/month depending on usage)
- External dependency

#### Option 3: Cloudinary (Easiest for Images)

```bash
pip install cloudinary
```

```python
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name='your_cloud_name',
    api_key='your_api_key',
    api_secret='your_api_secret'
)

# Upload
result = cloudinary.uploader.upload(image_file)
image_url = result['secure_url']
```

**Pros:**
- Built-in image optimization
- Automatic transformations
- CDN included
- Free tier: 25GB storage, 25GB bandwidth

**Cons:**
- Vendor lock-in
- Costs scale with usage

---

## 🏢 Dealer Application Documents

### Document Upload Flow

**Current Status:** Placeholder implementation

**Backend Endpoint:** `POST /api/dealer-applications/documents/`

```python
{
  "doc_type": "business_license",  # or "tax_certificate", "id_front", "id_back"
  "file_url": "path/to/file.pdf"  # Will be actual file upload
}
```

**To Implement Proper Document Upload:**

1. **Update Backend View:**

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dealer_document_upload(request):
    application = DealerApplication.objects.get(userid=request.user)

    if 'document' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)

    doc_file = request.FILES['document']
    doc_type = request.data.get('doc_type')

    # Validate file type (PDF, JPG, PNG)
    allowed_types = ['application/pdf', 'image/jpeg', 'image/png']
    if doc_file.content_type not in allowed_types:
        return Response({'error': 'Invalid file type'}, status=400)

    # Generate filename
    ext = doc_file.name.split('.')[-1]
    filename = f"dealer_documents/{application.dealerapp_id}/{doc_type}.{ext}"

    # Save file
    path = default_storage.save(filename, doc_file)
    url = default_storage.url(path)

    # Create record
    DealerDocument.objects.create(
        dealerapp_id=application,
        doc_type=doc_type,
        file_url=url
    )

    return Response({'message': 'Document uploaded', 'url': url})
```

2. **Frontend Component:**

```typescript
// In DealerApplicationPage
const [documents, setDocuments] = useState({
  business_license: null,
  tax_certificate: null,
});

const handleDocumentUpload = async (docType, file) => {
  const formData = new FormData();
  formData.append('document', file);
  formData.append('doc_type', docType);

  await dealerApplicationsApi.uploadDocument(formData);
};
```

---

## 🔒 Security Considerations

### File Validation
- ✅ File type whitelist (no executables)
- ✅ File size limits (5MB per image)
- ✅ Quantity limits (10 images per listing)
- ✅ Ownership verification

### Potential Improvements
- [ ] Virus scanning (ClamAV integration)
- [ ] Content-based file type validation (not just extension)
- [ ] Rate limiting on uploads
- [ ] User storage quotas
- [ ] Automatic EXIF data stripping (privacy)

---

## 📊 Storage Usage Monitoring

### Calculate Total Storage

```python
import os
from pathlib import Path

def get_directory_size(path):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += get_directory_size(entry.path)
    return total

# In Django shell
from pathlib import Path
from django.conf import settings

media_path = settings.MEDIA_ROOT
size_bytes = get_directory_size(media_path)
size_mb = size_bytes / (1024 * 1024)
size_gb = size_mb / 1024

print(f"Total media storage: {size_gb:.2f} GB")
```

### Monitor Per User

```python
from listings.models import Listing, ListingImage
from django.db.models import Count

# Users with most images
users_by_images = Listing.objects.values('userid__full_name').annotate(
    total_images=Count('listingimage')
).order_by('-total_images')[:10]
```

---

## 🚀 Migration Guide: Local Storage → Cloud Storage

When ready to move to production:

### Step 1: Install and Configure

```bash
pip install django-storages boto3
```

```python
# settings.py
if not DEBUG:  # Production only
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # ... S3 config
else:  # Development
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
```

### Step 2: Migrate Existing Files

```python
# management/commands/migrate_to_s3.py
from django.core.management.base import BaseCommand
from listings.models import ListingImage
import boto3
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        s3 = boto3.client('s3')

        for image in ListingImage.objects.all():
            # Get local file
            local_path = image.image_url.replace('/media/', 'media/')

            if os.path.exists(local_path):
                # Upload to S3
                s3_key = image.image_url.replace('/media/', '')
                s3.upload_file(
                    local_path,
                    'umuhuza-media',
                    s3_key,
                    ExtraArgs={'ACL': 'public-read'}
                )

                # Update URL
                image.image_url = f'https://umuhuza-media.s3.amazonaws.com/{s3_key}'
                image.save()

                self.stdout.write(f'Migrated: {image.listimage_id}')
```

Run migration:
```bash
python manage.py migrate_to_s3
```

---

## 📝 Quick Reference

### File Limits
- **Image Size**: 5MB max per image
- **Image Dimensions**: Auto-resized to max 1920px width
- **Images per Listing**: 10 max
- **Supported Formats**: JPEG, PNG, WebP (converted to JPEG)

### Storage Paths
- **Listing Images**: `media/listings/{listing_id}/{uuid}.jpg`
- **Dealer Docs**: `media/dealer_documents/{app_id}/{doc_type}.{ext}`
- **Profile Photos**: `media/profile_photos/{user_id}/avatar.jpg`

### API Endpoints
- `POST /api/listings/create/` - Create listing with images
- `POST /api/listings/{id}/upload-image/` - Add image to existing listing
- `POST /api/dealer-applications/documents/` - Upload dealer documents

---

## 🛠️ Troubleshooting

### Images not appearing?
1. Check `MEDIA_ROOT` exists: `ls -la backend/media/`
2. Verify URL configuration in urls.py (development)
3. Check file permissions: `chmod -R 755 backend/media/`

### Upload failing?
1. Check file size < 5MB
2. Verify file type is image/*
3. Check disk space: `df -h`
4. Review Django logs for errors

### Production images not loading?
1. Configure nginx to serve /media/
2. Or use cloud storage (S3, Cloudinary)
3. Check CORS settings if using separate domain

---

**Last Updated:** 2025-01-22
**Maintained By:** Umuhuza Development Team
