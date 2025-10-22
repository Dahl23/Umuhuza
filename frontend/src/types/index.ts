export interface User {
  userid: number;
  user_firstname: string;
  user_lastname: string;
  full_name: string;
  email: string;
  phone_number: string;
  user_role: 'buyer' | 'seller' | 'dealer';
  profile_photo: string;
  is_verified: boolean;
  email_verified: boolean;
  phone_verified: boolean;
  date_joined: string;
  badges?: UserBadge[];
}

export interface UserBadge {
  userbadge_id: number;
  badge_type: 'verified' | 'top_dealer' | 'trusted_seller' | 'power_buyer';
  issuedat: string;
  is_active: boolean;
}

export interface Listing {
  listing_id: number;
  listing_title: string;
  list_description: string;
  listing_price: string;
  list_location: string;
  listing_status: 'active' | 'pending' | 'sold' | 'expired' | 'hidden';
  views: number;
  is_featured: boolean;
  createdat: string;
  updatedat: string;
  images: ListingImage[];
  category: Category;
  seller: User;
  is_favorited?: boolean;
}

export interface ListingImage {
  listimage_id: number;
  image_url: string;
  is_primary: boolean;
  display_order: number;
}

export interface Category {
  cat_id: number;
  cat_name: string;
  slug: string;
  cat_description: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  user_firstname: string;
  user_lastname: string;
  email: string;
  phone_number: string;
  password: string;
  password_confirm: string;
}

export interface AuthResponse {
  message: string;
  user: User;
  tokens: {
    access: string;
    refresh: string;
  };
}

export interface ApiError {
  error?: string;
  detail?: string;
  [key: string]: any;
}

export interface Notification {
  notif_id: number;
  notif_title: string;
  notif_message: string;
  notif_type: 'system' | 'chat' | 'report' | 'payment' | 'listing' | 'review' | 'verification';
  link_url?: string;
  is_read: boolean;
  createdat: string;
  read_at?: string;
}

export interface NotificationsResponse {
  unread_count: number;
  unread: Notification[];
  read: Notification[];
}

export interface Report {
  reportmiscond_id: number;
  reporter: User;
  reported_user?: User;
  listing_id?: number;
  report_reason: string;
  report_type: 'spam' | 'fraud' | 'inappropriate' | 'duplicate' | 'harassment' | 'other';
  report_status: 'pending' | 'resolved' | 'rejected';
  createdat: string;
}

export interface ReportCreateData {
  reported_userid?: number;
  listing_id?: number;
  report_type: 'spam' | 'fraud' | 'inappropriate' | 'duplicate' | 'harassment' | 'other';
  report_reason: string;
}

export interface Review {
  ratingrev_id: number;
  reviewer: User;
  rating: number;
  comment?: string;
  createdat: string;
  updatedat: string;
}

export interface ReviewCreateData {
  reviewed_userid: number;
  listing_id?: number;
  rating: number;
  comment?: string;
}

export interface ReviewsResponse {
  average_rating: number;
  total_reviews: number;
  reviews: Review[];
}