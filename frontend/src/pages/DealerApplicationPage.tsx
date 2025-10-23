import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQuery } from '@tantml:react-query';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { toast } from 'react-hot-toast';
import { Building2, ArrowLeft, CheckCircle, XCircle, Clock } from 'lucide-react';
import Layout from '../components/layout/Layout';
import Button from '../components/common/Button';
import LoadingSpinner from '../components/common/LoadingSpinner';
import StepIndicator, { Step } from '../components/common/StepIndicator';
import FormStep from '../components/common/FormStep';
import { useMultiStepForm } from '../hooks/useMultiStepForm';
import { dealerApplicationsApi } from '../api/dealerApplications';
import type { DealerApplicationCreateData } from '../types';

const schema = yup.object({
  business_name: yup.string().required('Business name is required').min(3, 'Business name must be at least 3 characters'),
  business_type: yup.string().required('Business type is required').oneOf(['real_estate', 'vehicle', 'both'], 'Invalid business type'),
  business_address: yup.string().required('Business address is required'),
  business_phone: yup.string().matches(/^\+?[0-9]{8,15}$/, 'Invalid phone number'),
  business_email: yup.string().email('Invalid email address'),
  tax_id: yup.string(),
  business_license: yup.string(),
});

const steps: Step[] = [
  {
    number: 1,
    label: 'Business Info',
    description: 'Basic business details'
  },
  {
    number: 2,
    label: 'Contact Details',
    description: 'Address and contact'
  },
  {
    number: 3,
    label: 'Legal Info',
    description: 'Tax ID and license'
  }
];

export default function DealerApplicationPage() {
  const navigate = useNavigate();
  const [submitting, setSubmitting] = useState(false);

  // Multi-step form
  const {
    currentStep,
    completedSteps,
    nextStep,
    previousStep,
    isFirstStep,
    isLastStep
  } = useMultiStepForm({
    totalSteps: 3
  });

  // Check existing application status
  const { data: applicationStatus, isLoading: loadingStatus } = useQuery({
    queryKey: ['dealer-application-status'],
    queryFn: dealerApplicationsApi.getStatus,
  });

  const { register, handleSubmit, watch, formState: { errors } } = useForm<DealerApplicationCreateData>({
    resolver: yupResolver(schema),
    mode: 'onChange'
  });

  const submitMutation = useMutation({
    mutationFn: dealerApplicationsApi.create,
    onSuccess: (data) => {
      toast.success('Dealer application submitted successfully!');
      navigate('/profile');
    },
    onError: (error: any) => {
      const message = error.response?.data?.error || 'Failed to submit application';
      toast.error(message);
      setSubmitting(false);
    },
  });

  const onSubmit = (data: DealerApplicationCreateData) => {
    setSubmitting(true);
    submitMutation.mutate(data);
  };

  // Validation for each step
  const validateStep = (step: number): boolean => {
    const values = watch();

    switch (step) {
      case 1: // Business Info
        return !!(values.business_name && values.business_type) &&
               !errors.business_name && !errors.business_type;
      case 2: // Contact Details
        return !!(values.business_address) &&
               !errors.business_address && !errors.business_phone && !errors.business_email;
      case 3: // Legal Info (all optional)
        return !errors.tax_id && !errors.business_license;
      default:
        return false;
    }
  };

  const handleNextStep = () => {
    if (validateStep(currentStep)) {
      nextStep();
    }
  };

  // If loading status
  if (loadingStatus) {
    return (
      <Layout>
        <div className="flex justify-center py-20">
          <LoadingSpinner size="lg" text="Loading application status..." />
        </div>
      </Layout>
    );
  }

  // If already has application
  const hasApplication = applicationStatus && 'dealerapp_id' in applicationStatus;

  if (hasApplication) {
    const app = applicationStatus as any;
    return (
      <Layout>
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Button variant="outline" onClick={() => navigate('/profile')} className="mb-6">
            <ArrowLeft className="w-4 h-4" />
            Back to Profile
          </Button>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
            <div className="text-center mb-8">
              {app.appli_status === 'pending' && (
                <>
                  <Clock className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">Application Pending</h1>
                  <p className="text-gray-600">Your dealer application is under review</p>
                </>
              )}
              {app.appli_status === 'approved' && (
                <>
                  <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">Application Approved!</h1>
                  <p className="text-gray-600">Congratulations! You are now a verified dealer</p>
                </>
              )}
              {app.appli_status === 'rejected' && (
                <>
                  <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">Application Rejected</h1>
                  <p className="text-gray-600">Sorry, your application was not approved</p>
                </>
              )}
            </div>

            <div className="border-t border-gray-200 pt-6">
              <h2 className="font-semibold text-gray-900 mb-4">Application Details</h2>
              <dl className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <dt className="text-gray-600">Business Name:</dt>
                  <dd className="font-medium text-gray-900">{app.business_name}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-gray-600">Business Type:</dt>
                  <dd className="font-medium text-gray-900 capitalize">
                    {app.business_type.replace('_', ' ')}
                  </dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-gray-600">Status:</dt>
                  <dd className={`font-medium capitalize ${
                    app.appli_status === 'approved' ? 'text-green-600' :
                    app.appli_status === 'pending' ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {app.appli_status}
                  </dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-gray-600">Submitted:</dt>
                  <dd className="font-medium text-gray-900">
                    {new Date(app.createdat).toLocaleDateString()}
                  </dd>
                </div>
                {app.rejection_reason && (
                  <div className="pt-3 border-t border-gray-200">
                    <dt className="text-gray-600 mb-2">Rejection Reason:</dt>
                    <dd className="text-red-600 text-sm bg-red-50 p-3 rounded">
                      {app.rejection_reason}
                    </dd>
                  </div>
                )}
              </dl>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Button variant="outline" onClick={() => navigate('/profile')} className="mb-6">
          <ArrowLeft className="w-4 h-4" />
          Back to Profile
        </Button>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
              <Building2 className="w-8 h-8 text-primary-600" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Apply to Become a Dealer</h1>
            <p className="text-gray-600">
              Join our network of verified dealers and get access to premium features
            </p>
          </div>

          {/* Benefits */}
          <div className="bg-primary-50 border border-primary-200 rounded-lg p-6 mb-8">
            <h2 className="font-semibold text-primary-900 mb-3">Dealer Benefits:</h2>
            <ul className="space-y-2 text-sm text-primary-800">
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-primary-600" />
                <span>Verified dealer badge on your profile</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-primary-600" />
                <span>Priority placement in search results</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-primary-600" />
                <span>Unlimited active listings</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-primary-600" />
                <span>Advanced analytics and insights</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-primary-600" />
                <span>Dedicated support</span>
              </li>
            </ul>
          </div>

          {/* Step Indicator */}
          <StepIndicator
            steps={steps}
            currentStep={currentStep}
            completedSteps={completedSteps}
          />

          {/* Application Form */}
          <form onSubmit={handleSubmit(onSubmit)}>
            {/* Step 1: Business Information */}
            {currentStep === 1 && (
              <FormStep
                title="Business Information"
                description="Tell us about your business"
                onNext={handleNextStep}
                isFirstStep={isFirstStep}
                isLastStep={isLastStep}
                isValid={validateStep(1)}
              >
                {/* Business Name */}
                <div>
                  <label htmlFor="business_name" className="block text-sm font-medium text-gray-700 mb-2">
                    Business Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    {...register('business_name')}
                    type="text"
                    id="business_name"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="e.g., Premium Real Estate Ltd"
                  />
                  {errors.business_name && (
                    <p className="mt-1 text-sm text-red-600">{errors.business_name.message}</p>
                  )}
                </div>

                {/* Business Type */}
                <div>
                  <label htmlFor="business_type" className="block text-sm font-medium text-gray-700 mb-2">
                    Business Type <span className="text-red-500">*</span>
                  </label>
                  <select
                    {...register('business_type')}
                    id="business_type"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Select business type</option>
                    <option value="real_estate">Real Estate</option>
                    <option value="vehicle">Vehicle</option>
                    <option value="both">Both</option>
                  </select>
                  {errors.business_type && (
                    <p className="mt-1 text-sm text-red-600">{errors.business_type.message}</p>
                  )}
                </div>
              </FormStep>
            )}

            {/* Step 2: Contact Details */}
            {currentStep === 2 && (
              <FormStep
                title="Contact Details"
                description="How can customers reach you?"
                onBack={previousStep}
                onNext={handleNextStep}
                isFirstStep={isFirstStep}
                isLastStep={isLastStep}
                isValid={validateStep(2)}
              >
                {/* Business Address */}
                <div>
                  <label htmlFor="business_address" className="block text-sm font-medium text-gray-700 mb-2">
                    Business Address <span className="text-red-500">*</span>
                  </label>
                  <textarea
                    {...register('business_address')}
                    id="business_address"
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="Full business address including city and province"
                  />
                  {errors.business_address && (
                    <p className="mt-1 text-sm text-red-600">{errors.business_address.message}</p>
                  )}
                </div>

                {/* Business Phone */}
                <div>
                  <label htmlFor="business_phone" className="block text-sm font-medium text-gray-700 mb-2">
                    Business Phone
                  </label>
                  <input
                    {...register('business_phone')}
                    type="tel"
                    id="business_phone"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="+257 79 123 456"
                  />
                  {errors.business_phone && (
                    <p className="mt-1 text-sm text-red-600">{errors.business_phone.message}</p>
                  )}
                </div>

                {/* Business Email */}
                <div>
                  <label htmlFor="business_email" className="block text-sm font-medium text-gray-700 mb-2">
                    Business Email
                  </label>
                  <input
                    {...register('business_email')}
                    type="email"
                    id="business_email"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="contact@yourbusiness.bi"
                  />
                  {errors.business_email && (
                    <p className="mt-1 text-sm text-red-600">{errors.business_email.message}</p>
                  )}
                </div>
              </FormStep>
            )}

            {/* Step 3: Legal Information */}
            {currentStep === 3 && (
              <FormStep
                title="Legal Information"
                description="Optional: Provide your business credentials"
                onBack={previousStep}
                isFirstStep={isFirstStep}
                isLastStep={isLastStep}
                isValid={validateStep(3)}
                isSubmitting={submitting}
              >
                {/* Tax ID */}
                <div>
                  <label htmlFor="tax_id" className="block text-sm font-medium text-gray-700 mb-2">
                    Tax ID / TIN (Optional)
                  </label>
                  <input
                    {...register('tax_id')}
                    type="text"
                    id="tax_id"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="TIN123456789"
                  />
                </div>

                {/* Business License */}
                <div>
                  <label htmlFor="business_license" className="block text-sm font-medium text-gray-700 mb-2">
                    Business License Number (Optional)
                  </label>
                  <input
                    {...register('business_license')}
                    type="text"
                    id="business_license"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="BL123456"
                  />
                </div>

                {/* Terms */}
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <p className="text-sm text-gray-700">
                    By submitting this application, you agree to our dealer terms and conditions.
                    We will review your application within 2-3 business days and notify you via email.
                  </p>
                </div>
              </FormStep>
            )}
          </form>
        </div>
      </div>
    </Layout>
  );
}
