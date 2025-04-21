import { create } from 'zustand';
import axios from 'axios';

interface Interview {
  id: string;
  job: string;
  candidate: string;
  interviewer: string;
  scheduled_date: string;
  duration: number;
  status: string;
  feedback: string | null;
  created_at: string;
  updated_at: string;
}

interface InterviewState {
  interviews: Interview[];
  selectedInterview: Interview | null;
  isLoading: boolean;
  error: string | null;
  fetchInterviews: () => Promise<void>;
  fetchInterviewById: (id: string) => Promise<void>;
  scheduleInterview: (interviewData: Omit<Interview, 'id' | 'created_at' | 'updated_at'>) => Promise<void>;
  updateInterview: (id: string, interviewData: Partial<Interview>) => Promise<void>;
  cancelInterview: (id: string) => Promise<void>;
  submitFeedback: (id: string, feedback: string) => Promise<void>;
}

export const useInterviewStore = create<InterviewState>((set) => ({
  interviews: [],
  selectedInterview: null,
  isLoading: false,
  error: null,
  fetchInterviews: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get('/api/interviews/');
      set({ interviews: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  fetchInterviewById: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`/api/interviews/${id}/`);
      set({ selectedInterview: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  scheduleInterview: async (interviewData: Omit<Interview, 'id' | 'created_at' | 'updated_at'>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post('/api/interviews/', interviewData);
      set((state) => ({
        interviews: [...state.interviews, response.data],
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  updateInterview: async (id: string, interviewData: Partial<Interview>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.patch(`/api/interviews/${id}/`, interviewData);
      set((state) => ({
        interviews: state.interviews.map((interview) =>
          interview.id === id ? response.data : interview
        ),
        selectedInterview: response.data,
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  cancelInterview: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      await axios.delete(`/api/interviews/${id}/`);
      set((state) => ({
        interviews: state.interviews.filter((interview) => interview.id !== id),
        selectedInterview: null,
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  submitFeedback: async (id: string, feedback: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.patch(`/api/interviews/${id}/`, { feedback });
      set((state) => ({
        interviews: state.interviews.map((interview) =>
          interview.id === id ? response.data : interview
        ),
        selectedInterview: response.data,
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
})); 