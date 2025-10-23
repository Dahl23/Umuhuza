import { Check } from 'lucide-react';

export interface Step {
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
                w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all duration-300
                ${currentStep === step.number
                  ? 'bg-primary-600 text-white ring-4 ring-primary-100 scale-110'
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
              <span className={`text-sm mt-2 font-medium text-center transition-colors ${
                currentStep === step.number
                  ? 'text-primary-600'
                  : completedSteps.includes(step.number)
                  ? 'text-green-600'
                  : 'text-gray-600'
              }`}>
                {step.label}
              </span>

              {/* Description (optional, hidden on mobile) */}
              {step.description && (
                <span className="text-xs text-gray-500 mt-1 text-center hidden sm:block">
                  {step.description}
                </span>
              )}
            </div>

            {/* Connector Line */}
            {index < steps.length - 1 && (
              <div className={`h-1 flex-1 mx-2 transition-all duration-300 ${
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
