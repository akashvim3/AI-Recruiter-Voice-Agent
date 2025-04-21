import { create } from 'zustand';
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';

interface AuthState {
  user: any;
  isLoading: boolean;
  error: string | null;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, userData: any) => Promise<void>;
  signOut: () => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: false,
  error: null,
  signIn: async (email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      const supabase = createClientComponentClient();
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      if (error) throw error;
      set({ user: data.user, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  signUp: async (email: string, password: string, userData: any) => {
    set({ isLoading: true, error: null });
    try {
      const supabase = createClientComponentClient();
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: userData,
        },
      });
      if (error) throw error;
      set({ user: data.user, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  signOut: async () => {
    set({ isLoading: true, error: null });
    try {
      const supabase = createClientComponentClient();
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
      set({ user: null, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  resetPassword: async (email: string) => {
    set({ isLoading: true, error: null });
    try {
      const supabase = createClientComponentClient();
      const { error } = await supabase.auth.resetPasswordForEmail(email);
      if (error) throw error;
      set({ isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
})); 