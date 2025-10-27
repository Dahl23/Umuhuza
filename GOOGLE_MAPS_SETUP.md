# Google Maps API Setup Guide

## Overview
The location field in listing creation now supports Google Places Autocomplete for better user experience. This feature is **optional** - the platform works without it, but provides manual text input instead.

## Setup Instructions

### 1. Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API**
   - **Places API**
4. Go to "Credentials" and create an API key
5. (Recommended) Restrict the API key:
   - HTTP referrers: Add your domain (e.g., `localhost:5173/*`, `yourdomain.com/*`)
   - API restrictions: Select "Maps JavaScript API" and "Places API"

### 2. Configure Your Application

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Add your API key to `.env`:
   ```
   VITE_GOOGLE_MAPS_API_KEY=your_actual_api_key_here
   ```

3. Restart your development server

### 3. Verify Setup

1. Go to the "Create Listing" page
2. Click on the Location field
3. Start typing a location in Burundi
4. You should see autocomplete suggestions

## Troubleshooting

### Autocomplete Not Working

- **Check browser console** for errors
- **Verify API key** is correctly set in `.env`
- **Ensure APIs are enabled** in Google Cloud Console
- **Check billing** - Google Maps requires billing to be enabled (free tier available)

### "Google Maps JavaScript API not loaded" Warning

- API key not configured or invalid
- Platform will fall back to regular text input
- No functionality is lost, just reduced user experience

## Fallback Behavior

If Google Maps API is not configured:
- Users can still enter locations manually
- A small note appears under the field: "Google Places API not configured. Using manual input"
- All other features work normally

## Cost Considerations

Google Maps Platform offers:
- **$200 free credit per month**
- Places Autocomplete: $2.83 per 1000 requests
- Most small to medium platforms stay within free tier

Learn more: https://cloud.google.com/maps-platform/pricing
