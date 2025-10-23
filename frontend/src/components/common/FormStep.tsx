import { ReactNode } from 'react';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import Button from './Button';

interface FormStepProps {
  children: ReactNode;
  title?: string;
  description?: string;
  onBack?: () => void;
  onNext?: () => void;
  isFirstStep?: boolean;
  isLastStep?: boolean;
  isValid?: boolean;
  nextLabel?: string;
  backLabel?: string;
  isSubmitting?: boolean;
}

export default function FormStep({
  children,
  title,
  description,
  onBack,
  onNext,
  isFirstStep = false,
  isLastStep = false,
  isValid = true,
  nextLabel,
  backLabel = 'Back',
  isSubmitting = false
}: FormStepProps) {
  const defaultNextLabel = isLastStep ? 'Submit' : 'Next';

  return (
    <div className="space-y-6">
      {/* Step Header */}
      {(title || description) && (
        <div className="mb-6">
          {title && (
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {title}
            </h2>
          )}
          {description && (
            <p className="text-gray-600">
              {description}
            </p>
          )}
        </div>
      )}

      {/* Step Content */}
      <div className="space-y-6">
        {children}
      </div>

      {/* Navigation Buttons */}
      <div className="flex items-center justify-between pt-6 border-t border-gray-200">
        <div>
          {!isFirstStep && onBack && (
            <Button
              type="button"
              variant="outline"
              onClick={onBack}
              disabled={isSubmitting}
            >
              <ArrowLeft className="w-4 h-4" />
              {backLabel}
            </Button>
          )}
        </div>

        <div>
          {onNext && (
            <Button
              type={isLastStep ? 'submit' : 'button'}
              onClick={isLastStep ? undefined : onNext}
              disabled={!isValid || isSubmitting}
            >
              {isSubmitting ? 'Submitting...' : (nextLabel || defaultNextLabel)}
              {!isLastStep && <ArrowRight className="w-4 h-4" />}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
