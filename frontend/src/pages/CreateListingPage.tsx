import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import toast from 'react-hot-toast';
import { listingsApi } from '../api/listings';
import Layout from '../components/layout/Layout';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import ImageUpload from '../components/listings/ImageUpload';
import LoadingSpinner from '../components/common/LoadingSpinner';
import LocationInput from '../components/common/LocationInput';
import { Plus, ArrowLeft, AlertCircle } from 'lucide-react';
import { useAuthStore } from '../store/authStore';

interface ListingFormData {
  cat_id: number;
  listing_title: string;
  list_description: string;
  listing_price: number;
  list_location: string;
}

const schema = yup.object({
  cat_id: yup.number().required('Category is required').min(1, 'Please select a category'),
  listing_title: yup.string()
    .required('Title is required')
    .min(10, 'Title must be at least 10 characters')
    .max(100, 'Title must be less than 100 characters'),
  list_description: yup.string()
    .required('Description is required')
    .min(50, 'Description must be at least 50 characters')
    .max(2000, 'Description must be less than 2000 characters'),
  listing_price: yup.number()
    .required('Price is required')
    .min(1, 'Price must be greater than 0')
    .typeError('Price must be a number'),
  list_location: yup.string()
    .required('Location is required')
    .min(3, 'Location must be at least 3 characters'),
});

export default function CreateListingPage() {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const [images, setImages] = useState<File[]>([]);
  const [currentStep, setCurrentStep] = useState(1);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<ListingFormData>({
    resolver: yupResolver(schema),
  });

  // Fetch categories
  const { data: categories, isLoading: categoriesLoading } = useQuery({
    queryKey: ['categories'],
    queryFn: listingsApi.getCategories,
  });

  // Fetch current subscription
  const { data: subscriptionData } = useQuery({
    queryKey: ['current-subscription'],
    queryFn: listingsApi.getCurrentSubscription,
    enabled: !!user,
  });

  const subscription = subscriptionData?.subscription;
  const hasQuota = subscription ? subscription.remaining_listings > 0 : true;

  // Create listing mutation
  const createMutation = useMutation({
    mutationFn: async (data: ListingFormData) => {
      const formData = new FormData();
      formData.append('cat_id', data.cat_id.toString());
      formData.append('listing_title', data.listing_title);
      formData.append('list_description', data.list_description);
      formData.append('listing_price', data.listing_price.toString());
      formData.append('list_location', data.list_location);

      // Add images
      images.forEach((image) => {
        formData.append('images', image);
      });

      return listingsApi.create(formData);
    },
    onSuccess: (data) => {
      toast.success('Listing created successfully!');
      navigate(`/listings/${data.listing_id}`);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Failed to create listing');
    },
  });

  const onSubmit = (data: ListingFormData) => {
    if (images.length === 0) {
      toast.error('Please upload at least one image');
      return;
    }
    createMutation.mutate(data);
  };

  const watchedValues = watch();
  const canProceedToStep2 = watchedValues.cat_id && watchedValues.listing_title && watchedValues.listing_price && watchedValues.list_location;
  const canProceedToStep3 = canProceedToStep2 && watchedValues.list_description;

  if (categoriesLoading) {
    return (
      <Layout>
        <div className="flex justify-center py-20">
          <LoadingSpinner size="lg" text="Loading..." />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="w-5 h-5" />
            Back
          </button>
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Plus className="w-8 h-8 text-primary-600" />
            Create New Listing
          </h1>
          <p className="text-gray-600 mt-2">
            Fill in the details to create your listing
          </p>
        </div>

        {/* Subscription Quota Banner */}
        {subscription && (
          <div className={`mb-6 p-4 rounded-lg border ${
            hasQuota
              ? 'bg-green-50 border-green-200'
              : 'bg-red-50 border-red-200'
          }`}>
            <div className="flex items-start gap-3">
              <AlertCircle className={`w-5 h-5 flex-shrink-0 mt-0.5 ${
                hasQuota ? 'text-green-600' : 'text-red-600'
              }`} />
              <div className="flex-1">
                {hasQuota ? (
                  <div>
                    <p className="font-semibold text-green-900">
                      {subscription.plan.pricing_name} - {subscription.remaining_listings} listing{subscription.remaining_listings !== 1 ? 's' : ''} remaining
                    </p>
                    <p className="text-sm text-green-700 mt-1">
                      You're using {subscription.listings_used} of {subscription.plan.max_listings} listings
                    </p>
                  </div>
                ) : (
                  <div>
                    <p className="font-semibold text-red-900">
                      Listing limit reached
                    </p>
                    <p className="text-sm text-red-700 mt-1">
                      You've used all {subscription.plan.max_listings} listing{subscription.plan.max_listings !== 1 ? 's' : ''} in your {subscription.plan.pricing_name}
                    </p>
                    <Button
                      onClick={() => navigate('/pricing')}
                      className="mt-3 bg-primary-600 hover:bg-primary-700"
                    >
                      Upgrade Plan
                    </Button>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {[
              { num: 1, label: 'Basic Info' },
              { num: 2, label: 'Description' },
              { num: 3, label: 'Images' },
            ].map((step, index) => (
              <div key={step.num} className="flex items-center flex-1">
                <div className="flex flex-col items-center flex-1">
                  <div
                    className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-colors ${
                      currentStep >= step.num
                        ? 'bg-primary-600 text-white'
                        : 'bg-gray-200 text-gray-600'
                    }`}
                  >
                    {step.num}
                  </div>
                  <span className="text-sm mt-2 font-medium text-gray-700">
                    {step.label}
                  </span>
                </div>
                {index < 2 && (
                  <div
                    className={`h-1 flex-1 transition-colors ${
                      currentStep > step.num ? 'bg-primary-600' : 'bg-gray-200'
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
          {/* STEP 1: Basic Info */}
          {currentStep === 1 && (
            <div className="card space-y-6">
              <h2 className="text-xl font-semibold">Basic Information</h2>

              {/* Category */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category *
                </label>
                <select
                  {...register('cat_id', { valueAsNumber: true })}
                  className="input"
                >
                  <option value="">Select a category</option>
                  {categories?.map((cat) => (
                    <option key={cat.cat_id} value={cat.cat_id}>
                      {cat.cat_name}
                    </option>
                  ))}
                </select>
                {errors.cat_id && (
                  <p className="mt-1 text-sm text-red-600">{errors.cat_id.message}</p>
                )}
              </div>

              {/* Title */}
              <Input
                label="Listing Title *"
                placeholder="e.g., Beautiful 3-Bedroom House in Rohero"
                error={errors.listing_title?.message}
                {...register('listing_title')}
              />

              {/* Price */}
              <Input
                label="Price (BIF) *"
                type="number"
                placeholder="e.g., 50000000"
                error={errors.listing_price?.message}
                {...register('listing_price', { valueAsNumber: true })}
              />

              {/* Location */}
              <LocationInput
                label="Location *"
                placeholder="e.g., Bujumbura, Rohero"
                error={errors.list_location?.message}
                {...register('list_location')}
              />

              <Button
                type="button"
                onClick={() => canProceedToStep2 && setCurrentStep(2)}
                fullWidth
                disabled={!canProceedToStep2}
              >
                Next: Description
              </Button>
            </div>
          )}

          {/* STEP 2: Description */}
          {currentStep === 2 && (
            <div className="card space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">Description</h2>
                <button
                  type="button"
                  onClick={() => setCurrentStep(1)}
                  className="text-sm text-primary-600 hover:text-primary-700"
                >
                  Back to Basic Info
                </button>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Detailed Description *
                </label>
                <textarea
                  {...register('list_description')}
                  rows={10}
                  placeholder="Describe your listing in detail. Include features, condition, location details, etc."
                  className="input resize-none"
                />
                {errors.list_description && (
                  <p className="mt-1 text-sm text-red-600">
                    {errors.list_description.message}
                  </p>
                )}
                <p className="mt-1 text-sm text-gray-500">
                  {watchedValues.list_description?.length || 0} / 2000 characters
                </p>
              </div>

              <Button
                type="button"
                onClick={() => canProceedToStep3 && setCurrentStep(3)}
                fullWidth
                disabled={!canProceedToStep3}
              >
                Next: Upload Images
              </Button>
            </div>
          )}

          {/* STEP 3: Images */}
          {currentStep === 3 && (
            <div className="card space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-semibold">Upload Images</h2>
                <button
                  type="button"
                  onClick={() => setCurrentStep(2)}
                  className="text-sm text-primary-600 hover:text-primary-700"
                >
                  Back to Description
                </button>
              </div>

              <ImageUpload
                images={images}
                onImagesChange={setImages}
                maxImages={subscription?.plan?.max_images_per_listing || 5}
              />

              {/* Preview Summary */}
              <div className="bg-gray-50 rounded-lg p-4 space-y-2">
                <h3 className="font-semibold text-gray-900">Summary</h3>
                <div className="text-sm text-gray-600 space-y-1">
                  <p>• Category: {categories?.find(c => c.cat_id === watchedValues.cat_id)?.cat_name}</p>
                  <p>• Title: {watchedValues.listing_title}</p>
                  <p>• Price: {watchedValues.listing_price?.toLocaleString()} BIF</p>
                  <p>• Location: {watchedValues.list_location}</p>
                  <p>• Images: {images.length} uploaded</p>
                </div>
              </div>

              <Button
                type="submit"
                fullWidth
                isLoading={createMutation.isPending}
                disabled={images.length === 0 || !hasQuota}
              >
                {!hasQuota ? 'Upgrade Plan to Create Listing' : 'Create Listing'}
              </Button>
            </div>
          )}
        </form>
      </div>
    </Layout>
  );
}