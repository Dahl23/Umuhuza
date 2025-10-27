import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
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
import { ArrowLeft, Save } from 'lucide-react';

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

export default function EditListingPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [images, setImages] = useState<File[]>([]);

  const {
    register,
    handleSubmit,
    reset,
    watch,
    formState: { errors },
  } = useForm<ListingFormData>({
    resolver: yupResolver(schema),
  });

  // Fetch listing data
  const { data: listing, isLoading: listingLoading } = useQuery({
    queryKey: ['listing', id],
    queryFn: () => listingsApi.getById(Number(id)),
    enabled: !!id,
  });

  // Fetch categories
  const { data: categories, isLoading: categoriesLoading } = useQuery({
    queryKey: ['categories'],
    queryFn: listingsApi.getCategories,
  });

  // Pre-populate form when listing data is loaded
  useEffect(() => {
    if (listing) {
      reset({
        cat_id: listing.category.cat_id,
        listing_title: listing.listing_title,
        list_description: listing.list_description,
        listing_price: parseFloat(listing.listing_price),
        list_location: listing.list_location,
      });
    }
  }, [listing, reset]);

  // Update listing mutation
  const updateMutation = useMutation({
    mutationFn: async (data: ListingFormData) => {
      return listingsApi.update(Number(id), {
        ...data,
        listing_price: data.listing_price.toString(),
      });
    },
    onSuccess: () => {
      toast.success('Listing updated successfully!');
      queryClient.invalidateQueries({ queryKey: ['listing', id] });
      queryClient.invalidateQueries({ queryKey: ['my-listings'] });
      navigate(`/listings/${id}`);
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Failed to update listing');
    },
  });

  const onSubmit = (data: ListingFormData) => {
    updateMutation.mutate(data);
  };

  const watchedValues = watch();

  if (listingLoading || categoriesLoading) {
    return (
      <Layout>
        <div className="flex justify-center py-20">
          <LoadingSpinner size="lg" text="Loading listing..." />
        </div>
      </Layout>
    );
  }

  if (!listing) {
    return (
      <Layout>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p className="text-red-600 mb-4">Listing not found</p>
            <Button onClick={() => navigate('/my-listings')}>
              Back to My Listings
            </Button>
          </div>
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
            <Save className="w-8 h-8 text-primary-600" />
            Edit Listing
          </h1>
          <p className="text-gray-600 mt-2">
            Update your listing details
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
          {/* Basic Info */}
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

            {/* Status Display (Read-only) */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Status
              </label>
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <p className="text-sm text-gray-600 mb-2">
                  Current Status: <span className="font-semibold capitalize text-gray-900">{listing?.listing_status}</span>
                </p>
                <p className="text-xs text-gray-500">
                  To change the status of this listing (active, sold, or hidden), go to the "My Listings" page and click the three-dot menu (⋮) next to this listing.
                  Status changes cannot be made directly through editing.
                </p>
              </div>
            </div>
          </div>

          {/* Description */}
          <div className="card space-y-6">
            <h2 className="text-xl font-semibold">Description</h2>

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
          </div>

          {/* Current Images */}
          <div className="card space-y-6">
            <h2 className="text-xl font-semibold">Images</h2>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-sm text-blue-800">
                <strong>Note:</strong> Image management is currently view-only.
                To change images, please delete and recreate the listing, or contact support.
              </p>
            </div>

            {listing.images.length > 0 ? (
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {listing.images
                  .sort((a, b) => a.display_order - b.display_order)
                  .map((img) => (
                    <div
                      key={img.listimage_id}
                      className="relative aspect-square rounded-lg overflow-hidden border-2 border-gray-200"
                    >
                      <img
                        src={img.image_url}
                        alt=""
                        className="w-full h-full object-cover"
                      />
                      {img.is_primary && (
                        <div className="absolute top-2 left-2 bg-primary-600 text-white text-xs px-2 py-1 rounded">
                          Primary
                        </div>
                      )}
                    </div>
                  ))}
              </div>
            ) : (
              <p className="text-gray-500">No images</p>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate(-1)}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={updateMutation.isPending}
              className="flex-1"
            >
              <Save className="w-5 h-5" />
              Save Changes
            </Button>
          </div>
        </form>
      </div>
    </Layout>
  );
}
