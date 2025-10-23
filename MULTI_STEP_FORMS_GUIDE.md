# 📝 Multi-Step Forms Guide - Umuhuza Platform

## Overview

This guide explains how to create beautiful, user-friendly multi-step forms throughout the Umuhuza platform.

---

## 🎯 Why Multi-Step Forms?

**Benefits:**
- ✅ Reduces cognitive load - users focus on one section at a time
- ✅ Improves completion rates - feels less overwhelming
- ✅ Better mobile experience - easier to navigate on small screens
- ✅ Progressive validation - catch errors early
- ✅ Save progress - users can go back and edit
- ✅ Professional appearance - modern, clean UX

**Best For:**
- Complex forms with 6+ fields
- Forms requiring file uploads
- Forms with conditional fields
- Forms requiring validation at each step

---

## 🏗️ Architecture

### Components Structure

```
frontend/src/
├── components/
│   └── common/
│       ├── MultiStepForm.tsx       # Reusable wrapper
│       ├── StepIndicator.tsx       # Progress visualization
│       └── FormStep.tsx            # Individual step wrapper
├── pages/
│   ├── CreateListingPage.tsx      # Example: Listing creation
│   ├── DealerApplicationPage.tsx   # Example: Dealer application
│   └── Register MultiStepPage.tsx  # Example: User registration
```

---

## 🔧 Reusable Components

### 1. StepIndicator Component

**File:** `frontend/src/components/common/StepIndicator.tsx`

```typescript
import { Check } from 'lucide-react';

interface Step {
  number: number;
  label: string;
  description?: string;
}

interface StepIndicatorProps {
  steps: Step[];
  currentStep: number;
  completedSteps?: number[];
}

export default function StepIndicator({
  steps,
  currentStep,
  completedSteps = []
}: StepIndicatorProps) {
  return (
    <div className="w-full py-6">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => (
          <div key={step.number} className="flex items-center flex-1">
            {/* Step Circle */}
            <div className="flex flex-col items-center flex-1">
              <div className={`
                w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all duration-200
                ${currentStep === step.number
                  ? 'bg-primary-600 text-white ring-4 ring-primary-100'
                  : completedSteps.includes(step.number)
                  ? 'bg-green-500 text-white'
                  : 'bg-gray-200 text-gray-600'}
              `}>
                {completedSteps.includes(step.number) ? (
                  <Check className="w-5 h-5" />
                ) : (
                  step.number
                )}
              </div>

              {/* Label */}
              <span className={`text-sm mt-2 font-medium text-center ${
                currentStep === step.number
                  ? 'text-primary-600'
                  : 'text-gray-600'
              }`}>
                {step.label}
              </span>

              {/* Description (optional) */}
              {step.description && (
                <span className="text-xs text-gray-500 mt-1 text-center hidden sm:block">
                  {step.description}
                </span>
              )}
            </div>

            {/* Connector Line */}
            {index < steps.length - 1 && (
              <div className={`h-1 flex-1 mx-2 transition-colors duration-200 ${
                currentStep > step.number || completedSteps.includes(step.number)
                  ? 'bg-primary-600'
                  : 'bg-gray-200'
              }`} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 2. MultiStepForm Hook

**File:** `frontend/src/hooks/useMultiStepForm.ts`

```typescript
import { useState, useCallback } from 'react';

interface UseMultiStepFormOptions {
  totalSteps: number;
  onStepChange?: (step: number) => void;
  onComplete?: () => void;
}

export function useMultiStepForm({
  totalSteps,
  onStepChange,
  onComplete
}: UseMultiStepFormOptions) {
  const [currentStep, setCurrentStep] = useState(1);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);
  const [visitedSteps, setVisitedSteps] = useState<number[]>([1]);

  const goToStep = useCallback((step: number) => {
    if (step >= 1 && step <= totalSteps) {
      setCurrentStep(step);
      setVisitedSteps(prev => [...new Set([...prev, step])]);
      onStepChange?.(step);
    }
  }, [totalSteps, onStepChange]);

  const nextStep = useCallback(() => {
    if (currentStep < totalSteps) {
      setCompletedSteps(prev => [...new Set([...prev, currentStep])]);
      goToStep(currentStep + 1);
    } else {
      onComplete?.();
    }
  }, [currentStep, totalSteps, goToStep, onComplete]);

  const previousStep = useCallback(() => {
    if (currentStep > 1) {
      goToStep(currentStep - 1);
    }
  }, [currentStep, goToStep]);

  const isFirstStep = currentStep === 1;
  const isLastStep = currentStep === totalSteps;
  const isStepCompleted = (step: number) => completedSteps.includes(step);
  const isStepVisited = (step: number) => visitedSteps.includes(step);

  return {
    currentStep,
    completedSteps,
    visitedSteps,
    goToStep,
    nextStep,
    previousStep,
    isFirstStep,
    isLastStep,
    isStepCompleted,
    isStepVisited,
  };
}
```

### 3. FormStep Wrapper

**File:** `frontend/src/components/common/FormStep.tsx`

```typescript
import { ReactNode } from 'react';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import Button from './Button';

interface FormStepProps {
  title: string;
  description?: string;
  children: ReactNode;
  onNext?: () => void;
  onPrevious?: () => void;
  isFirstStep?: boolean;
  isLastStep?: boolean;
  canProceed?: boolean;
  isLoading?: boolean;
  nextButtonText?: string;
  previousButtonText?: string;
}

export default function FormStep({
  title,
  description,
  children,
  onNext,
  onPrevious,
  isFirstStep = false,
  isLastStep = false,
  canProceed = true,
  isLoading = false,
  nextButtonText,
  previousButtonText,
}: FormStepProps) {
  return (
    <div className="card space-y-6 animate-fadeIn">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
          {description && (
            <p className="text-sm text-gray-600 mt-1">{description}</p>
          )}
        </div>

        {/* Back Link (for non-first steps) */}
        {!isFirstStep && onPrevious && (
          <button
            type="button"
            onClick={onPrevious}
            className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1"
          >
            <ArrowLeft className="w-4 h-4" />
            {previousButtonText || 'Back'}
          </button>
        )}
      </div>

      {/* Content */}
      <div>{children}</div>

      {/* Navigation */}
      {onNext && (
        <div className="pt-4 border-t border-gray-200">
          <Button
            type="button"
            onClick={onNext}
            fullWidth
            disabled={!canProceed}
            isLoading={isLoading}
          >
            {nextButtonText || (isLastStep ? 'Submit' : 'Next')}
            {!isLastStep && <ArrowRight className="w-4 h-4 ml-2" />}
          </Button>
        </div>
      )}
    </div>
  );
}
```

---

## 📋 Implementation Examples

### Example 1: Create Listing (Already Implemented)

**File:** `frontend/src/pages/CreateListingPage.tsx`

**Steps:**
1. Basic Info (category, title, price, location)
2. Description
3. Images

**Key Features:**
- Form validation at each step
- Progress indicator
- Can't proceed without required fields
- Local preview of images before upload
- Summary before submission

### Example 2: User Registration (New)

**File:** `frontend/src/pages/RegisterMultiStepPage.tsx`

```typescript
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import Layout from '../components/layout/Layout';
import StepIndicator from '../components/common/StepIndicator';
import FormStep from '../components/common/FormStep';
import { useMultiStepForm } from '../hooks/useMultiStepForm';
import { authApi } from '../api/auth';

const steps = [
  { number: 1, label: 'Account', description: 'Basic info' },
  { number: 2, label: 'Personal', description: 'Your details' },
  { number: 3, label: 'Verify', description: 'Confirm identity' },
];

const schema = yup.object({
  email: yup.string().email().required(),
  password: yup.string().min(8).required(),
  user_firstname: yup.string().required(),
  user_lastname: yup.string().required(),
  phone_number: yup.string().required(),
});

export default function RegisterMultiStepPage() {
  const navigate = useNavigate();
  const { register, handleSubmit, watch, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
  });

  const {
    currentStep,
    completedSteps,
    nextStep,
    previousStep,
    isFirstStep,
    isLastStep,
  } = useMultiStepForm({
    totalSteps: 3,
    onComplete: handleSubmit(onSubmit),
  });

  const watchedValues = watch();

  const canProceedStep1 = watchedValues.email && watchedValues.password;
  const canProceedStep2 = watchedValues.user_firstname &&
                          watchedValues.user_lastname &&
                          watchedValues.phone_number;

  async function onSubmit(data: any) {
    try {
      await authApi.register(data);
      navigate('/verify');
    } catch (error) {
      // Handle error
    }
  }

  return (
    <Layout>
      <div className="max-w-2xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-2">Create Account</h1>
        <p className="text-gray-600 text-center mb-8">
          Join Umuhuza and start buying & selling
        </p>

        <StepIndicator
          steps={steps}
          currentStep={currentStep}
          completedSteps={completedSteps}
        />

        <form onSubmit={handleSubmit(onSubmit)}>
          {currentStep === 1 && (
            <FormStep
              title="Account Information"
              description="Create your login credentials"
              onNext={nextStep}
              canProceed={!!canProceedStep1}
              isFirstStep={isFirstStep}
              isLastStep={isLastStep}
            >
              <div className="space-y-4">
                <input
                  {...register('email')}
                  type="email"
                  placeholder="Email"
                  className="input"
                />
                {errors.email && <p className="text-red-600 text-sm">{errors.email.message}</p>}

                <input
                  {...register('password')}
                  type="password"
                  placeholder="Password"
                  className="input"
                />
                {errors.password && <p className="text-red-600 text-sm">{errors.password.message}</p>}
              </div>
            </FormStep>
          )}

          {currentStep === 2 && (
            <FormStep
              title="Personal Information"
              description="Tell us about yourself"
              onNext={nextStep}
              onPrevious={previousStep}
              canProceed={!!canProceedStep2}
              isFirstStep={isFirstStep}
              isLastStep={isLastStep}
            >
              <div className="space-y-4">
                <input {...register('user_firstname')} placeholder="First Name" className="input" />
                <input {...register('user_lastname')} placeholder="Last Name" className="input" />
                <input {...register('phone_number')} placeholder="Phone Number" className="input" />
              </div>
            </FormStep>
          )}

          {currentStep === 3 && (
            <FormStep
              title="Review & Submit"
              description="Confirm your information"
              onNext={handleSubmit(onSubmit)}
              onPrevious={previousStep}
              isFirstStep={isFirstStep}
              isLastStep={isLastStep}
              nextButtonText="Create Account"
            >
              <div className="space-y-3 bg-gray-50 p-4 rounded-lg">
                <p><strong>Email:</strong> {watchedValues.email}</p>
                <p><strong>Name:</strong> {watchedValues.user_firstname} {watchedValues.user_lastname}</p>
                <p><strong>Phone:</strong> {watchedValues.phone_number}</p>
              </div>
            </FormStep>
          )}
        </form>
      </div>
    </Layout>
  );
}
```

### Example 3: Edit Profile (Multi-Step)

**Steps:**
1. Basic Info (name, email, phone)
2. Location & Preferences
3. Profile Photo

### Example 4: Dealer Application (Already Has Form)

Convert `DealerApplicationPage.tsx` to multi-step:

**Steps:**
1. Business Information
2. Contact Details
3. Documents Upload
4. Review & Submit

---

## 🎨 Styling Guidelines

### Animation Classes

Add to `index.css`:

```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}

/* Step transition */
.step-enter {
  opacity: 0;
  transform: translateX(20px);
}

.step-enter-active {
  opacity: 1;
  transform: translateX(0);
  transition: opacity 300ms, transform 300ms;
}

.step-exit {
  opacity: 1;
  transform: translateX(0);
}

.step-exit-active {
  opacity: 0;
  transform: translateX(-20px);
  transition: opacity 300ms, transform 300ms;
}
```

### Card Styles

```css
.card {
  @apply bg-white rounded-lg shadow-sm border border-gray-200 p-6;
}

.card-hover {
  @apply card transition-shadow hover:shadow-md;
}
```

---

## ✅ Best Practices

### 1. Field Validation

```typescript
// Validate BEFORE allowing next step
const canProceedToStep2 = watch(['cat_id', 'listing_title']).every(val => val);

<Button
  onClick={nextStep}
  disabled={!canProceedToStep2}
>
  Next
</Button>
```

### 2. Save Progress

```typescript
// Save to localStorage
useEffect(() => {
  const formData = watch();
  localStorage.setItem('draft_listing', JSON.stringify(formData));
}, [watch()]);

// Load on mount
useEffect(() => {
  const draft = localStorage.getItem('draft_listing');
  if (draft) {
    const data = JSON.parse(draft);
    Object.keys(data).forEach(key => setValue(key, data[key]));
  }
}, []);
```

### 3. Prevent Data Loss

```typescript
// Warn user before leaving
useEffect(() => {
  const handleBeforeUnload = (e: BeforeUnloadEvent) => {
    if (currentStep > 1) {
      e.preventDefault();
      e.returnValue = '';
    }
  };

  window.addEventListener('beforeunload', handleBeforeUnload);
  return () => window.removeEventListener('beforeunload', handleBeforeUnload);
}, [currentStep]);
```

### 4. Mobile Optimization

```typescript
// Hide step descriptions on mobile
<span className="hidden sm:inline">{step.description}</span>

// Stack buttons vertically on mobile
<div className="flex flex-col sm:flex-row gap-3">
  <Button variant="outline" onClick={previousStep}>Back</Button>
  <Button onClick={nextStep}>Next</Button>
</div>
```

### 5. Accessibility

```typescript
// Add ARIA labels
<div
  role="progressbar"
  aria-valuenow={currentStep}
  aria-valuemin={1}
  aria-valuemax={totalSteps}
  aria-label={`Step ${currentStep} of ${totalSteps}`}
>

// Focus management
useEffect(() => {
  // Focus first input when step changes
  const firstInput = document.querySelector<HTMLInputElement>('input:not([disabled])');
  firstInput?.focus();
}, [currentStep]);
```

---

## 🔧 Converting Existing Forms

### Before (Single-Page Form)

```typescript
export default function RegisterPage() {
  return (
    <form>
      <input name="email" />
      <input name="password" />
      <input name="firstname" />
      <input name="lastname" />
      <input name="phone" />
      <button>Register</button>
    </form>
  );
}
```

### After (Multi-Step Form)

```typescript
export default function RegisterPage() {
  const { currentStep, nextStep, previousStep } = useMultiStepForm({ totalSteps: 3 });

  return (
    <>
      <StepIndicator currentStep={currentStep} />

      {currentStep === 1 && (
        <FormStep title="Account" onNext={nextStep}>
          <input name="email" />
          <input name="password" />
        </FormStep>
      )}

      {currentStep === 2 && (
        <FormStep title="Personal" onNext={nextStep} onPrevious={previousStep}>
          <input name="firstname" />
          <input name="lastname" />
        </FormStep>
      )}

      {currentStep === 3 && (
        <FormStep title="Contact" onNext={handleSubmit} onPrevious={previousStep}>
          <input name="phone" />
        </FormStep>
      )}
    </>
  );
}
```

---

## 📊 Forms to Convert

### Priority 1 (High Impact)
- ✅ Create Listing - Already done
- ⏳ Dealer Application - TODO
- ⏳ User Registration - TODO
- ⏳ Edit Profile - TODO

### Priority 2 (Medium Impact)
- ⏳ Edit Listing - TODO
- ⏳ Payment Checkout - TODO (currently modal)
- ⏳ Report Submission - TODO (currently modal)

### Priority 3 (Low Impact)
- Single-field forms (login, search, etc.) - Keep single-page

---

## 🚀 Quick Start Checklist

To convert any form to multi-step:

- [ ] Identify logical groupings (3-5 steps ideal)
- [ ] Create step definitions with labels
- [ ] Add StepIndicator component
- [ ] Wrap each step in FormStep component
- [ ] Implement useMultiStepForm hook
- [ ] Add validation per step
- [ ] Test navigation (next/back/direct)
- [ ] Add animations
- [ ] Test mobile responsiveness
- [ ] Add accessibility features

---

## 📝 Summary

**Key Takeaways:**
1. Multi-step forms improve UX significantly
2. Reusable components save development time
3. Validation at each step catches errors early
4. Mobile-first design is essential
5. Save user progress to prevent data loss

**Next Steps:**
1. Create reusable components (StepIndicator, FormStep, hook)
2. Convert Dealer Application to multi-step
3. Add multi-step registration
4. Document any custom patterns

---

**Last Updated:** 2025-01-22
**Maintained By:** Umuhuza Development Team
