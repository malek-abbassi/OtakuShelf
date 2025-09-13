import { z } from 'zod';

// Form schemas
export const signInSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
});

export const signUpSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 'Password must contain at least one uppercase letter, one lowercase letter, and one number'),
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(50, 'Username must be at most 50 characters')
    .regex(/^[\w-]+$/, 'Username can only contain letters, numbers, underscores, and hyphens'),
  fullName: z.string()
    .min(1, 'Full name is required')
    .max(100, 'Full name must be at most 100 characters')
    .optional(),
});

export const profileUpdateSchema = z.object({
  username: z.string()
    .min(3, 'Username must be at least 3 characters')
    .max(50, 'Username must be at most 50 characters')
    .regex(/^[\w-]+$/, 'Username can only contain letters, numbers, underscores, and hyphens')
    .optional(),
  fullName: z.string()
    .max(100, 'Full name must be at most 100 characters')
    .optional(),
});

// Type definitions
export type SignInSchema = z.output<typeof signInSchema>;
export type SignUpSchema = z.output<typeof signUpSchema>;
export type ProfileUpdateSchema = z.output<typeof profileUpdateSchema>;

// API response types
export type User = {
  id: number;
  username: string;
  email: string;
  fullName?: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
};

export type UserProfile = {
  id: number;
  username: string;
  email: string;
  fullName?: string;
  isActive: boolean;
  createdAt: string;
  watchlistCount: number;
};

export type AuthResponse = {
  message: string;
  data?: {
    userId: number;
    username: string;
  };
};

export type UsernameCheckResponse = {
  username: string;
  available: boolean;
  message: string;
};
