import { useState, useCallback } from 'react';

interface UseMultiStepFormOptions {
  totalSteps: number;
  initialStep?: number;
  onStepChange?: (step: number) => void;
}

export function useMultiStepForm({
  totalSteps,
  initialStep = 1,
  onStepChange
}: UseMultiStepFormOptions) {
  const [currentStep, setCurrentStep] = useState(initialStep);
  const [completedSteps, setCompletedSteps] = useState<number[]>([]);
  const [visitedSteps, setVisitedSteps] = useState<number[]>([initialStep]);

  const goToStep = useCallback((step: number) => {
    if (step >= 1 && step <= totalSteps) {
      setCurrentStep(step);
      setVisitedSteps(prev =>
        prev.includes(step) ? prev : [...prev, step]
      );
      onStepChange?.(step);
    }
  }, [totalSteps, onStepChange]);

  const nextStep = useCallback(() => {
    if (currentStep < totalSteps) {
      // Mark current step as completed
      setCompletedSteps(prev =>
        prev.includes(currentStep) ? prev : [...prev, currentStep]
      );
      goToStep(currentStep + 1);
    }
  }, [currentStep, totalSteps, goToStep]);

  const previousStep = useCallback(() => {
    if (currentStep > 1) {
      goToStep(currentStep - 1);
    }
  }, [currentStep, goToStep]);

  const reset = useCallback(() => {
    setCurrentStep(initialStep);
    setCompletedSteps([]);
    setVisitedSteps([initialStep]);
  }, [initialStep]);

  const isFirstStep = currentStep === 1;
  const isLastStep = currentStep === totalSteps;
  const isStepCompleted = useCallback(
    (step: number) => completedSteps.includes(step),
    [completedSteps]
  );
  const isStepVisited = useCallback(
    (step: number) => visitedSteps.includes(step),
    [visitedSteps]
  );

  return {
    currentStep,
    completedSteps,
    visitedSteps,
    goToStep,
    nextStep,
    previousStep,
    reset,
    isFirstStep,
    isLastStep,
    isStepCompleted,
    isStepVisited,
    progress: (completedSteps.length / totalSteps) * 100
  };
}
