import { User } from 'lucide-react';

interface AvatarProps {
  src?: string | null;
  alt?: string;
  firstName?: string;
  lastName?: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
  className?: string;
}

export default function Avatar({
  src,
  alt,
  firstName = '',
  lastName = '',
  size = 'md',
  className = '',
}: AvatarProps) {
  // Generate initials from first and last name
  const getInitials = () => {
    const firstInitial = firstName?.charAt(0)?.toUpperCase() || '';
    const lastInitial = lastName?.charAt(0)?.toUpperCase() || '';
    return firstInitial + lastInitial || '?';
  };

  // Generate consistent color based on name
  const getColorFromName = () => {
    const name = `${firstName}${lastName}`.toLowerCase();
    const colors = [
      'bg-blue-500',
      'bg-green-500',
      'bg-yellow-500',
      'bg-red-500',
      'bg-purple-500',
      'bg-pink-500',
      'bg-indigo-500',
      'bg-teal-500',
      'bg-orange-500',
      'bg-cyan-500',
    ];

    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
  };

  // Size mappings
  const sizeClasses = {
    xs: 'w-6 h-6 text-xs',
    sm: 'w-8 h-8 text-sm',
    md: 'w-10 h-10 text-base',
    lg: 'w-12 h-12 text-lg',
    xl: 'w-16 h-16 text-xl',
    '2xl': 'w-24 h-24 text-3xl',
  };

  const iconSizes = {
    xs: 'w-3 h-3',
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
    xl: 'w-8 h-8',
    '2xl': 'w-12 h-12',
  };

  // Check if we have a valid profile photo
  const hasValidPhoto = src && src !== 'default-avatar.png' && !src.includes('default-avatar');

  if (hasValidPhoto) {
    return (
      <img
        src={src}
        alt={alt || `${firstName} ${lastName}`}
        className={`${sizeClasses[size]} rounded-full object-cover border-2 border-gray-200 ${className}`}
      />
    );
  }

  // Show initials if we have name
  if (firstName || lastName) {
    return (
      <div
        className={`${sizeClasses[size]} ${getColorFromName()} rounded-full flex items-center justify-center text-white font-semibold ${className}`}
        title={alt || `${firstName} ${lastName}`}
      >
        {getInitials()}
      </div>
    );
  }

  // Fallback to user icon
  return (
    <div
      className={`${sizeClasses[size]} bg-gray-300 rounded-full flex items-center justify-center text-gray-600 ${className}`}
      title={alt || 'User'}
    >
      <User className={iconSizes[size]} />
    </div>
  );
}
