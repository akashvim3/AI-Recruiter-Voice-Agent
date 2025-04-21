import { create } from 'zustand';
import axios from 'axios';

interface Job {
  id: string;
  title: string;
  description: string;
  requirements: string;
  location: string;
  salary_range: string;
  job_type: string;
  experience_level: string;
  posted_by: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

interface JobState {
  jobs: Job[];
  selectedJob: Job | null;
  isLoading: boolean;
  error: string | null;
  fetchJobs: () => Promise<void>;
  fetchJobById: (id: string) => Promise<void>;
  createJob: (jobData: Partial<Job>) => Promise<void>;
  updateJob: (id: string, jobData: Partial<Job>) => Promise<void>;
  deleteJob: (id: string) => Promise<void>;
  applyForJob: (jobId: string, coverLetter: string, resume: File) => Promise<void>;
}

export const useJobStore = create<JobState>((set) => ({
  jobs: [],
  selectedJob: null,
  isLoading: false,
  error: null,
  fetchJobs: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get('/api/jobs/jobs/');
      set({ jobs: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  fetchJobById: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`/api/jobs/jobs/${id}/`);
      set({ selectedJob: response.data, isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  createJob: async (jobData: Partial<Job>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post('/api/jobs/jobs/', jobData);
      set((state) => ({
        jobs: [...state.jobs, response.data],
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  updateJob: async (id: string, jobData: Partial<Job>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.patch(`/api/jobs/jobs/${id}/`, jobData);
      set((state) => ({
        jobs: state.jobs.map((job) =>
          job.id === id ? response.data : job
        ),
        selectedJob: response.data,
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  deleteJob: async (id: string) => {
    set({ isLoading: true, error: null });
    try {
      await axios.delete(`/api/jobs/jobs/${id}/`);
      set((state) => ({
        jobs: state.jobs.filter((job) => job.id !== id),
        selectedJob: null,
        isLoading: false,
      }));
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
  applyForJob: async (jobId: string, coverLetter: string, resume: File) => {
    set({ isLoading: true, error: null });
    try {
      const formData = new FormData();
      formData.append('cover_letter', coverLetter);
      formData.append('resume', resume);
      await axios.post(`/api/jobs/jobs/${jobId}/apply/`, formData);
      set({ isLoading: false });
    } catch (error: any) {
      set({ error: error.message, isLoading: false });
    }
  },
})); 